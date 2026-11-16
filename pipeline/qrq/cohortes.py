"""Modèle de cohortes des générations liées à l'immigration, 1911-2025 (docs/PISCINE.md §6).

Ce que la statistique publique n'observe pas année par année (les enfants et petits-enfants
d'immigrés, par âge), le modèle le reconstruit, calé sur ce qu'elle observe. Paramètres et statut
dans referentiels/cohortes.yaml ; tous les écarts aux cibles sont exportés et contrôlés.

État au 1er janvier, par âge révolu (0 à 105 ans et plus) :
- G1  : immigrés (nés étrangers à l'étranger) ;
- G2a : nés en France de deux parents immigrés ;
- G2b : nés en France d'un seul parent immigré ;
- G3  : nés en France de deux parents non immigrés dont au moins un est G2.
Le reste de la population (« autres ») est le complément de la population totale du bilan.

Dynamique (année t → t+1) :
1. Mortalité : quotients nationaux par âge (moyenne hommes-femmes), sans hypothèse de
   surmortalité par origine.
2. G1 : le stock est forcé sur la série des recensements (interpolée) ; le flux net d'une année
   s'en déduit, réparti par âge selon le profil d'âge à l'arrivée (IP 2107, entrées 2024). Un flux
   net négatif retire des immigrés au prorata du stock des 15-79 ans.
3. Naissances : part des naissances de deux parents immigrés (G2a) et d'un seul (G2b) observée de
   1998 à 2025 (pays de naissance des parents, corrigé de la part des immigrés parmi les personnes
   nées à l'étranger) ; avant 1998, proportionnelle à la part des immigrés parmi les 20-44 ans
   (coefficients ajustés sur 1998-2025). G3 : parmi les naissances sans parent immigré, part
   proportionnelle à la part des G2 parmi les 20-44 ans non immigrés (coefficient calé sur IP 1910).
4. Ni les G2 ni les G3 n'émigrent (hypothèse, U19).
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import openpyxl

from .lecture import annee, feuille, milliers, nombre, texte
from .sources import fichier

AGES = 106  # 0 … 104, 105 ou plus
GROUPES = ("G1", "G2a", "G2b", "G3")
TRANCHES = [(a, a + 4) for a in range(0, 100, 5)] + [(100, 105)]


# --- Lecture -------------------------------------------------------------------------------------


def lire_ages(raw: Path) -> dict[int, np.ndarray]:
    """Population au 1er janvier par âge (0 à 105+). France quand disponible, sinon métropole."""
    wb = openpyxl.load_workbook(fichier(raw, "ages"), data_only=True, read_only=True)
    out = {}
    try:
        for nom in wb.sheetnames:
            if not nom.strip().isdigit():
                continue
            a = int(nom.strip())
            v = np.zeros(AGES)
            vu = False
            for r in wb[nom].iter_rows(values_only=True):
                age = texte(r[1]).replace("ou plus", "").strip() if len(r) > 1 else ""
                if not age.isdigit():
                    continue
                fr = nombre(r[5]) if len(r) > 5 else None
                x = fr if (a >= 1990 and fr is not None) else nombre(r[2])
                if x is not None:
                    v[min(int(age), AGES - 1)] += x
                    vu = True
            if vu:
                out[a] = v
    finally:
        wb.close()
    return out


def lire_quotients(raw: Path) -> dict[int, np.ndarray]:
    """Quotients de mortalité par âge (probabilité), moyenne des hommes et des femmes."""
    par_sexe: dict[str, dict[int, np.ndarray]] = {"F": {}, "H": {}}
    for nom in ("FM-Femmes-Histo", "FM-Hommes-Histo", "FM-Femmes", "FM-Hommes"):
        sexe = "F" if "Femmes" in nom else "H"
        for r in feuille(fichier(raw, "mortalite"), nom):
            a = annee(r[0])
            if not a:
                continue
            q = [nombre(x) for x in r[1:102]]
            q = [x for x in q if x is not None]
            if len(q) >= 100:
                v = np.array(q[:101]) / 100_000
                # 101 à 105+ : on prolonge le dernier quotient.
                par_sexe[sexe][a.annee] = np.concatenate([v, np.full(AGES - 101, v[-1])])
    return {a: (par_sexe["F"][a] + par_sexe["H"][a]) / 2 for a in par_sexe["F"] if a in par_sexe["H"]}


def lire_part_immigres_nes_etranger(raw: Path) -> dict[int, float]:
    """Part des immigrés parmi les personnes nées à l'étranger (2006-2025, 2865118)."""
    rows = feuille(fichier(raw, "nes_etranger"), "Données")
    entete = next(r for r in rows if annee(r[1]))
    # Colonnes par paires (effectif, proportion) : seules les colonnes impaires portent une année.
    # L'en-tête publié contient des étiquettes parasites dans les colonnes paires (« 2014 (p) »,
    # « 1994 (p) »…, fichier du 22/06/2026) : on les ignore.
    cols = [(i, annee(v).annee) for i, v in enumerate(entete) if i % 2 == 1 and annee(v)]
    lignes = {texte(r[0]): r for r in rows if r[0]}
    nes = lignes["Nés à l'étranger"]
    imm = lignes["Ensemble des immigrés"]
    return {a: nombre(imm[i]) / nombre(nes[i]) for i, a in cols if nombre(nes[i])}


