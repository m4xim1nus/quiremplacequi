"""Sensibilité du modèle de cohortes à ses paramètres libres (referentiels/cohortes.yaml), pour la
fiche de relecture docs/PARAMETRES.md. Chaque variante est recalée (comme au build), puis comparée
à la référence : parts des générations en 1968 et 2025, écarts aux cibles et aux témoins.
Lancer depuis pipeline/ : uv run python explo/sensibilite_cohortes.py
"""
import copy
from pathlib import Path

import numpy as np
import yaml

from qrq import bilan, cohortes as C, flux, naissances, stock

R = Path("../data/raw")
P = yaml.safe_load(open("referentiels/cohortes.yaml"))
st, bl = stock.lire_stock(R), bilan.lire_bilan(R)
E = C.preparer(R, st, bl, naissances.lire_naissances_parents(R), P)
CIBLES = C.lire_cibles_ip1910(R)
FL = flux.lire_flux(R)
SORTIES = {f["annee"]: f["sorties_imm"] for f in FL if f["sorties_imm"] is not None}


def variante(**modifs) -> dict:
    p = copy.deepcopy(P)
    for chemin, v in modifs.items():
        d = p
        *tete, fin = chemin.split("__")
        for k in tete:
            d = d[k]
        d[fin] = v
    return p


PLATE = [{"de": 0, "a": 105, "poids": 1.0}]
VARIANTES = {
    "référence": variante(),
    "G2 initiaux ×0,5 (0,4)": variante(initial__g2_rapport_g1=0.4),
    "G2 initiaux ×1,5 (1,2)": variante(initial__g2_rapport_g1=1.2),
    "départs : forme plate": variante(departs__forme=PLATE),
    "départs : 2022 inclus": variante(calage__sorties=[2006, 2023]),
}


def resume(p: dict) -> dict:
    sim, cal = C.caler(E, p, CIBLES, SORTIES)
    an = {a["annee"]: a for a in sim["annees"]}
    ec = C.ecarts_calage(sim, E, CIBLES, FL, R)
    grandes = [x for x in ec if x["temoin"] == "ip1910_2020" and x["cle"] in ("0-17", "18-59", "60 ou plus")]
    d25 = next(x for x in ec if x["cle"] == "effectif")
    un = next(x for x in ec if x["cle"] == "part_un_parent")
    dc = [x for x in ec if x["temoin"] == "deces_immigres_insee"]
    parts = {}
    for t in (1968, 2025):
        tot = C._vecteur(E.ages, t).sum()
        parts[t] = {g: 100 * an[t][g] / tot for g in ("G2a", "G2b", "G3")}
    return {
        "taux": cal["taux_departs"],
        "err_ip": max(abs(x["modele"] - x["observe"]) for x in grandes),
        "desc25": d25["modele"] / d25["observe"],
        "un_parent": (un["modele"], un["observe"]),
        "deces": sum(x["modele"] for x in dc) / sum(x["observe"] for x in dc),
        "parts": parts,
    }


print(f"{'variante':26} {'taux':>6} {'IP±pt':>6} {'desc25':>6} {'1 par.':>11} {'décès':>6}"
      f" | 1968 G2a G2b  G3 | 2025 G2a G2b  G3")
for nom, p in VARIANTES.items():
    r = resume(p)
    p68, p25 = r["parts"][1968], r["parts"][2025]
    print(f"{nom:26} {100 * r['taux']:5.2f}% {r['err_ip']:6.2f} {r['desc25']:6.3f}"
          f" {r['un_parent'][0]:5.1f}/{r['un_parent'][1]:4.1f} {r['deces']:6.3f}"
          f" | {p68['G2a']:7.1f} {p68['G2b']:3.1f} {p68['G3']:4.1f}"
          f" | {p25['G2a']:7.1f} {p25['G2b']:3.1f} {p25['G3']:4.1f}")
