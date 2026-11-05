"""Tableaux et figures de TeO2 ressaisis à la main (référentiels YAML) : lecture et contrôles.

Les tableaux et figures de *Trajectoires et Origines 2* (Ined Éditions, 2026) n'existent qu'en images.
Ils sont ressaisis dans `pipeline/referentiels/teo2/*.yaml`, un fichier par tableau ou figure, avec une
référence par cellule (fichier, chapitre, objet, ligne, colonne). Ce module charge ces fichiers
(`lire_teo2`) et signale les anomalies (`verifier_teo2`) : doublons, valeurs hors bornes, sommes de
pourcentages qui s'écartent de l'arrondi.

Un fichier peut porter une clé facultative `controles` (sommes attendues) :

    controles:
      - {axe: ligne, pour: [<lignes>], parmi: [<colonnes>], attendu: 100, tolerance: 1}
      - {axe: colonne, pour: [<colonnes>], parmi: [<lignes>], attendu_ligne: "<ligne totale>", tolerance: 1}

`axe: ligne` somme, pour chaque ligne de `pour`, les colonnes de `parmi` ; `axe: colonne` somme, pour
chaque colonne de `pour`, les lignes de `parmi`. Le total attendu est un nombre (`attendu`) ou la valeur
d'une autre ligne (`attendu_ligne`) ou colonne (`attendu_colonne`) du tableau. La tolérance est celle de
l'arrondi de la source (1 point par défaut).
"""

from pathlib import Path

import yaml

DOSSIER_DEFAUT = Path(__file__).resolve().parents[1] / "referentiels" / "teo2"
TOLERANCE_DEFAUT = 1.0


def _charger(chemin: Path) -> dict:
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def lire_teo2(dossier: Path = DOSSIER_DEFAUT) -> list[dict]:
    """Une ligne par cellule saisie.

    Clés : fichier, chapitre, objet, ligne, colonne, valeur, unite, approx, champ, precision.
    `unite` est celle de la cellule si elle en porte une (surcharge), sinon celle du fichier ;
    `precision` vaut None quand la valeur est lue telle quelle.
    """
    lignes: list[dict] = []
    for chemin in sorted(Path(dossier).glob("*.yaml")):
        doc = _charger(chemin)
        source = doc["source"]
        for c in doc["cellules"]:
            lignes.append(
                {
                    "fichier": chemin.name,
                    "chapitre": source["chapitre"],
                    "objet": source["objet"],
                    "ligne": c["ligne"],
                    "colonne": c["colonne"],
                    "valeur": c["valeur"],
                    "unite": c.get("unite", source["unite"]),
                    "approx": bool(c.get("approx", False)),
                    "champ": source["champ"],
                    "precision": c.get("precision"),
                }
            )
    return lignes


def _controles_du_dossier(fichiers: set[str], dossier: Path) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for nom in fichiers:
        chemin = Path(dossier) / nom
        if chemin.exists():
            out[nom] = _charger(chemin).get("controles") or []
    return out


def _verifier_somme(fichier: str, ctl: dict, cellules: dict) -> list[str]:
    anomalies = []
    axe = ctl["axe"]
    tol = ctl.get("tolerance", TOLERANCE_DEFAUT)
    for autre in ctl["pour"]:
        total, manquantes = 0.0, []
        for p in ctl["parmi"]:
            cle = (p, autre) if axe == "colonne" else (autre, p)  # (ligne, colonne)
            if cle in cellules:
                total += cellules[cle]
            else:
                manquantes.append(p)
        if manquantes:
            anomalies.append(f"{fichier} : cellule manquante pour la somme « {autre} » ({', '.join(manquantes)})")
            continue
        if "attendu" in ctl:
            attendu = ctl["attendu"]
        elif "attendu_ligne" in ctl:
            attendu = cellules.get((ctl["attendu_ligne"], autre))
        else:
            attendu = cellules.get((autre, ctl["attendu_colonne"]))
        if attendu is None:
            anomalies.append(f"{fichier} : total attendu introuvable pour « {autre} »")
        elif abs(total - attendu) > tol:
            anomalies.append(
                f"{fichier} : somme de « {autre} » = {total:g}, attendu {attendu:g} (± {tol:g}, arrondi)"
            )
    return anomalies


def verifier_teo2(
    lignes: list[dict],
    controles: dict[str, list[dict]] | None = None,
    dossier: Path = DOSSIER_DEFAUT,
) -> list[str]:
    """Anomalies détectées dans les cellules saisies (liste vide si tout est cohérent).

    Contrôles : doublons (fichier, ligne, colonne) ; valeur non numérique ; pourcentage hors de 0-100 ;
    cellule lue sur un graphique (`approx`) sans `precision` ; sommes déclarées dans `controles`
    (lues dans les YAML de `dossier` si `controles` n'est pas fourni).
    """
    anomalies: list[str] = []
    vues: dict[tuple, int] = {}
    par_fichier: dict[str, dict[tuple, float]] = {}
    for c in lignes:
        cle = (c["fichier"], c["ligne"], c["colonne"])
        vues[cle] = vues.get(cle, 0) + 1
        v = c["valeur"]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            anomalies.append(f"{c['fichier']} : valeur non numérique « {v} » ({c['ligne']} / {c['colonne']})")
            continue
        if c["unite"] == "%" and not 0 <= v <= 100:
            anomalies.append(f"{c['fichier']} : pourcentage hors de 0-100 : {v} ({c['ligne']} / {c['colonne']})")
        if c.get("approx") and not c.get("precision"):
            anomalies.append(f"{c['fichier']} : valeur approximative sans précision ({c['ligne']} / {c['colonne']})")
        par_fichier.setdefault(c["fichier"], {})[(c["ligne"], c["colonne"])] = v
    for (fichier, ligne, colonne), n in vues.items():
        if n > 1:
            anomalies.append(f"{fichier} : doublon ({ligne} / {colonne}) × {n}")
    if controles is None:
        controles = _controles_du_dossier(set(par_fichier), dossier)
    for fichier, cellules in par_fichier.items():
        for ctl in controles.get(fichier, []):
            anomalies.extend(_verifier_somme(fichier, ctl, cellules))
    return anomalies