def lire_profil_arrivee(raw: Path) -> list[tuple[float, float]]:
    """Points (âge, part cumulée) de l'âge à l'arrivée des immigrés entrés en 2024 (IP 2107)."""
    f3 = {texte(r[0]): r for r in feuille(fichier(raw, "flux"), "Figure 3") if r[0]}
    tc2 = {texte(r[0]): r for r in feuille(fichier(raw, "flux"), "Tableau complémentaire 2") if r[0]}
    e = f3["Ensemble des immigrés"]
    total, q1, med, q3 = nombre(e[1]), nombre(e[3]), nombre(e[4]), nombre(e[5])
    t = tc2["Ensemble des immigrés"]
    plus25, plus15 = nombre(t[1]), nombre(t[4])
    pts = {0: 0.0, 15: 1 - plus15 / total, q1: 0.25, 25: 1 - plus25 / total, med: 0.5, q3: 0.75, 75: 1.0}
    return sorted(pts.items())


def profil_par_age(points: list[tuple[float, float]]) -> np.ndarray:
    """Densité par âge révolu à partir d'une fonction de répartition linéaire par morceaux."""
    ages, cum = zip(*points)
    bornes = np.interp(np.arange(AGES + 1), ages, cum)
    d = np.diff(bornes)
    return d / d.sum()


def lire_cibles_ip1910(raw: Path) -> list[dict]:
    """Parts de G1, G2 (deux parents, un parent), G3 par classe d'âge en 2019-2020 (IP 1910, fig. 1)."""
    out = []
    for r in feuille(fichier(raw, "ip1910"), "Figure 1"):
        c = texte(r[0])
        if not c or not (c[0].isdigit()):
            continue
        out.append(
            {
                "classe": c,
                "G1": nombre(r[1]),
                "G2a": nombre(r[2]),
                "G2b": nombre(r[3]),
                "G3": None if nombre(r[4]) is None else nombre(r[4]) + nombre(r[5]),
            }
        )
    return out


CLASSES_RP = {"0-14": (0, 15), "15-24": (15, 25), "25-54": (25, 55), "55 ou plus": (55, AGES)}


def lire_ages_immigres(raw: Path) -> dict[int, dict[str, float]]:
    """Répartition des immigrés par grande classe d'âge, en % (recensements 1990-2025, 2381759).
    Tous logements, contrairement à IP 1910 (logement ordinaire)."""
    rows = feuille(fichier(raw, "ages_immigres"), "Données")
    entete = next(r for r in rows if annee(r[1]))
    # Colonnes par paires (immigrés, étrangers) : l'année est sur la colonne des immigrés.
    cols = [(i, annee(v).annee) for i, v in enumerate(entete) if annee(v)]
    lignes = {texte(r[0]): r for r in rows if r[0]}
    noms = dict(zip(CLASSES_RP, ("Moins de 15 ans", "15 à 24 ans", "25 à 54 ans", "55 ans ou plus")))
    return {a: {c: nombre(lignes[n][i]) for c, n in noms.items()} for i, a in cols}


def lire_descendants_2025(raw: Path) -> dict:
    """Descendants d'immigrés en 2025 (enquête Emploi) : effectif et part à un seul parent immigré."""
    for r in feuille(fichier(raw, "descendants"), "Données"):
        if texte(r[0]).lower().startswith("ensemble"):
            return {"effectif": milliers(r[1]), "part_un_parent": nombre(r[3])}
    raise ValueError("ligne Ensemble introuvable (descendants 2025)")


# --- Modèle --------------------------------------------------------------------------------------


def bornes_classe(c: str) -> tuple[int, int]:
    c = c.replace(" ou plus", "-105")
    a, b = c.split("-")
    return int(a), int(b)


def interp_annees(points: dict[int, float], a: int) -> float:
    xs = sorted(points)
    return float(np.interp(a, xs, [points[x] for x in xs]))


