"""B1 : stock d'immigrés et d'étrangers, 1911-2025 (Insee 2381757 et 6793226)."""

from pathlib import Path

from .lecture import annee, feuille, milliers, nombre
from .sources import fichier


def champ_stock(a: int) -> str:
    """Champ des séries 2381757 et 6793226 (notes des tableurs ; U6)."""
    if a <= 1982:
        return "metropole"
    return "france_hors_mayotte" if a <= 2013 else "france"


def lire_stock(raw: Path) -> list[dict]:
    """Immigrés, Français de naissance, par acquisition, étrangers : 1921-2025 (2381757)."""
    f = fichier(raw, "stock")
    lignes: dict[int, dict] = {}
    for r in feuille(f, "Figure 1"):
        a = annee(r[0])
        if a and nombre(r[1]) is not None:
            lignes[a.annee] = {
                "annee": a.annee,
                "immigres": milliers(r[1]),
                "part_immigres": nombre(r[2]),
                "population": milliers(r[3]),
                "statut": a.statut,
                "rupture": a.rupture,
                "champ": champ_stock(a.annee),
                "source": "stock",
            }
    for r in feuille(f, "Figure 2"):
        a = annee(r[0])
        if a and a.annee in lignes and nombre(r[1]) is not None:
            lignes[a.annee] |= {
                "francais_naissance": milliers(r[1]),
                "francais_acquisition": milliers(r[3]),
                "etrangers": milliers(r[5]),
                "part_etrangers": nombre(r[6]),
            }
    # 1911 : seulement dans la série de 6793226 (Figure 1), même définition (immigrés).
    for r in feuille(fichier(raw, "pays_long"), "Figure 1"):
        a = annee(r[0])
        if a and a.annee not in lignes and nombre(r[1]) is not None:
            lignes[a.annee] = {
                "annee": a.annee,
                "immigres": milliers(r[1]),
                "part_immigres": nombre(r[2]),
                "population": milliers(r[3]),
                "statut": a.statut,
                "rupture": False,
                "champ": champ_stock(a.annee),
                "source": "pays_long",
            }
    return [lignes[a] for a in sorted(lignes)]


def lire_pays_long(raw: Path) -> list[dict]:
    """Immigrés par pays ou groupe de pays de naissance, 8 dates de 1968 à 2021 (6793226, Figure 2)."""
    rows = feuille(fichier(raw, "pays_long"), "Figure 2")
    entete = next(r for r in rows if annee(r[1]))
    annees = [(i, annee(v).annee) for i, v in enumerate(entete) if annee(v)]
    out = []
    for r in rows[rows.index(entete) + 1 :]:
        libelle = (r[0] or "").strip() if isinstance(r[0], str) else None
        if not libelle or all(nombre(r[i]) is None for i, _ in annees):
            if libelle and libelle.startswith(("Champ", "Source", "Lecture", "Note")):
                break
            continue
        for i, a in annees:
            out.append(
                {
                    "annee": a,
                    "pays": libelle.replace(", dont :", "").replace(" dont :", ""),
                    "immigres": milliers(r[i]),
                    "champ": champ_stock(a),
                }
            )
    return out


ENCADRES = {" Encadré Figure a": "europe", "Encadré Figure b ": "afrique", "Encadré Figure c": "asie"}


def lire_nationalites(raw: Path) -> list[dict]:
    """B2 : part des étrangers par nationalité dans la population, 1901-2020 (IP 1910, encadré).

    Parts arrondies à 0,1 point par l'Insee ; champ France métropolitaine.
    """
    out = []
    for nom, groupe in ENCADRES.items():
        rows = feuille(fichier(raw, "ip1910"), nom)
        entete = next(
            r for r in rows if r[0] is None and sum(isinstance(c, str) for c in r[1:]) >= 2
        )
        cols = [(i, str(c).strip()) for i, c in enumerate(entete) if i > 0 and c]
        for r in rows:
            a = annee(r[0])
            if not a:
                continue
            for i, nat in cols:
                v = nombre(r[i])
                if v is not None:
                    out.append(
                        {"annee": a.annee, "nationalite": nat, "groupe": groupe, "part_pct": v}
                    )
    return out
