"""Fécondité (page « Les naissances ») : lue telle que publiée, rien n'est calculé ici.

Trois niveaux à ne jamais mêler :
- les naissances d'une année (état civil, naissances.py) ;
- l'indicateur conjoncturel de fécondité (ICF) d'une année : somme des taux par âge, nombre
  d'enfants d'une génération fictive qui connaîtrait toute sa vie les taux de l'année ;
- la descendance finale d'une génération réelle : nombre moyen d'enfants qu'elle a eus.

Sources :
- Insee Première 1939 (2023) : ICF ajusté des femmes nées à l'étranger (2006-2021, figure 6),
  descendance finale selon le lien à la migration (TeO2, générations 1960-1974, figures 1, 3, 4),
  par génération (TeO1 et TeO2, figure 2a), calendrier des naissances autour de l'arrivée (figure 5) ;
- bilan démographique 2025 : ICF et taux de reproduction de la France et de la métropole
  (1901-2025), descendance par génération (métropole) ;
- référentiels saisis (onu2000.yaml, fecondite.yaml), vérifiés contre leurs PDF.

L'ICF de l'état civil porte sur les femmes nées à l'étranger (on ne connaît pas leur nationalité
de naissance) ; la descendance finale de TeO, sur les immigrées.
"""

import re
import shutil
import subprocess
from pathlib import Path

import yaml

from .lecture import annee, feuille, nombre, texte
from .sources import fichier

REFERENTIELS = Path(__file__).resolve().parents[1] / "referentiels"

# Libellés de l'Insee → identifiants (figure 6 de l'IP 1939).
GROUPES_ICF = {
    "Ensemble des femmes": "ensemble",
    "Femmes nées en France": "nees_en_france",
    "Femmes nées à l’étranger, dont :": "nees_a_l_etranger",
    "Italie, Espagne, Portugal": "europe_du_sud",
    "Autres pays d’Europe": "autres_europe",
    "Algérie, Maroc, Tunisie": "maghreb",
    "Autres pays d’Afrique": "autres_afrique",
    "Turquie, Moyen-Orient": "turquie_moyen_orient",
    "Autres pays d’Asie": "autres_asie",
    "Amérique, Océanie": "amerique_oceanie",
}
LIENS = {
    "Immigrées": "immigrees",
    "Arrivées avant 15 ans": "arrivees_avant_15_ans",
    "Arrivées à 15 ans ou plus": "arrivees_15_ans_ou_plus",
    "Descendantes d’immigrés": "descendantes",
    "Avec deux parents immigrés": "descendantes_deux_parents",
    "Avec un seul parent immigré": "descendantes_un_parent",
    "Ni immigrées ni descendantes d’immigrés": "ni_immigrees_ni_descendantes",
    "Ensemble des femmes": "ensemble",
}
PAYS_TEO = {
    "Italie, Espagne, Portugal": "europe_du_sud",
    "Autres pays d’Europe": "autres_europe",
    "Algérie, Maroc, Tunisie": "maghreb",
    "Autres pays d’Afrique": "autres_afrique",
    "Turquie, Moyen-Orient": "turquie_moyen_orient",
    "Autres pays d’Asie": "autres_asie",
    "Amérique, Océanie": "amerique_oceanie",
    "Ensemble": "immigrees",
}
DIPLOMES = ["sans_diplome_ou_inferieur_au_bac", "bac", "superieur_au_bac"]


def _ip1939(raw: Path, nom: str) -> list[tuple]:
    return feuille(fichier(raw, "fecondite_ip1939"), nom)


def lire_icf_origine(raw: Path) -> list[dict]:
    """ICF ajusté selon le pays de naissance (France, 2006-2021), deux décimales comme publié."""
    rows = _ip1939(raw, "Figure 6")
    entete = next(r for r in rows if annee(r[1]))
    annees = [(i, annee(v).annee) for i, v in enumerate(entete) if annee(v)]
    out = []
    for r in rows:
        g = GROUPES_ICF.get(texte(r[0]))
        if g is None:
            continue
        for i, a in annees:
            out.append({"annee": a, "groupe": g, "icf": round(nombre(r[i]), 2)})
    assert len({o["groupe"] for o in out}) == len(GROUPES_ICF), "IP 1939 figure 6 : groupe manquant"
    return out