@dataclass
class Entrees:
    ages: dict[int, np.ndarray]
    quotients: dict[int, np.ndarray]
    stock_g1: dict[int, float]  # immigrés au 1er janvier (recensements, puis annuel)
    naissances: dict[int, float]  # naissances de l'année (bilan, même champ que la piscine)
    parts_naissances: dict[int, tuple[float, float]]  # (deux parents nés à l'étranger, un seul)
    part_imm_nes_etranger: dict[int, float]
    profil: np.ndarray


def _vecteur(d: dict[int, np.ndarray], a: int) -> np.ndarray:
    if a in d:
        return d[a]
    xs = sorted(d)
    avant = max((x for x in xs if x < a), default=xs[0])
    apres = min((x for x in xs if x > a), default=xs[-1])
    if avant == apres:
        return d[avant]
    t = (a - avant) / (apres - avant)
    return d[avant] + t * (d[apres] - d[avant])


def forme_departs(p: dict) -> np.ndarray:
    """Profil par âge des départs d'immigrés (relatif) : referentiels/cohortes.yaml."""
    v = np.ones(AGES)
    for seg in p["departs"]["forme"]:
        v[seg["de"] : seg["a"] + 1] = seg["poids"]
    return v


def parts_cohortes(cibles: list[dict]) -> dict[int, dict[str, float]]:
    """Composition des naissances par année, déduite de la photo 2019-2020 (IP 1910, fig. 1).

    Une classe d'âge a0-a1 au 1er janvier 2020 est née de 2019 − a1 à 2019 − a0. Parmi les
    personnes nées en France (non immigrées), la part de G2 et de G3 donne la composition des
    naissances de ces années, sous l'hypothèse d'une survie et d'une émigration identiques à
    celles des autres non-immigrés (U19).
    """
    out: dict[int, dict[str, float]] = {}
    for c in cibles:
        if c["classe"] in ("0-17", "18-59", "0-59", "60 ou plus") or c["G1"] is None:
            continue
        a0, a1 = bornes_classe(c["classe"])
        nes_ici = 100 - c["G1"]
        parts = {g: (c[g] / nes_ici if c[g] is not None else None) for g in ("G2a", "G2b", "G3")}
        for y in range(2019 - a1, 2019 - a0 + 1):
            out[y] = parts
    return out


def simuler(e: Entrees, p: dict, cohortes: dict[int, dict[str, float]], seul_g1: bool = False) -> dict:
    debut, fin = p["debut"], p["fin"]
    adultes = slice(20, 45)
    n = {g: np.zeros(AGES) for g in GROUPES}
    np_ = p["naissances"]
    c2, c1 = np_["correction_deux"] or 1.0, np_["correction_un"] or 1.0
    beta_ancien, beta_recent = np_["beta_ancien"] or 0.0, np_["beta_recent"] or 0.0
    mu = p["departs"]["taux"] * forme_departs(p)
    premiere_ip = min(cohortes)

    # Conditions initiales (1911) : faible effet sur les cibles (docs/PISCINE.md §6).
    pop0 = _vecteur(e.ages, debut)
    g1_0 = interp_annees(e.stock_g1, debut)
    forme_g1 = pop0 * (np.arange(AGES) >= 15)
    n["G1"] = g1_0 * forme_g1 / forme_g1.sum()
    forme_g2 = pop0 * (np.arange(AGES) < 60)
    g2_0 = p["initial"]["g2_rapport_g1"] * g1_0
    n["G2a"] = 0.5 * g2_0 * forme_g2 / forme_g2.sum()
    n["G2b"] = 0.5 * g2_0 * forme_g2 / forme_g2.sum()

    annees = []
    for t in range(debut, fin + 1):
        pop = _vecteur(e.ages, t)
        a_tot = pop[adultes].sum()
        g1_ad = n["G1"][adultes].sum()
        g2_ad = n["G2a"][adultes].sum() + n["G2b"][adultes].sum()
        h = g2_ad / max(1.0, a_tot - g1_ad)
        etat = {g: n[g].copy() for g in GROUPES}
        ligne = {"annee": t, **{g: float(etat[g].sum()) for g in GROUPES}, "part_g2_adultes": h}
        if t == fin:
            annees.append(ligne | {"etat": etat})
            break

        # Composition des naissances de l'année t.
        b = e.naissances[t]
        if t in e.parts_naissances:
            r2, r1 = e.parts_naissances[t]
            p2, p1 = r2 * c2, r1 * c1
            regime = "etat_civil"
        else:
            k = cohortes.get(t, cohortes[premiere_ip])
            p2, p1 = k["G2a"], k["G2b"]
            regime = "ip1910" if t in cohortes else "ip1910_extrapole"
        k = cohortes.get(t)
        if k and k["G3"] is not None:
            p3 = k["G3"]
        else:
            beta = beta_recent if t > max(cohortes) else beta_ancien
            p3 = min(1.0, beta * h) * (1 - p1 - p2)
        nais = {"G2a": b * p2, "G2b": b * p1, "G3": b * p3}

        # Vieillissement, mortalité, départs d'immigrés.
        q = _vecteur(e.quotients, t)
        deces, departs = {}, 0.0
        for g in GROUPES:
            if seul_g1 and g != "G1":
                continue
            sortie = q + (mu * (1 - q) if g == "G1" else 0)
            deces[g] = float((n[g] * q).sum())
            if g == "G1":
                departs = float((n[g] * (1 - q) * mu).sum())
            survivants = n[g] * (1 - sortie)
            nouveau = np.zeros(AGES)
            nouveau[1:] = survivants[:-1]
            nouveau[-1] += survivants[-1]
            if g in nais:
                nouveau[0] = nais[g] * (1 - q[0] / 2)
                deces[g] += nais[g] * q[0] / 2
            n[g] = nouveau

        # Arrivées d'immigrés : ce qu'il faut pour retomber sur le stock observé suivant.
        cible = interp_annees(e.stock_g1, t + 1)
        arrivees = cible - n["G1"].sum()
        if arrivees >= 0:
            n["G1"] += arrivees * e.profil
        else:
            poids = n["G1"] * ((np.arange(AGES) >= 15) & (np.arange(AGES) < 80))
            n["G1"] += arrivees * poids / poids.sum()
            departs -= arrivees
            arrivees = 0.0

        ligne |= {
            "naissances": b,
            "regime_naissances": regime,
            **{f"naissances_{g}": v for g, v in nais.items()},
            **{f"deces_{g}": v for g, v in deces.items()},
            "arrivees_G1": arrivees,
            "departs_G1": departs,
        }
        annees.append(ligne | {"etat": etat})
    return {"annees": annees}


