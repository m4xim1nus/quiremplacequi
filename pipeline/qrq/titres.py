"""Premiers titres de séjour par motif (ministère de l'Intérieur, DSED), 2011-2024.

Deux sources de la DSED, raccordées en 2015 :
- la série publiée le 27 juin 2024 (2011-2023, France, ressortissants de pays tiers hors
  Britanniques, 2023 provisoire) ; on n'en garde que 2011-2014 ;
- les fichiers annuels définitifs publiés en août 2026 (2015-2024, France, Britanniques compris).

Le raccord est contrôlé : de 2015 à 2022, total de la série + premiers titres des Britanniques
(même publication) = total du fichier annuel (`titres_raccord`, `qrq check`). Avant 2015, les
Britanniques (moins de 250 titres par an) manquent : rupture négligeable, signalée.

Le sous-motif « accord de retrait Brexit » (2020-2024) régularise des Britanniques qui vivaient déjà
en France avant le Brexit : ce ne sont pas des arrivées, le site le sépare.
"""

import csv
import io
import re
import unicodedata
from pathlib import Path

from .sources import DSED_ANNUELS, fichier

MOTIFS = {
    "economique": "economique",
    "familial": "familial",
    "etudiants": "etudiants",
    "humanitaire": "humanitaire",
    "divers": "divers",
}

# Sous-motifs : libellés des deux sources → clé commune.
SOUS_MOTIFS = {
    "salarie": "salarie",
    "scientifique": "scientifique",
    "actif_non_salarie": "actif_non_salarie",
    "artiste": "artiste",
    "saisonnier_ou_temporaire": "saisonnier_temporaire",
    "saisonnier": "saisonnier_temporaire",
    "temporaire": "saisonnier_temporaire",
    "competences_et_talents": "competences_talents",
    "famille_de_francais": "famille_de_francais",
    "membre_de_famille": "membre_de_famille",
    "liens_personnels_et_familiaux": "liens_personnels_familiaux",
    "etudiants_et_stagiaires": "etudiants",
    "total_etudiants": "etudiants",
    "refugie_et_apatride": "refugie_apatride",
    "asile_territorial_protection_subsidiaire": "protection_subsidiaire",
    "protection_subsidiaire": "protection_subsidiaire",
    "etranger_malade": "etranger_malade",
    "victime_de_la_traite_des_etres_humains": "victimes_traite_violences",
    "victime_de_violences_conjugales": "victimes_traite_violences",
    "victime_de_la_traite_des_etres_humains_et_de_violences_conjugales": "victimes_traite_violences",
    "visiteur": "visiteur",
    "etranger_entre_mineur": "entre_mineur",
    "etrangers_entres_mineurs": "entre_mineur",
    "accord_de_retrait_brexit": "accord_retrait_brexit",
    # « Autres divers » de la série = rente, ancien combattant, retraité, motifs divers.
    "autres_divers": "autres_divers",
    "rente_accident_du_travail": "autres_divers",
    "ancien_combattant": "autres_divers",
    "retraite_ou_pensionne": "autres_divers",
    "motifs_divers": "autres_divers",
}


def cle(texte: str) -> str:
    s = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"^[a-e]\.\s*|^\d+\s*-\s*", "", s.strip())
    return re.sub(r"[^a-z]+", "_", s).strip("_")