def lire_descendance_teo(raw: Path) -> list[dict]:
    """Descendance finale (TeO) : lien à la migration, génération, pays de naissance, diplôme."""
    out = []
    for r in _ip1939(raw, "Figure 1"):
        c = LIENS.get(texte(r[0]))
        if c and nombre(r[1]) is not None:
            out.append({"dimension": "lien", "categorie": c, "groupe": "", "valeur": nombre(r[1]),
                        "generations": "1960-1974", "enquete": "TeO2"})
    for r in _ip1939(raw, "Figure 2a"):
        g = texte(r[0])
        if re.fullmatch(r"19\d\d-19\d\d", g):
            for j, groupe in ((1, "immigrees"), (2, "non_immigrees")):
                out.append({"dimension": "generation", "categorie": g, "groupe": groupe,
                            "valeur": nombre(r[j]), "generations": g,
                            "enquete": "TeO1" if int(g[:4]) < 1960 else "TeO2"})
    for r in _ip1939(raw, "Figure 3"):
        c = PAYS_TEO.get(texte(r[0]))
        if c and nombre(r[1]) is not None:
            out.append({"dimension": "pays", "categorie": c, "groupe": "immigrees", "valeur": nombre(r[1]),
                        "generations": "1960-1974", "enquete": "TeO2"})
    for r in _ip1939(raw, "Figure 4"):
        lien = {"Immigrées": "immigrees", "Descendantes d’immigrés": "descendantes",
                "Ni immigrées ni descendantes d’immigrés": "ni_immigrees_ni_descendantes"}.get(texte(r[0]))
        if lien:
            for j, d in enumerate(DIPLOMES, start=1):
                out.append({"dimension": "diplome", "categorie": d, "groupe": lien, "valeur": nombre(r[j]),
                            "generations": "1960-1974", "enquete": "TeO2"})
    attendus = {"lien": 8, "generation": 10, "pays": 8, "diplome": 9}
    for dim, n in attendus.items():
        assert sum(o["dimension"] == dim for o in out) == n, f"IP 1939 : {dim} incomplet"
    return out


def lire_calendrier_arrivee(raw: Path) -> list[dict]:
    """Naissances des immigrées (générations 1960-1974) selon l'année écoulée depuis leur première
    entrée en France, en France ou à l'étranger (% de toutes leurs naissances)."""
    out = []
    for r in _ip1939(raw, "Figure 5"):
        if isinstance(r[0], (int, float)) or re.fullmatch(r"-?\d+", texte(r[0])):
            out.append({"duree": int(nombre(r[0])), "en_france": nombre(r[1]), "a_l_etranger": nombre(r[2])})
    assert out[0]["duree"] < 0 < out[-1]["duree"], "IP 1939 figure 5 : durées"
    return out


def lire_nationale(raw: Path) -> list[dict]:
    """ICF, âge moyen à l'accouchement et taux de reproduction (pour 100 femmes → par femme pour
    l'ICF), métropole depuis 1901 et France depuis 1994, tels que publiés."""
    icf = feuille(fichier(raw, "icf"), "ICF-âge moyen-mères")
    rep = feuille(fichier(raw, "reproduction"), "Taux-reproduction")
    trn = {}
    for r in rep:
        a = annee(r[0])
        if a:
            trn[(a.annee, "metropole")] = (nombre(r[1]), nombre(r[2]))
            trn[(a.annee, "france")] = (nombre(r[3]), nombre(r[4]))
    out = []
    for r in icf:
        a = annee(r[0])
        if not a:
            continue
        for champ, j in (("metropole", 1), ("france", 3)):
            v = nombre(r[j])
            if v is None:
                continue
            brut, net = trn[(a.annee, champ)]
            out.append({
                "annee": a.annee, "champ": champ, "statut": a.statut,
                "icf": round(v / 100, 2), "age_moyen": nombre(r[j + 1]),
                "taux_reproduction_brut": brut, "taux_reproduction_net": net,
            })
    return out


