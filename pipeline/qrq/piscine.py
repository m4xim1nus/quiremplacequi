"""La piscine v0 : la population en deux teintes (immigrés, non-immigrés) et ses quatre vannes.

docs/PISCINE.md §6 et §8 ; paramètres dans referentiels/piscine.yaml. Une ligne par année `a` :
les stocks au 1er janvier de `a`, et les flux de l'année `a` (du 1er janvier `a` au 1er janvier
`a + 1`). Trois régimes, toujours affichés :

- `mesure` (2006-2022) : entrées, sorties et décès d'immigrés publiés par l'Insee (IP 2107) ;
- `partiel` (2023-2024) : entrées publiées, sorties pas encore (U3) ; décès d'immigrés estimés ;
- `reconstruit` (avant 2006) : stocks des recensements interpolés, décès estimés, **flux net**
  par différence ; arrivées et départs ne sont pas séparables (U17).

Identité tenue à chaque année, par construction (et testée) :

    immigres(a+1) = immigres(a) + entrees − sorties − deces_imm + ajust_imm + non_ventile_imm

où `net_imm` remplace `entrees − sorties` avant 2006. `ajust_*` porte les changements de champ et
l'effet de collecte de 2024 (jamais comptés comme des arrivées) ; `non_ventile_*` ce que les sources
ne permettent pas encore d'attribuer (sorties non publiées, arrondis).
"""

from statistics import mean


def interpoler(points: dict[int, int], a: int) -> float:
    """Interpolation linéaire entre les deux recensements qui encadrent `a`."""
    if a in points:
        return float(points[a])
    avant = max(x for x in points if x < a)
    apres = min(x for x in points if x > a)
    t = (a - avant) / (apres - avant)
    return points[avant] + t * (points[apres] - points[avant])


def ratio_deces(deces_imm: float, deces: float, immigres: float, population: float) -> float:
    """Rapport entre la part des immigrés dans les décès et leur part dans la population."""
    return (deces_imm / deces) / (immigres / population)


def construire(stock: list[dict], bilan: list[dict], flux: list[dict], params: dict) -> dict:
    debut, fin = params["debut"], params["fin"]
    bascule = params["bilan_metropole_jusqua"]
    recensements = params["recensements"]
    collecte_2024 = params["saisies"]["effet_collecte_2024_immigres"]["valeur"]

    st = {s["annee"]: s for s in stock}
    bil = {(b["annee"], b["onglet"]): b for b in bilan}
    fx = {f["annee"]: f for f in flux}

    def b(a: int) -> dict:
        return bil[(a, "FM" if a <= bascule else "FR")]

    points = {a: st[a]["immigres"] for a in recensements}

    def immigres(a: int) -> int:
        if a >= 2006:
            return st[a]["immigres"]
        return round(interpoler(points, a))

    def statut_stock(a: int) -> str:
        if a < 2006:
            return "recensement" if a in points else "interpole"
        return st[a]["statut"]  # « definitif » ou « provisoire »

    # Calage du rapport des décès sur les années mesurées.
    calage = range(params["deces_immigres"]["calage"][0], params["deces_immigres"]["calage"][1] + 1)
    ratios = {
        a: ratio_deces(fx[a]["deces_imm"], b(a)["deces"], immigres(a), b(a)["population"])
        for a in calage
    }
    r_moy, r_min, r_max = mean(ratios.values()), min(ratios.values()), max(ratios.values())

    annees = []
    for a in range(debut, fin + 1):
        pop, imm = b(a)["population"], immigres(a)
        ligne = {
            "annee": a,
            "population": pop,
            "immigres": imm,
            "non_immigres": pop - imm,
            "part_immigres": round(100 * imm / pop, 2),
            "statut_stock": statut_stock(a),
            "champ": b(a)["champ"],
            "rupture": a == 2024,
        }
        if a < fin:
            ligne |= _flux(a, b, fx, immigres, r_moy, r_min, r_max, collecte_2024)
        annees.append(ligne)

    return {
        "echelle": params["echelle"],
        "statut_parametres": params["statut"],
        "ratio_deces": {
            "moyen": round(r_moy, 4),
            "min": round(r_min, 4),
            "max": round(r_max, 4),
            "calage": list(params["deces_immigres"]["calage"]),
            "par_annee": {str(a): round(r, 4) for a, r in ratios.items()},
        },
        "evenements": params["evenements"],
        "annees": annees,
    }


