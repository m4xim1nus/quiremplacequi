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

    # Pays de naissance (B2) : chaque agrégat = somme de ses parties (milliers arrondis). Avant 2006,
    # les Afriques sahélienne et guinéenne ne sont pas publiées : elles sont dans « Autres pays
    # d'Afrique ». Asie 1999 : +5 000 dans le tableur Insee lui-même (6793226, figure 2).
    pays = pl.read_csv(export / "b2_pays.csv").pivot(on="pays", index="annee", values="immigres")
    emboitements = {
        "Maghreb": ["Algérie", "Maroc, Tunisie"],
        "Afrique": ["Maghreb", "Afrique sahélienne", "Afrique guinéenne ou centrale", "Autres pays d'Afrique"],
        "Asie": ["Turquie", "Chine", "Asie du Sud-Est", "Autres pays d'Asie"],
        "Europe du Sud": ["Espagne, Italie", "Portugal"],
        "Europe": ["Europe du Sud", "Autres pays d'Europe"],
        "Ensemble": ["Afrique", "Asie", "Europe", "Amérique, Océanie"],
    }
    ecarts = {
        (tot, a): e
        for tot, parts in emboitements.items()
        for a, e in zip(pays["annee"], pays[tot] - pays.select(pl.sum_horizontal(parts)).to_series())
        if (tot, a) != ("Asie", 1999)
    }
    pire = max(ecarts, key=lambda k: abs(ecarts[k]))
    asie99 = pays.filter(pl.col("annee") == 1999).select(pl.col("Asie") - pl.sum_horizontal(emboitements["Asie"])).item()
    controle("pays : agrégats = Σ parties (± 2 000)", abs(ecarts[pire]) <= 2000, f"pire {pire[0]} {pire[1]} : {ecarts[pire]:+}")
    controle("pays : écart de la source Asie 1999 inchangé (+5 000)", asie99 == 5000, f"{asie99:+}")

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

    # Piscine v1 : générations (modèle de cohortes).
    gens = [x for x in ans if "g2a" in x]
    ecart = max(abs(x["immigres"] + x["g2a"] + x["g2b"] + x["g3"] + x["autres"] - x["population"]) for x in gens)
    controle("piscine : G1 + G2 + G3 + autres = population", ecart == 0, f"écart max {ecart}")
    neg = [x["annee"] for x in gens if min(x["autres"], x.get("naissances_autres") or 0, x.get("deces_autres") or 0) < 0]
    controle("piscine : aucun flux ni stock « autres » négatif", not neg, f"années {neg}" if neg else "")
    cal = pl.read_csv(export / "cohortes_calage.csv")
    ip = cal.filter((pl.col("temoin") == "ip1910_2020") & pl.col("cle").is_in(["0-17", "18-59", "60 ou plus"]))
    pire = (ip["modele"] - ip["observe"]).abs().max()
    controle("cohortes : parts par génération à ± 1,5 point d'IP 1910 (0-17, 18-59, 60+)", pire <= 1.5, f"écart max {pire:.2f} point")
    d = cal.filter((pl.col("temoin") == "descendants_2025") & (pl.col("cle") == "effectif"))
    ratio = d["modele"][0] / d["observe"][0]
    controle("cohortes : descendants 2025 à ± 10 % de l'enquête Emploi (témoin indépendant)", 0.9 <= ratio <= 1.1, f"modèle / Insee = {ratio:.3f}")
    dc = cal.filter(pl.col("temoin") == "deces_immigres_insee")
    ratio = dc["modele"].sum() / dc["observe"].sum()
    controle("cohortes : décès d'immigrés à ± 15 % des estimations Insee 2006-2022", 0.85 <= ratio <= 1.15, f"modèle / Insee = {ratio:.3f}")

    # TeO2 : anomalies de saisie (les anomalies de la source sont signalées, pas bloquantes).
    from .teo2 import lire_teo2, verifier_teo2

    anomalies = verifier_teo2(lire_teo2())
    lignes.append(f"info TeO2 : {len(lire_teo2())} cellules saisies, {len(anomalies)} anomalie(s) signalée(s)")
    lignes.extend(f"     · {a}" for a in anomalies)

    # Pyramides des âges : leur total retombe sur la population de la piscine. Le site n'en utilise
    # que des parts (« nés avant telle année »). En 1990, l'onglet ne donne que la métropole.
    ages = pl.read_csv(export / "ages.csv").group_by("annee").agg(pl.col("population").sum())
    tot = dict(ages.rows())
    ecarts = {a["annee"]: tot[a["annee"]] / a["population"] - 1 for a in ans if a["annee"] in tot and a["annee"] != 1990}
    pire = max(ecarts, key=lambda a: abs(ecarts[a]))
    controle(
        "ages : total = population de la piscine (± 0,5 %, hors 1990)",
        len(ecarts) == len(ans) - 1 and abs(ecarts[pire]) <= 0.005,
        f"pire {pire} : {100 * ecarts[pire]:+.2f} %",
    )

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
