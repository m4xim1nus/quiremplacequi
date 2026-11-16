"""Flux migratoires 2006-2024 des immigrés et des non-immigrés (Insee Première 2107).

Les entrées sont estimées par l'Insee ; les sorties sont le solde migratoire moins les entrées
(U2) ; les décès d'immigrés sont modélisés (l'état civil ne les identifie pas). Valeurs en
milliers dans la source, converties en personnes.
"""

from pathlib import Path

import re

from .lecture import annee, feuille, milliers, texte
from .sources import fichier


def _figure(raw: Path, nom: str) -> dict[int, tuple]:
    out = {}
    for r in feuille(fichier(raw, "flux"), nom):
        a = annee(r[0])
        if a:
            out[a.annee] = (a, milliers(r[1]), milliers(r[2]), milliers(r[3]))
    return out


def lire_flux(raw: Path) -> list[dict]:
    imm = _figure(raw, "Figure 2a")
    ni = _figure(raw, "Figure 2b")
    tc1 = {}
    for r in feuille(fichier(raw, "flux"), "Tableau complémentaire 1"):
        a = annee(r[0])
        if a and milliers(r[1]) is not None:
            tc1[a.annee] = {
                "solde_naturel_imm": milliers(r[5]),
                "solde_naturel_ni": milliers(r[6]),
                "evolution_imm": milliers(r[2]),
                "evolution_ni": milliers(r[3]),
            }
    out = []
    for a in sorted(imm):
        info, e_imm, s_imm, sm_imm = imm[a]
        _, e_ni, s_ni, sm_ni = ni[a]
        t = tc1.get(a, {})
        sn_imm = t.get("solde_naturel_imm")
        out.append(
            {
                "annee": a,
                "statut": info.statut,
                "entrees_imm": e_imm,
                "sorties_imm": None if s_imm is None else -s_imm,
                "entrees_ni": e_ni,
                "sorties_ni": None if s_ni is None else -s_ni,
                # Soldes publiés (arrondis au millier par l'Insee, pas recalculés).
                "solde_imm": sm_imm,
                "solde_ni": sm_ni,
                "deces_imm": None if sn_imm is None else -sn_imm,
                "solde_naturel_ni": t.get("solde_naturel_ni"),
                "evolution_imm": t.get("evolution_imm"),
                "evolution_ni": t.get("evolution_ni"),
                "champ": "france_hors_mayotte" if a <= 2013 else "france",
            }
        )
    return out


def lire_entrees_origine(raw: Path) -> list[dict]:
    """Entrées d'immigrés de la dernière année par région de naissance (IP 2107, figure 3)."""
    lignes = feuille(fichier(raw, "flux"), "Figure 3")
    titre = texte(lignes[0][0])
    annee_ = int(re.search(r"en (20\d\d)", titre).group(1))
    out = []
    for r in lignes[3:]:
        nom = texte(r[0])
        if not nom or nom.startswith(("Lecture", "Champ", "Source", "Note")):
            continue
        n = milliers(r[1])
        if n is not None:
            out.append({"annee": annee_, "origine": nom, "entrees": n})
    return out