def _annuel(raw: Path, annee: int) -> dict[tuple[str, str], int]:
    """(motif, sous_motif) → titres, sous-motifs regroupés ; ('total', 'total') = total du fichier."""
    out: dict[tuple[str, str], int] = {}
    secret: dict[str, tuple[str, str]] = {}
    with open(fichier(raw, f"titres_{annee}"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m, sm = cle(r["motif_principal"]), cle(r["sous_motif"])
            if r["nb_titres"].strip() == "nc":  # non communiqué (secret statistique, petits effectifs)
                if m != "total":
                    secret[MOTIFS[m]] = (MOTIFS[m], SOUS_MOTIFS[sm])
                continue
            n = int(r["nb_titres"])
            if m == "total":
                if sm == "total":
                    out[("total", "total")] = n
                continue
            if sm == "total":
                out[(MOTIFS[m], "total")] = n
                continue
            k = (MOTIFS[m], SOUS_MOTIFS[sm])
            out[k] = out.get(k, 0) + n
    # Les cellules « nc » se déduisent du total du motif, publié : on les rend à leur sous-motif.
    for m, k in secret.items():
        reste = out[(m, "total")] - sum(n for (mm, sm), n in out.items() if mm == m and sm != "total")
        out[k] = out.get(k, 0) + reste
    return out


def lire_serie(raw: Path) -> dict[int, dict[tuple[str, str], int]]:
    """Série du 27 juin 2024 : année → (motif, sous_motif) → titres ; plus ('britanniques', 'total')."""
    texte = fichier(raw, "titres_serie").read_bytes().decode("latin-1").replace("\r", "")
    lignes = list(csv.reader(io.StringIO(texte), delimiter="\t"))
    annees: list[int] = []
    out: dict[int, dict] = {}
    motif = None
    britanniques = False
    for r in lignes:
        r = [c.strip() for c in r]
        if len(r) < 3:
            continue
        ans = [int(c[:4]) for c in r[2:] if re.fullmatch(r"20\d\d( \(\w+\))?", c)]
        if len(ans) >= 5:
            annees = ans
            continue
        if r[0] == "" and r[1] == "":
            continue
        if r[0]:
            k0 = cle(r[0])
            if k0.startswith("total_hors_britanniques"):
                motif, sm = "total", "total"
            else:
                motif = MOTIFS.get(k0, motif)
                sm = cle(r[1])
        else:
            sm = cle(r[1])
        if sm == "britanniques":
            motif, sm, britanniques = "britanniques", "total", True
        valeurs = r[2 : 2 + len(annees)]
        if not any(v.isdigit() for v in valeurs):
            continue
        if motif == "etudiants":  # un seul sous-motif, publié comme « Total »
            k = ("etudiants", "etudiants")
        else:
            k = (motif, "total" if sm == "total" else SOUS_MOTIFS[sm])
        for a, v in zip(annees, valeurs):
            if v.isdigit():
                out.setdefault(a, {})
                out[a][k] = out[a].get(k, 0) + int(v)
    assert britanniques, "série DSED : ligne des Britanniques introuvable"
    return out


REGIONS = {
    "MAGHREB": "maghreb",
    "AFRIQUE_HORS_MAGHREB": "afrique_hors_maghreb",
    "ASIE": "asie",
    "MOYEN_ORIENT": "moyen_orient",
    "EUROPE_HORS_UE27": "europe_hors_ue",
    "AMERIQUE DU NORD": "amerique_nord",
    "AMERIQUE LATINE ET CENTRALE": "amerique_latine",
    "OCEANIE": "oceanie",
    "INDETERMINE": "indetermine",
}


def _nationalites(raw: Path, annee: int) -> dict[str, int]:
    """Totaux par région du monde, total général et Britanniques (fichier annuel par nationalité)."""
    out: dict[str, int] = {}
    with open(fichier(raw, f"titres_nat_{annee}"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n = r["nb_titres"].strip()
            if r["pays_nationalite"] == "TOTAL" and n.isdigit():
                out["total" if r["region_monde_origine"] == "TOTAL" else REGIONS[r["region_monde_origine"]]] = int(n)
            elif r["code_iso3"] == "GBR":
                out["britanniques"] = int(n) if n.isdigit() else 0
    return out


def lire_titres(raw: Path) -> tuple[list[dict], list[dict]]:
    """→ (titres : année × motif × sous-motif, totaux : année → total, Britanniques, régions, et
    contrôle du raccord des deux sources)."""
    serie = lire_serie(raw)
    lignes = []
    for a in sorted(serie):
        if a >= min(DSED_ANNUELS):
            continue
        for (m, sm), n in sorted(serie[a].items()):
            if m in MOTIFS.values() and sm != "total":
                lignes.append({"annee": a, "motif": m, "sous_motif": sm, "titres": n,
                               "statut": "definitif", "source": "serie_2024_06"})
    raccord = [
        {"annee": a, "total": serie[a][("total", "total")] + serie[a][("britanniques", "total")],
         "britanniques": serie[a][("britanniques", "total")], "accord_retrait_brexit": 0}
        for a in sorted(serie) if a < min(DSED_ANNUELS)
    ]
    for a in sorted(DSED_ANNUELS):
        an = _annuel(raw, a)
        for (m, sm), n in sorted(an.items()):
            if m in MOTIFS.values() and sm != "total":
                lignes.append({"annee": a, "motif": m, "sous_motif": sm, "titres": n,
                               "statut": "definitif", "source": f"annuel_{a}"})
        s = serie.get(a)
        nat = _nationalites(raw, a)
        raccord.append({
            "annee": a,
            "total": an[("total", "total")],
            "britanniques": nat["britanniques"],
            "accord_retrait_brexit": an.get(("divers", "accord_retrait_brexit"), 0),
            **{f"region_{r}": nat.get(r, 0) for r in REGIONS.values()},
            "total_nationalites": nat["total"],
            "somme_motifs_annuel": sum(n for (m, sm), n in an.items() if m in MOTIFS.values() and sm == "total"),
            "somme_sous_motifs_annuel": sum(n for (m, sm), n in an.items() if m in MOTIFS.values() and sm != "total"),
            "serie_hors_britanniques": s[("total", "total")] if s else None,
            "serie_britanniques": s[("britanniques", "total")] if s else None,
            "serie_statut": None if not s else ("provisoire" if a == max(serie) else "definitif"),
        })
    return lignes, raccord