def parts_par_classe(etat: dict[str, np.ndarray], pop: np.ndarray, classe: str) -> dict[str, float]:
    a, b = bornes_classe(classe)
    s = slice(a, b + 1)
    return {g: 100 * float(etat[g][s].sum() / pop[s].sum()) for g in GROUPES}


def _bissection(f, lo: float, hi: float, n: int = 40) -> float:
    """Racine de f croissante sur [lo, hi]."""
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def caler(e: Entrees, p: dict, cibles: list[dict], sorties_insee: dict[int, float]) -> tuple[dict, dict]:
    """Cale, dans l'ordre : le taux de départ des immigrés (sorties Insee), la correction des
    naissances par pays de naissance des parents (G2 des 0-17 ans en 2020), et les coefficients
    G3 hors de la photo de 2019-2020. Renvoie la simulation et les valeurs calées."""
    p = {**p, "naissances": dict(p["naissances"]), "departs": dict(p["departs"])}
    coh = parts_cohortes(cibles)
    an_ip = p["calage"]["annee_ip1910"]
    periode = range(*p["calage"]["sorties"])  # années de sorties Insee utilisées

    def ecart_sorties(taux: float) -> float:
        p["departs"]["taux"] = taux
        sim = {a["annee"]: a for a in simuler(e, p, coh, seul_g1=True)["annees"]}
        return float(np.mean([sim[t]["departs_G1"] for t in periode]) - np.mean([sorties_insee[t] for t in periode]))

    p["departs"]["taux"] = _bissection(ecart_sorties, 0.0, 0.1)

    cible = next(x for x in cibles if x["classe"] == "0-17")
    pop = _vecteur(e.ages, an_ip)

    def ecart(cle: str, groupe: str):
        def f(cor: float) -> float:
            p["naissances"][cle] = cor
            sim = {a["annee"]: a for a in simuler(e, p, coh)["annees"]}
            return parts_par_classe(sim[an_ip]["etat"], pop, "0-17")[groupe] - cible[groupe]
        return f

    # Les naissances G2a ne dépendent que de correction_deux, les G2b que de correction_un.
    p["naissances"]["correction_deux"] = _bissection(ecart("correction_deux", "G2a"), 0.2, 1.5)
    p["naissances"]["correction_un"] = _bissection(ecart("correction_un", "G2b"), 0.2, 1.5)

    # G3 hors photo : beta tel que beta × h reproduise la part observée aux bords de la photo.
    sim = {a["annee"]: a for a in simuler(e, p, coh)["annees"]}
    def beta(annees: range) -> float:
        vals = []
        for y in annees:
            k = coh[y]
            vals.append(k["G3"] / ((1 - k["G2a"] - k["G2b"]) * sim[y]["part_g2_adultes"]))
        return float(np.mean(vals))

    g3_annees = sorted(y for y, k in coh.items() if k["G3"] is not None)
    p["naissances"]["beta_ancien"] = beta(range(g3_annees[0], g3_annees[0] + 5))
    p["naissances"]["beta_recent"] = beta(range(g3_annees[-1] - 4, g3_annees[-1] + 1))
    sim = simuler(e, p, coh)
    cal = {
        "taux_departs": p["departs"]["taux"],
        "correction_deux": p["naissances"]["correction_deux"],
        "correction_un": p["naissances"]["correction_un"],
        "beta_ancien": p["naissances"]["beta_ancien"],
        "beta_recent": p["naissances"]["beta_recent"],
    }
    return sim, cal


