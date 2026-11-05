"""Identités comptables, invariants et valeurs témoins, sur data/export/ (docs/CADRAGE.md §5)."""

import json
from pathlib import Path

import polars as pl

from .piscine import ecart_identite

# Années où un ajustement des immigrés est attendu (changement de champ, collecte) : U5, U6.
AJUSTEMENTS_ATTENDUS = {2013, 2023}


def verifier(export: Path) -> tuple[bool, list[str]]:
    lignes: list[str] = []
    ok = True

    def controle(nom: str, condition: bool, detail: str = "") -> None:
        nonlocal ok
        ok &= condition
        lignes.append(f"{'ok ' if condition else 'KO '} {nom}{' : ' + detail if detail else ''}")

    stock = pl.read_csv(export / "b1_stock.csv")
    flux = pl.read_csv(export / "flux.csv")
    bilan = pl.read_csv(export / "bilan.csv")
    nais = pl.read_csv(export / "naissances_parents.csv")
    psc = json.loads((export / "piscine.json").read_text())

    # Stock : Français de naissance + par acquisition + étrangers = population (arrondis au millier).
    s = stock.drop_nulls("etrangers")
    ecart = (s["francais_naissance"] + s["francais_acquisition"] + s["etrangers"] - s["population"]).abs().max()
    controle("stock : nationalités = population", ecart <= 1500, f"écart max {ecart} personnes")

    # Flux : évolution des immigrés = entrées − sorties − décès (IP 2107, arrondis au millier).
    f = flux.drop_nulls(["sorties_imm", "evolution_imm"])
    ecart = (f["entrees_imm"] - f["sorties_imm"] - f["deces_imm"] - f["evolution_imm"]).abs().max()
    controle("flux : Δimmigrés = E − S − D", ecart <= 2000, f"écart max {ecart}")

    # Bilan : population(a+1) = population(a) + solde naturel + solde migratoire + ajustement.
    for onglet in ("FM", "FR"):
        bl = bilan.filter(pl.col("onglet") == onglet).sort("annee").drop_nulls(["population", "solde_migratoire"])
        p = dict(zip(bl["annee"], bl["population"]))
        ecarts = {
            a: p[a + 1] - p[a] - sn - sm - (aj or 0)
            for a, sn, sm, aj in bl.select("annee", "solde_naturel", "solde_migratoire", "ajustement").rows()
            if a + 1 in p
        }
        mayotte = ecarts.pop(2013, None) if onglet == "FR" else None
        pire = max(map(abs, ecarts.values()))
        # Tolérance : arrondis de la source (onglet FR, quelques unités certaines années).
        controle(f"bilan {onglet} : ΔP = SN + SM + ajustement", pire <= 20, f"écart max {pire}")
        if onglet == "FR":
            # Mayotte entre dans le champ au 1er janvier 2014 (≈ 212 000 habitants au recensement de 2012).
            controle("bilan FR : entrée de Mayotte en 2014 (200 000 à 260 000)", 200_000 <= mayotte <= 260_000, f"{mayotte}")

    # Naissances : trois catégories = ensemble.
    piv = nais.pivot(on="categorie", index="annee", values="naissances")
    ecart = (piv["deux_parents_nes_en_france"] + piv["un_parent_ne_a_l_etranger"] + piv["deux_parents_nes_a_l_etranger"] - piv["ensemble"]).abs().max()
    controle("naissances : catégories = ensemble", ecart == 0, f"écart max {ecart}")

    # Piscine : identité des immigrés tenue chaque année (par construction).
    ans = psc["annees"]
    ecarts = [ecart_identite(x, y) for x, y in zip(ans, ans[1:])]
    controle("piscine : identité des immigrés", max(map(abs, ecarts)) == 0, f"écart max {max(map(abs, ecarts))}")

    # Piscine : sur les années mesurées, l'ajustement reste petit hors changements de champ.
    mesures = [x for x in ans if x.get("statut_flux") == "mesure" and x["annee"] not in AJUSTEMENTS_ATTENDUS]
    pire = max(mesures, key=lambda x: abs(x["ajust_imm"]))
    controle("piscine : ajustement des immigrés ≤ 15 000 (mesuré)", abs(pire["ajust_imm"]) <= 15000, f"max {pire['ajust_imm']} en {pire['annee']}")
    a13 = next(x for x in ans if x["annee"] == 2013)
    controle("piscine : Mayotte visible en 2013 (40 000 à 80 000)", 40000 <= a13["ajust_imm"] <= 80000, f"{a13['ajust_imm']}")

    # Piscine : le rapport des décès reste plausible.
    r = psc["ratio_deces"]
    controle("piscine : rapport des décès dans [0,9 ; 1,2]", 0.9 <= r["min"] and r["max"] <= 1.2, f"moyen {r['moyen']}, min {r['min']}, max {r['max']}")

    # Témoins lus dans les sources (docs/spike/insee.md).
    temoins = {
        ("b1_stock", 2025, "immigres"): 7_970_000,
        ("b1_stock", 1931, "immigres"): 2_729_300,
        ("b1_stock", 1921, "part_immigres"): 3.7,
    }
    for (t, a, col), attendu in temoins.items():
        v = stock.filter(pl.col("annee") == a)[col][0]
        controle(f"témoin {t} {a} {col}", v == attendu, f"{v}")
    a22 = next(x for x in ans if x["annee"] == 2022)
    controle("témoin piscine 2022 : 375 000 entrées, 26 000 sorties, 71 000 décès", (a22["entrees_imm"], a22["sorties_imm"], a22["deces_imm"]) == (375000, 26000, 71000))
    return ok, lignes
