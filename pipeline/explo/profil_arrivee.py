"""Profil d'âge à l'arrivée des immigrés (referentiels/cohortes.yaml, `arrivees`) : effet sur les âges
des immigrés aux recensements (Insee 2381759, 1990-2025) et sur IP 1910. Compare le profil unique des
entrées de 2024 aux profils par époque (quartiles du stock de 1999 avant une année de bascule).
Lancer depuis pipeline/ : uv run python explo/profil_arrivee.py
"""
import copy
import json
from pathlib import Path

import yaml

from qrq import bilan, cohortes as C, flux, naissances, stock

R = Path("../data/raw")
P = yaml.safe_load(open("referentiels/cohortes.yaml"))
E = C.preparer(R, stock.lire_stock(R), bilan.lire_bilan(R), naissances.lire_naissances_parents(R), P)
PSC = json.loads(Path("../data/export/piscine.json").read_text())
E.stock_g1.update({x["annee"]: float(x["immigres"]) for x in PSC["annees"] if x["annee"] < 2006})
CI = C.lire_cibles_ip1910(R)
FL = flux.lire_flux(R)
S = {f["annee"]: f["sorties_imm"] for f in FL if f["sorties_imm"] is not None}
RP = C.lire_ages_immigres(R)
FINES = [c for c in CI if c["classe"] not in ("0-17", "18-59", "0-59", "60 ou plus")]


def essai(nom: str, ancien, bascule: int) -> None:
    E.profil_ancien, E.profil_bascule = ancien, bascule
    sim, cal = C.caler(E, P, CI, S)
    an = {a["annee"]: a for a in sim["annees"]}
    err = {}
    for t, o in RP.items():
        g = an[t]["etat"]["G1"]
        err[t] = max(abs(100 * g[a:b].sum() / g.sum() - o[c]) for c, (a, b) in C.CLASSES_RP.items())
    pop = C._vecteur(E.ages, 2020)
    ip = max(abs(C.parts_par_classe(an[2020]["etat"], pop, c["classe"])["G1"] - c["G1"]) for c in FINES)
    dc = [x for x in C.ecarts_calage(sim, E, CI, FL, R) if x["temoin"] == "deces_immigres_insee"]
    ratio = sum(x["modele"] for x in dc) / sum(x["observe"] for x in dc)
    print(f"{nom:24} décès {ratio:.3f} | IP 1910 max {ip:4.2f} | recensement max {max(err.values()):3.1f} |", " ".join(f"{t}:{e:.1f}" for t, e in err.items()))


# Quartiles du stock de 1999 (Insee, Les immigrés en France, 2005, fiche 1.7, figure 2).
P99 = C.profil_par_age([(0, 0.0), (12, 0.25), (22, 0.5), (28, 0.75), (75, 1.0)])
essai("entrées 2024 seules", None, 0)
for b in (1982, 1990, 1999):
    essai(f"stock 1999 avant {b}", P99, b)
# Variante : profil 2024 rajeuni, médiane 22 ans (âges × 22/26).
base = C.lire_profil_arrivee(R)
P2024_22 = C.profil_par_age([(0, 0.0)] + [(a * 22 / 26, c) for a, c in base if 0 < a < 75] + [(75, 1.0)])
for b in (1982, 1990, 1999):
    essai(f"2024 × 22/26 avant {b}", P2024_22, b)  # retenu : avant 1990 (cohortes.yaml)
