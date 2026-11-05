"""Bilan démographique : population au 1er janvier et composantes (Insee 8999013).

Onglet `FM` : France métropolitaine (naissances et décès depuis 1901, population et solde
migratoire depuis 1946). Onglet `FR` : France hors Mayotte jusqu'en 2013, France ensuite
(population depuis 1982). Le solde migratoire est un résidu (U1).
"""

from pathlib import Path

from .lecture import annee, entier, feuille
from .sources import fichier

CHAMPS = {"FM": "metropole", "FR": "france"}


def lire_bilan(raw: Path) -> list[dict]:
    out = []
    for onglet, champ in CHAMPS.items():
        for r in feuille(fichier(raw, "bilan"), onglet):
            a = annee(r[0])
            if not a:
                continue
            ajust = [entier(r[i]) for i in (7, 8, 9)]
            c = champ
            if onglet == "FR":
                c = "france_hors_mayotte" if a.annee <= 2013 else "france"
            out.append(
                {
                    "annee": a.annee,
                    "champ": c,
                    "onglet": onglet,
                    "statut": a.statut,
                    "population": entier(r[1]),
                    "naissances": entier(r[2]),
                    "deces": entier(r[3]),
                    "solde_naturel": entier(r[4]),
                    "solde_migratoire": entier(r[6]),
                    "ajustement": None if all(x is None for x in ajust) else sum(x or 0 for x in ajust),
                }
            )
    return out
