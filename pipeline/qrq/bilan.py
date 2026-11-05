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


def completer_avant_1946(bilan: list[dict], population: dict[int, float]) -> None:
    """Complète l'onglet FM avant 1946 : population au 1er janvier manquante (1939-1945) lue dans
    les pyramides par âge (POP3, métropole), et solde migratoire, absent avant 1946, calculé par
    différence (résidu, U1). Les lignes complétées sont marquées `complete`."""
    fm = {b["annee"]: b for b in bilan if b["onglet"] == "FM"}
    for a, b in fm.items():
        if a < 1946 and b["population"] is None and a in population:
            b["population"] = round(population[a])
            b["complete"] = "population_pyramides"
    for a, b in fm.items():
        suiv = fm.get(a + 1)
        if a < 1946 and b["solde_migratoire"] is None and b["population"] is not None and suiv and suiv["population"] is not None:
            residu = suiv["population"] - b["population"] - b["solde_naturel"]
            if 1938 <= a <= 1945:  # 1938 : passage du bilan aux pyramides (sources différentes)
                # Guerre : les pyramides ne comptent pas les prisonniers et déportés hors du
                # territoire ; l'écart n'est pas une migration mais un ajustement de champ.
                b["solde_migratoire"], b["ajustement"] = 0, residu
                b["complete"] = (b.get("complete", "") + " guerre_ajustement").strip()
            else:
                b["solde_migratoire"], b["ajustement"] = residu, 0
                b["complete"] = (b.get("complete", "") + " solde_par_difference").strip()
