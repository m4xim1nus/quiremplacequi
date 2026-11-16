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
    f = flux.drop_nulls(["solde_imm", "solde_ni", "sorties_ni"])
    ecart = max((f["entrees_imm"] - f["sorties_imm"] - f["solde_imm"]).abs().max(), (f["entrees_ni"] - f["sorties_ni"] - f["solde_ni"]).abs().max())
    controle("flux : solde publié = E − S (± 1 000, arrondis)", ecart <= 1000, f"écart max {ecart}")

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

    # Avant 2006 (répartition « solde_bilan ») : solde des non-immigrés constant entre deux
    # recensements, à l'arrondi près ; la rupture de 1974 apparaît dans le flux des immigrés.
    rep = psc.get("repartition_flux", {})
    if rep.get("methode") == "solde_bilan":
        recs = [r for r in (1968, 1975, 1982, 1990, 1999, 2006) if r >= rep["de"]]
        par = {a["annee"]: a for a in ans}
        ecart = max(max(par[a]["net_ni"] for a in range(r0, r1)) - min(par[a]["net_ni"] for a in range(r0, r1)) for r0, r1 in zip(recs, recs[1:]))
        controle("piscine : solde des non-immigrés constant entre deux recensements (1968-2005)", ecart <= 5, f"écart max {ecart}")
        controle("piscine : flux net des immigrés de 1974 < moitié de 1973", par[1974]["net_imm"] < par[1973]["net_imm"] / 2, f"{par[1973]['net_imm']} → {par[1974]['net_imm']}")

    # Piscine v1 : générations (modèle de cohortes).
    gens = [x for x in ans if "g2a" in x]
    ecart = max(abs(x["immigres"] + x["g2a"] + x["g2b"] + x["g3"] + x["autres"] - x["population"]) for x in gens)
    controle("piscine : G1 + G2 + G3 + autres = population", ecart == 0, f"écart max {ecart}")
    # Fourchette U20 (G2 vivants en 1911) : la référence est dedans ; en 2025, elle ne pèse pas.
    hors = [x["annee"] for x in gens for g in ("g2a", "g2b", "g3") if not x[f"{g}_min"] <= x[g] <= x[f"{g}_max"]]
    controle("piscine : générations dans leur fourchette U20", not hors, f"années {hors}" if hors else "")
    a25 = next(x for x in gens if x["annee"] == 2025)
    large = max(100 * max(a25[g] - a25[f"{g}_min"], a25[f"{g}_max"] - a25[g]) / a25["population"] for g in ("g2a", "g2b", "g3"))
    controle("piscine : fourchette U20 en 2025 à ± 0,15 point", large <= 0.15, f"± {large:.2f} point")
    neg = [x["annee"] for x in gens if min(x["autres"], x.get("naissances_autres") or 0, x.get("deces_autres") or 0) < 0]
    controle("piscine : aucun flux ni stock « autres » négatif", not neg, f"années {neg}" if neg else "")
    cal = pl.read_csv(export / "cohortes_calage.csv")
    ip = cal.filter((pl.col("temoin") == "ip1910_2020") & pl.col("cle").is_in(["0-17", "18-59", "60 ou plus"]))
    pire = (ip["modele"] - ip["observe"]).abs().max()
    controle("cohortes : parts par génération à ± 1,5 point d'IP 1910 (0-17, 18-59, 60+)", pire <= 1.5, f"écart max {pire:.2f} point")
    d = cal.filter((pl.col("temoin") == "descendants_2025") & (pl.col("cle") == "effectif"))
    ratio = d["modele"][0] / d["observe"][0]
    controle("cohortes : descendants 2025 à ± 10 % de l'enquête Emploi (témoin indépendant)", 0.9 <= ratio <= 1.1, f"modèle / Insee = {ratio:.3f}")
    # Âges des immigrés au recensement (tous logements, 1990-2025) : la bascule du profil d'arrivée est
    # choisie sur ces années (explo/profil_arrivee.py) ; IP 1910 reste le témoin indépendant.
    rp = cal.filter(pl.col("temoin") == "rp_ages_g1")
    ec = (rp["modele"] - rp["observe"]).abs()
    pire = rp["cle"][ec.arg_max()]
    controle("cohortes : âges des immigrés à ± 3 points du recensement (4 classes, 1990-2025)", ec.max() <= 3, f"pire {pire} : {ec.max():.1f} point")
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

    # Titres de séjour (DSED) : chaque fichier annuel est cohérent (motifs, sous-motifs, nationalités),
    # et les deux sources se raccordent (série du 27 juin 2024 + Britanniques = fichier annuel).
    tit = pl.read_csv(export / "titres.csv")
    tot = pl.read_csv(export / "titres_totaux.csv")
    somme = dict(tit.group_by("annee").agg(pl.col("titres").sum()).rows())
    # Avant 2015, la série par motif est publiée hors Britanniques (moins de 250 titres par an).
    ecarts = {a: somme[a] - n + (b if a < 2015 else 0) for a, n, b in tot.select("annee", "total", "britanniques").rows()}
    pire = max(ecarts, key=lambda a: abs(ecarts[a]))
    controle("titres : Σ sous-motifs = total publié (2011-2024 ; hors Britanniques avant 2015)", ecarts[pire] == 0 and len(ecarts) >= 14, f"pire {pire} : {ecarts[pire]:+}")
    an = tot.drop_nulls("total_nationalites")
    ecart = max((an["total"] - an["total_nationalites"]).abs().max(), (an["total"] - an["somme_motifs_annuel"]).abs().max())
    controle("titres : total = Σ motifs = Σ nationalités (fichiers annuels)", ecart == 0, f"écart max {ecart}")
    rac = tot.drop_nulls("serie_hors_britanniques")
    defi = rac.filter(pl.col("serie_statut") == "definitif")
    ecart = (defi["serie_hors_britanniques"] + defi["serie_britanniques"] - defi["total"]).abs().max()
    controle("titres : raccord des deux sources DSED (années définitives)", ecart == 0 and len(defi) >= 8, f"écart max {ecart}, {len(defi)} années")
    prov = rac.filter(pl.col("serie_statut") == "provisoire")
    rev = (prov["total"] / (prov["serie_hors_britanniques"] + prov["serie_britanniques"]) - 1).abs().max()
    controle("titres : révision du provisoire au définitif ≤ 2 %", rev <= 0.02, f"{100 * rev:.1f} %")

    # Eurostat : décisions positives = réfugié + protection subsidiaire + raisons humanitaires ;
    # nés à l'étranger + nés dans le pays ≤ population ; croissance = naturel + migratoire (‰).
    eu = pl.read_csv(export / "eurostat.csv")
    piv = eu.pivot(on="indicateur", index=["geo", "annee"], values="valeur")
    d = piv.drop_nulls(["decisions_positives", "statut_refugie", "protection_subsidiaire"])
    ecart = (d["statut_refugie"] + d["protection_subsidiaire"] + d["raisons_humanitaires"].fill_null(0) - d["decisions_positives"]).abs().max()
    controle("eurostat : décisions positives = Σ statuts", ecart <= 5, f"écart max {ecart}")
    n = piv.drop_nulls(["nes_etranger", "nes_pays", "pop_naissance_total"])
    inc = (n["pop_naissance_total"] - n["nes_etranger"] - n["nes_pays"]) / n["pop_naissance_total"]
    controle("eurostat : naissance inconnue entre 0 et 2 % de la population", inc.min() >= 0 and inc.max() <= 0.02, f"de {100 * inc.min():.2f} à {100 * inc.max():.2f} %")
    g = piv.drop_nulls(["taux_croissance", "taux_naturel", "taux_migratoire"])
    ecart = (g["taux_croissance"] - g["taux_naturel"] - g["taux_migratoire"]).abs().max()
    controle("eurostat : croissance = naturel + migratoire (± 0,15 ‰)", ecart <= 0.15, f"écart max {ecart:.2f} ‰")
    fr = piv.filter((pl.col("geo") == "FR") & (pl.col("annee") == 2025))
    insee25 = bilan.filter((pl.col("onglet") == "FR") & (pl.col("annee") == 2025))["population"][0]
    r = fr["population"][0] / insee25 - 1
    controle("eurostat : population de la France 2025 = bilan Insee (± 0,5 %)", abs(r) <= 0.005, f"{100 * r:+.2f} %")

    # OCDE : chaque pays publie ses six catégories et sa population.
    oc = pl.read_csv(export / "ocde.csv")
    p = oc.filter((pl.col("pays_code") == "FRA") & (pl.col("annee") == 2024))
    controle("ocde : France 2024, six catégories et population", len(p) == 7 and p["valeur"].min() > 0, f"{len(p)} indicateurs")

    # Entrées par origine (IP 2107, figure 3) : régions = ensemble, ensemble = flux.csv.
    eo = dict(pl.read_csv(export / "entrees_origine.csv").select("origine", "entrees").rows())
    a_eo = pl.read_csv(export / "entrees_origine.csv")["annee"][0]
    ecart = abs(eo["Afrique"] + eo["Asie"] + eo["Europe"] + eo["Amérique, Océanie"] - eo["Ensemble des immigrés"])
    controle("entrées par origine : Σ régions = ensemble des immigrés (± 2 000)", ecart <= 2000, f"écart {ecart}")
    fx = flux.filter(pl.col("annee") == a_eo)["entrees_imm"][0]
    controle("entrées par origine : ensemble = flux.csv de la même année", fx == eo["Ensemble des immigrés"], f"{fx} et {eo['Ensemble des immigrés']}")

    # ONU : les huit grandes régions de destination font le total des émigrés d'Afrique
    # subsaharienne ; les pays ont presque tous émigrés, population et PIB par habitant.
    reg = pl.read_csv(export / "onu_regions.csv")
    rr = dict(reg.select("destination", "migrants").rows())
    somme = reg.filter(pl.col("code_destination").is_in([1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836]))["migrants"].sum()
    controle("onu : Σ régions de destination = émigrés d'Afrique subsaharienne", somme == rr["Monde"], f"{somme} et {rr['Monde']}")
    op = pl.read_csv(export / "onu_pays.csv")
    complets = op.filter(pl.col("population") >= 1_000_000).drop_nulls(["emigres", "pib_hab_usd"])
    controle("onu : au moins 150 pays d'un million d'habitants complets", len(complets) >= 150, f"{len(complets)} pays")
    fr_onu = op.filter(pl.col("code") == 250)
    controle("témoin onu France 2024 : 9 186 757 migrants (définition large)", fr_onu["immigres"][0] == 9_186_757, f"{fr_onu['immigres'][0]}")

    # Naissances : les sous-catégories de la figure 2 refont leurs totaux, chaque année.
    det = pl.read_csv(export / "naissances_detail.csv")
    un = ["mere_france_second_ue", "mere_france_second_hors_ue", "mere_ue_second_france", "mere_hors_ue_second_france"]
    deux = ["deux_ue", "deux_hors_ue", "mere_ue_second_hors_ue", "mere_hors_ue_second_ue"]
    ecarts = []
    for (a,), g in det.group_by("annee"):
        d = dict(g.select("categorie", "naissances").rows())
        n = dict(nais.filter(pl.col("annee") == a).select("categorie", "naissances").rows())
        if sum(d[c] for c in un) != n["un_parent_ne_a_l_etranger"] or sum(d[c] for c in deux) != n["deux_parents_nes_a_l_etranger"]:
            ecarts.append(a)
    controle("naissances : sous-catégories = « un parent » et « deux parents » nés à l'étranger", not ecarts, f"années {sorted(ecarts)}")

    # Fécondité : l'ICF d'ensemble est entre ceux des femmes nées en France et à l'étranger ;
    # descendance finale témoin ; calendrier des naissances autour de l'arrivée ≈ 100 %.
    icf = pl.read_csv(export / "fecondite_icf.csv").pivot(on="groupe", index="annee", values="icf")
    hors = icf.filter((pl.col("ensemble") < pl.col("nees_en_france")) | (pl.col("ensemble") > pl.col("nees_a_l_etranger")))
    controle("fécondité : ICF ensemble entre nées en France et nées à l'étranger (2006-2021)", hors.is_empty(), f"{hors['annee'].to_list()}")
    v = icf.filter(pl.col("annee") == 2021)["nees_a_l_etranger"][0]
    controle("témoin IP 1939 : ICF ajusté des femmes nées à l'étranger 2021 = 2,33", v == 2.33, f"{v}")
    dfe = pl.read_csv(export / "fecondite_descendance.csv").filter(pl.col("dimension") == "lien")
    dl = dict(dfe.select("categorie", "valeur").rows())
    controle("témoin IP 1939 : descendance finale 2,35 (immigrées), 1,90 (descendantes), 1,86 (ni l'un ni l'autre)",
             (dl["immigrees"], dl["descendantes"], dl["ni_immigrees_ni_descendantes"]) == (2.35, 1.9, 1.86))
    cal = pl.read_csv(export / "fecondite_arrivee.csv")
    tot_cal = cal["en_france"].sum() + cal["a_l_etranger"].sum()
    controle("fécondité : calendrier des naissances autour de l'arrivée, Σ ≈ 100 % (± 1,5)", abs(tot_cal - 100) <= 1.5, f"{tot_cal:.1f}")
    # Seuil de remplacement = ICF pour 100 femmes / taux net de reproduction (filles qui atteignent
    # l'âge de leur mère) : autour de 2,05 en France aujourd'hui.
    fn = pl.read_csv(export / "fecondite_nationale.csv")
    der = fn.filter(pl.col("champ") == "france").sort("annee").tail(1)
    seuil = 100 * der["icf"][0] / der["taux_reproduction_net"][0]
    controle(f"fécondité : seuil de remplacement {der['annee'][0]} entre 2,0 et 2,1", 2.0 <= seuil <= 2.1, f"{seuil:.3f}")
    controle("témoin bilan 2025 : ICF France 2025 = 1,56", der["icf"][0] == 1.56 and der["annee"][0] == 2025, f"{der['icf'][0]}")
    dg = dict(pl.read_csv(export / "descendance_generations.csv").rows())
    controle("témoin descendance : génération 1950 (métropole) 2,117", dg[1950] == 2.117, f"{dg[1950]}")

    # ONU 2000 : moyenne annuelle × 50 ≈ total (arrondis des milliers) ; pas de migration au scénario II.
    o2 = pl.read_csv(export / "onu2000.csv")
    tot2 = dict(o2.filter(pl.col("indicateur") == "migrants_2000_2050").select("scenario", "valeur").rows())
    an2 = dict(o2.filter(pl.col("indicateur") == "migrants_par_an").select("scenario", "valeur").rows())
    ecart = max(abs(50 * an2[s] - tot2[s]) for s in tot2)
    controle("onu 2000 : 50 × moyenne annuelle = total 2000-2050 (± 25 000)", ecart <= 25 and tot2["II"] == 0, f"écart max {ecart:.0f} milliers")

    # Personnes en situation irrégulière : indices (U7), cohérence et témoin.
    irr = dict(pl.read_csv(export / "irreguliers.csv").select("cle", "valeur").rows())
    controle("témoin AME : 465 208 bénéficiaires au 31 décembre 2024, dont outre-mer moins", irr["ame_beneficiaires_2024"] == 465_208 and irr["ame_outre_mer_2024"] < irr["ame_beneficiaires_2024"])
    controle("Elipa 2 : sans papier avant les démarches ≥ sans papier à l'arrivée", irr["elipa_sans_papier_avant_demarches"] >= irr["elipa_sans_papier_arrivee"])

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
    controle("témoin titres 2024 : 345 587 premiers titres", tot.filter(pl.col("annee") == 2024)["total"][0] == 345_587)
    v = piv.filter((pl.col("geo") == "FR") & (pl.col("annee") == 2024))["premieres_demandes"][0]
    controle("témoin eurostat FR 2024 : 129 910 premières demandes d'asile", v == 129_910, f"{v}")
    return ok, lignes
