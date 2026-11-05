"""Lecture des tableurs Insee : cellules textuelles (« 7970 », « nd », « 2025 (p) »…) → valeurs typées.

Les tableurs de l'Insee stockent souvent les nombres sous forme de texte, avec des marqueurs
(`nd` non disponible, `///` sans objet, `ns` non significatif, `p` provisoire, `e` estimé,
`(*)` rupture de série). Ce module ne fait que traduire ces conventions ; les lecteurs par source
(stock.py, flux.py…) savent où sont les cellules.
"""

import re
from dataclasses import dataclass
from pathlib import Path

import openpyxl

MARQUEURS_VIDES = {"", "nd", "///", "ns", "-", "None"}


def feuille(chemin: Path, nom: str) -> list[tuple]:
    """Toutes les lignes d'une feuille, valeurs brutes (le nom est comparé sans espaces de bord)."""
    wb = openpyxl.load_workbook(chemin, data_only=True, read_only=True)
    try:
        noms = {n.strip(): n for n in wb.sheetnames}
        ws = wb[noms[nom.strip()]]
        return [tuple(r) for r in ws.iter_rows(values_only=True)]
    finally:
        wb.close()


def texte(v) -> str:
    return "" if v is None else str(v).replace("\xa0", " ").replace("\n", " ").strip()


def nombre(v) -> float | None:
    """« 7970 », « -71 », « 11.6 », « 1 234 », « +19p » → float ; marqueurs vides → None."""
    if isinstance(v, (int, float)):
        return float(v)
    s = texte(v).replace(" ", "").replace(",", ".")
    if s in MARQUEURS_VIDES:
        return None
    s = re.sub(r"[pe]$", "", s)  # « +19p », « 246e »
    try:
        return float(s)
    except ValueError:
        return None


@dataclass(frozen=True)
class Annee:
    annee: int
    statut: str  # "definitif" | "provisoire" | "estime"
    rupture: bool


def annee(v) -> Annee | None:
    """« 2025 (p) », « 2024 (p) (*) », « 2020e », 1968 → Annee ; autre chose → None."""
    s = texte(v)
    m = re.match(r"^(1[89]\d\d|20\d\d)\s*(e)?\s*(\(p\))?\s*(\(\*\))?$", s)
    if not m:
        return None
    statut = "provisoire" if m.group(3) else "estime" if m.group(2) else "definitif"
    return Annee(int(m.group(1)), statut, bool(m.group(4)))


def milliers(v) -> int | None:
    x = nombre(v)
    return None if x is None else round(x * 1000)


def entier(v) -> int | None:
    x = nombre(v)
    return None if x is None else round(x)