def _flux(a, b, fx, immigres, r_moy, r_min, r_max, collecte_2024) -> dict:
    bil, suiv = b(a), b(a + 1)
    naissances, deces = bil["naissances"], bil["deces"]
    imm, imm_suiv = immigres(a), immigres(a + 1)
    d_imm_ni = (suiv["population"] - imm_suiv) - (bil["population"] - imm)
    d_imm = imm_suiv - imm
    f = fx.get(a)
    o = {
        "naissances": naissances,
        "deces": deces,
        "entrees_imm": None,
        "sorties_imm": None,
        "net_imm": None,
        "entrees_ni": None,
        "sorties_ni": None,
        "net_ni": None,
        "ajust_imm": 0,
        "ajust_ni": 0,
        "non_ventile_imm": 0,
        "non_ventile_ni": 0,
        "deces_imm_bas": None,
        "deces_imm_haut": None,
    }

    def estime(r: float) -> int:
        return round(r * imm / bil["population"] * deces)

    if f and f["sorties_imm"] is not None:
        o["statut_flux"] = "mesure"
        o["deces_imm"] = f["deces_imm"]
        o["deces_ni"] = deces - f["deces_imm"]
        o |= {k: f[k] for k in ("entrees_imm", "sorties_imm", "entrees_ni", "sorties_ni")}
        o["net_imm"] = f["entrees_imm"] - f["sorties_imm"]
        o["net_ni"] = f["entrees_ni"] - f["sorties_ni"]
        o["ajust_imm"] = d_imm - (o["net_imm"] - o["deces_imm"])
        o["ajust_ni"] = d_imm_ni - (naissances - o["deces_ni"] + o["net_ni"])
    elif f:
        o["statut_flux"] = "partiel"
        o["deces_imm"] = estime(r_moy)
        o["deces_imm_bas"], o["deces_imm_haut"] = estime(r_min), estime(r_max)
        o["deces_ni"] = deces - o["deces_imm"]
        o["entrees_imm"], o["entrees_ni"] = f["entrees_imm"], f["entrees_ni"]
        collecte = collecte_2024 if a == 2023 else 0  # stocks de 2023 à 2024 : U5
        o["ajust_imm"], o["ajust_ni"] = collecte, -collecte
        o["non_ventile_imm"] = d_imm - (o["entrees_imm"] - o["deces_imm"]) - collecte
        o["non_ventile_ni"] = d_imm_ni - (naissances - o["deces_ni"] + o["entrees_ni"]) + collecte
    else:
        o["statut_flux"] = "reconstruit"
        o["deces_imm"] = estime(r_moy)
        o["deces_imm_bas"], o["deces_imm_haut"] = estime(r_min), estime(r_max)
        o["deces_ni"] = deces - o["deces_imm"]
        o["net_imm"] = d_imm + o["deces_imm"]
        o["net_ni"] = bil["solde_migratoire"] - o["net_imm"]
        o["ajust_ni"] = d_imm_ni - (naissances - o["deces_ni"] + o["net_ni"])
    return o


def ecart_identite(ligne: dict, suivante: dict) -> int:
    """Écart à l'identité comptable des immigrés (0 attendu, par construction)."""
    net = ligne["net_imm"] if ligne["net_imm"] is not None else ligne["entrees_imm"]
    attendu = (
        ligne["immigres"] + net - ligne["deces_imm"] + ligne["ajust_imm"] + ligne["non_ventile_imm"]
    )
    return suivante["immigres"] - attendu