def preparer(raw: Path, stock: list[dict], bilan: list[dict], naissances: list[dict], p: dict) -> Entrees:
    bascule = p["bilan_metropole_jusqua"]
    nb = {}
    for b in bilan:
        if (b["onglet"] == "FM" and b["annee"] <= bascule) or (b["onglet"] == "FR" and b["annee"] > bascule):
            if b["naissances"] is not None:
                nb[b["annee"]] = float(b["naissances"])
    parts = {}
    par = {}
    for x in naissances:
        par.setdefault(x["annee"], {})[x["categorie"]] = x["naissances"]
    for a, d in par.items():
        parts[a] = (d["deux_parents_nes_a_l_etranger"] / d["ensemble"], d["un_parent_ne_a_l_etranger"] / d["ensemble"])
    return Entrees(
        ages=lire_ages(raw),
        quotients=lire_quotients(raw),
        stock_g1={s["annee"]: float(s["immigres"]) for s in stock},
        naissances=nb,
        parts_naissances=parts,
        part_imm_nes_etranger=lire_part_immigres_nes_etranger(raw),
        profil=profil_par_age(lire_profil_arrivee(raw)),
    )


def ecarts_calage(sim: dict, e: Entrees, cibles: list[dict], flux: list[dict], raw: Path) -> list[dict]:
    """Écarts du modèle à ses cibles et à ses témoins indépendants (exportés et contrôlés)."""
    an = {a["annee"]: a for a in sim["annees"]}
    out = []
    ip = 2020
    pop = _vecteur(e.ages, ip)
    for c in cibles:
        m = parts_par_classe(an[ip]["etat"], pop, c["classe"])
        for g in GROUPES:
            if c[g] is not None:
                out.append({"temoin": "ip1910_2020", "groupe": g, "cle": c["classe"], "modele": round(m[g], 2), "observe": c[g], "unite": "%"})
    d = lire_descendants_2025(raw)
    g2 = an[2025]["G2a"] + an[2025]["G2b"]
    out.append({"temoin": "descendants_2025", "groupe": "G2", "cle": "effectif", "modele": round(g2), "observe": d["effectif"], "unite": "personnes"})
    out.append({"temoin": "descendants_2025", "groupe": "G2b", "cle": "part_un_parent", "modele": round(100 * an[2025]["G2b"] / g2, 1), "observe": d["part_un_parent"], "unite": "%"})
    # Âges des immigrés au recensement (tous logements) : témoin de la forme par âge des G1.
    for t, parts in lire_ages_immigres(raw).items():
        if t in an:
            g1 = an[t]["etat"]["G1"]
            for c, (a, b) in CLASSES_RP.items():
                out.append({"temoin": "rp_ages_g1", "groupe": "G1", "cle": f"{t} {c}", "modele": round(100 * float(g1[a:b].sum() / g1.sum()), 2), "observe": parts[c], "unite": "%"})
    for f in flux:
        t = f["annee"]
        if f["deces_imm"] is not None and t in an and "deces_G1" in an[t]:
            out.append({"temoin": "deces_immigres_insee", "groupe": "G1", "cle": str(t), "modele": round(an[t]["deces_G1"]), "observe": f["deces_imm"], "unite": "personnes"})
    return out


def tranches(v: np.ndarray) -> list[int]:
    return [round(float(v[a : b + 1].sum())) for a, b in TRANCHES]


__all__ = ["simuler", "caler", "preparer", "lire_cibles_ip1910", "lire_descendants_2025"]
