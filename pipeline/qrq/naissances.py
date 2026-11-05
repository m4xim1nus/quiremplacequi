"""Naissances selon le pays de naissance des parents, 1998-2025 (Insee 2381382, Figure 2).

« Né à l'étranger » n'est pas « immigré » : les Français nés à l'étranger y sont comptés.
Rupture de méthode 2010-2011 ; depuis 2023, le second parent peut être une mère n'ayant pas
accouché (notes du tableur).
"""

from pathlib import Path

from .lecture import annee, entier, feuille, texte
from .sources import fichier

CATEGORIES = {
    "Les deux parents nés en France": "deux_parents_nes_en_france",
    "Un parent né en France, un parent né à l": "un_parent_ne_a_l_etranger",
    "Les deux parents nés à l'étranger": "deux_parents_nes_a_l_etranger",
}


def lire_naissances_parents(raw: Path) -> list[dict]:
    rows = feuille(fichier(raw, "naissances_parents"), "Figure 2")
    entete = next(r for r in rows if annee(r[1]))
    annees = [(i, annee(v)) for i, v in enumerate(entete) if annee(v)]
    out = []
    for r in rows:
        lib = texte(r[0])
        cat = next((c for prefixe, c in CATEGORIES.items() if lib.startswith(prefixe)), None)
        if cat is None and lib.lower().startswith("ensemble"):
            cat = "ensemble"
        if cat is None:
            continue
        for i, a in annees:
            v = entier(r[i])
            if v is not None:
                out.append({"annee": a.annee, "statut": a.statut, "categorie": cat, "naissances": v})
    return out
