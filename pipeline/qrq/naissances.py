"""Naissances selon le pays de naissance des parents, 1998-2025 (Insee 2381382, Figure 2).

« Né à l'étranger » n'est pas « immigré » : les Français nés à l'étranger y sont comptés.
Rupture de méthode 2010-2011 ; depuis 2023, le second parent peut être une mère n'ayant pas
accouché (notes du tableur).
"""

import re
from pathlib import Path

from .lecture import Annee, annee, entier, feuille, texte
from .sources import fichier

CATEGORIES = {
    "Les deux parents nés en France": "deux_parents_nes_en_france",
    "Un parent né en France, un parent né à l": "un_parent_ne_a_l_etranger",
    "Les deux parents nés à l'étranger": "deux_parents_nes_a_l_etranger",
}


def _annee(v) -> Annee | None:
    """En-tête d'année, appel de note compris : « 20231 » est 2023 suivi de la note 1."""
    a = annee(v)
    if a is None and re.fullmatch(r"(19|20)\d\d\d", texte(v)):
        a = annee(texte(v)[:4])
    return a


def lire_naissances_parents(raw: Path) -> list[dict]:
    rows = feuille(fichier(raw, "naissances_parents"), "Figure 2")
    entete = next(r for r in rows if _annee(r[1]))
    annees = [(i, _annee(v)) for i, v in enumerate(entete) if _annee(v)]
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


# Sous-lignes de la figure 2 : qui, de la mère ou du second parent, est né à l'étranger.
DETAIL = {
    "Mère née en France, second parent né dans un pays de l'UE": "mere_france_second_ue",
    "Mère née en France, second parent né hors UE": "mere_france_second_hors_ue",
    "Mère née dans un pays de l'UE à 27, second parent né en France": "mere_ue_second_france",
    "Mère née hors UE à 27, second parent né en France": "mere_hors_ue_second_france",
    "Deux parents nés dans un pays de l'UE": "deux_ue",
    "Deux parents nés hors UE": "deux_hors_ue",
    "Mère née dans un pays de l'UE à 27, second parent né hors UE": "mere_ue_second_hors_ue",
    "Mère née hors UE à 27, second parent né dans un pays de l": "mere_hors_ue_second_ue",
}


def lire_naissances_detail(raw: Path) -> list[dict]:
    """Sous-catégories de la figure 2 (2381382) : elles décomposent « un parent né à l'étranger » et
    « deux parents nés à l'étranger ». Avant 2023, le second parent est le père."""
    rows = feuille(fichier(raw, "naissances_parents"), "Figure 2")
    entete = next(r for r in rows if _annee(r[1]))
    annees = [(i, _annee(v)) for i, v in enumerate(entete) if _annee(v)]
    out = []
    for r in rows:
        lib = texte(r[0])
        cat = next((c for prefixe, c in DETAIL.items() if lib.startswith(prefixe)), None)
        if cat is None:
            continue
        for i, a in annees:
            v = entier(r[i])
            if v is not None:
                out.append({"annee": a.annee, "statut": a.statut, "categorie": cat, "naissances": v})
    assert len({o["categorie"] for o in out}) == len(DETAIL), "2381382 figure 2 : sous-catégorie manquante"
    return out