def lire_descendance_nationale(raw: Path) -> list[dict]:
    """Descendance finale (à 50 ans) des générations de femmes, France métropolitaine, par femme."""
    rows = feuille(fichier(raw, "descendance"), "FM")
    entete = next(r for r in rows if texte(r[1]) == "15 ans")
    c50 = next(i for i, v in enumerate(entete) if texte(v) == "50 ans")
    return [
        {"generation": int(r[0]), "descendance": round(nombre(r[c50]) / 100, 3)}
        for r in rows
        if isinstance(r[0], (int, float)) and nombre(r[c50]) is not None
    ]


# Référentiels saisis : vérification contre les PDF. -----------------------------------------------

def _norme(s: str) -> str:
    return re.sub(r"\s+", "", s.replace("’", "'").replace(" ", " ").replace(" ", " "))


def _page(pdf: Path, n: int) -> str:
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext (poppler) est nécessaire pour vérifier les référentiels saisis")
    # Avec la mise en page (tableaux) puis sans (texte en colonnes) : l'extrait doit être dans l'un.
    return "\n".join(
        subprocess.run(["pdftotext", *opt, "-f", str(n), "-l", str(n), str(pdf), "-"],
                       capture_output=True, text=True, check=True).stdout
        for opt in (["-layout"], [])
    )


def _en_texte(v: float) -> list[str]:
    """Écritures possibles d'une valeur dans un extrait (espaces déjà retirés)."""
    if float(v).is_integer():
        n = int(v)
        return [str(n), f"{n:,}"]
    return [str(v), str(v).replace(".", ",")]


def _verifier_extrait(pdf: Path, page: int, extrait: str, valeurs: list[float], ou: str) -> None:
    if _norme(extrait) not in _norme(_page(pdf, page)):
        raise ValueError(f"{ou} : extrait introuvable page {page} du PDF : {extrait!r}")
    reste = _norme(extrait)
    for v in valeurs:  # dans l'ordre de l'extrait
        pos = min((p for p in (reste.find(t) for t in _en_texte(v)) if p >= 0), default=-1)
        if pos < 0:
            raise ValueError(f"{ou} : valeur {v} absente de l'extrait {extrait!r}")
        reste = reste[pos + 1 :]


def lire_onu2000(raw: Path) -> list[dict]:
    ref = yaml.safe_load((REFERENTIELS / "onu2000.yaml").read_text())
    pdf = fichier(raw, ref["source"]["cle"])
    out = []
    for l in ref["lignes"]:
        _verifier_extrait(pdf, l["page_pdf"], l["extrait"], list(l["valeurs"].values()), f"onu2000 {l['indicateur']}")
        for sc, v in l["valeurs"].items():
            out.append({"indicateur": l["indicateur"], "scenario": sc, "valeur": v, "unite": l["unite"],
                        "libelle": l["libelle"], "tableau": l["tableau"], "page": l["page"]})
    for c in ref["citations"]:
        _verifier_extrait(pdf, c["page_pdf"], c["texte"], [], f"onu2000 citation {c['cle']}")
    return out


def lire_textes_ip1939(raw: Path) -> list[dict]:
    ref = yaml.safe_load((REFERENTIELS / "fecondite.yaml").read_text())
    pdf = fichier(raw, ref["source"]["cle"])
    out = []
    for v in ref["valeurs"]:
        _verifier_extrait(pdf, v["page"], v["extrait"], [v["valeur"]], f"fecondite {v['cle']}")
        out.append({k: v[k] for k in ("cle", "libelle", "valeur", "unite", "page")})
    return out
