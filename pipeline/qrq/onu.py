"""Émigration dans le monde (module C7) : ONU, lus tels que publiés.

- Migrants par pays d'origine et de destination en 2024 (International Migrant Stock 2024,
  tableau 1 ; tableau 2 pour les grandes régions).
- Population au 1er juillet 2024 (World Population Prospects 2024). 2024 est la première année de
  la variante moyenne : c'est la population que l'ONU associe à ses stocks de migrants de 2024.
- PIB par habitant en dollars courants (Division de statistique, dernière année publiée).
- Noms français des pays et des régions (nomenclature M49).

Rien n'est calculé ici : le taux d'émigration et les classements se font au prérendu.
"""

import html
import re
from pathlib import Path

import openpyxl

from .sources import fichier

ANNEE = 2024
AFRIQUE_SUBSAHARIENNE_IMS = 1834  # code de région du fichier des migrants
MONDE = 900
FRANCE = 250

# Grandes régions (objectifs de développement durable) du tableau 2 : code → nom français.
REGIONS_ODD = {
    1834: "Afrique subsaharienne",
    1833: "Afrique du Nord et Asie de l'Ouest",
    1831: "Asie centrale et du Sud",
    1832: "Asie de l'Est et du Sud-Est",
    1830: "Amérique latine et Caraïbes",
    1835: "Océanie (hors Australie et Nouvelle-Zélande)",
    1836: "Australie et Nouvelle-Zélande",
    1829: "Europe et Amérique du Nord",
}


def _m49(raw: Path) -> dict[int, dict]:
    """Code M49 → nom français du pays, de sa région, de sa sous-région (tableau français de la page)."""
    t = fichier(raw, "onu_m49").read_text(encoding="utf-8")
    tables = [m.start() for m in re.finditer(r"<table", t)]
    cellules = lambda r: [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
    for i, debut in enumerate(tables):
        fin = tables[i + 1] if i + 1 < len(tables) else len(t)
        lignes = [cellules(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t[debut:fin], re.S)]
        if len(lignes) > 1 and lignes[1][1] == "Monde":
            return {
                int(l[9]): {"pays": l[8], "region": l[3], "sous_region": l[5], "iso3": l[11]}
                for l in lignes[1:]
                if len(l) > 11 and l[9].isdigit()
            }
    raise ValueError("M49 : tableau français introuvable")


def _ligne_entete(lignes: list[tuple], texte: str) -> int:
    return next(i for i, r in enumerate(lignes) if r and any(texte == str(c).strip() for c in r if c is not None))


def lire_onu(raw: Path) -> tuple[list[dict], list[dict]]:
    """→ (pays : émigrés, immigrés, population, PIB par habitant ; régions : où vivent les émigrés
    d'Afrique subsaharienne)."""
    noms = _m49(raw)

    wb = openpyxl.load_workbook(fichier(raw, "onu_migrants"), read_only=True, data_only=True)
    t1 = list(wb["Table 1"].iter_rows(values_only=True))
    h = _ligne_entete(t1, "Location code of destination")
    entete = t1[h]
    col = entete.index(ANNEE)  # première occurrence : les deux sexes
    c_dest, c_orig = entete.index("Location code of destination"), entete.index("Location code of origin")
    emigres, immigres = {}, {}
    vers_france = {}
    for r in t1[h + 1 :]:
        if r[c_dest] is None or r[col] is None:
            continue
        d, o, v = int(r[c_dest]), int(r[c_orig]), int(r[col])
        if d == MONDE:
            emigres[o] = v
        if o == MONDE:
            immigres[d] = v
        if d == FRANCE:
            vers_france[o] = v

    t2 = list(wb["Table 2"].iter_rows(values_only=True))
    h2 = _ligne_entete(t2, "Location code of destination")
    codes_orig = t2[h2]
    c_ssa = list(codes_orig).index(AFRIQUE_SUBSAHARIENNE_IMS)
    c_code = list(codes_orig).index("Location code of destination")
    regions = []
    for r in t2[h2 + 1 :]:
        if r[c_code] in REGIONS_ODD or r[c_code] == MONDE:
            regions.append({
                "origine": "Afrique subsaharienne",
                "destination": "Monde" if r[c_code] == MONDE else REGIONS_ODD[r[c_code]],
                "code_destination": r[c_code],
                "migrants": int(r[c_ssa]),
                "annee": ANNEE,
            })
    regions.append({
        "origine": "Afrique subsaharienne", "destination": "dont France", "code_destination": FRANCE,
        "migrants": vers_france[AFRIQUE_SUBSAHARIENNE_IMS], "annee": ANNEE,
    })
    wb.close()

    # Population au 1er juillet 2024 (milliers), pays et Afrique subsaharienne.
    wp = openpyxl.load_workbook(fichier(raw, "onu_population"), read_only=True, data_only=True)
    lignes = list(wp["Medium variant"].iter_rows(values_only=True))
    h3 = _ligne_entete(lignes, "Location code")
    e3 = lignes[h3]
    c_loc, c_type, c_an, c_nom = e3.index("Location code"), e3.index("Type"), e3.index("Year"), 2
    c_pop = next(i for i, c in enumerate(e3) if c and str(c).startswith("Total Population, as of 1 July"))
    population, pop_ssa = {}, None
    for r in lignes[h3 + 1 :]:
        if r[c_an] != ANNEE:
            continue
        if r[c_type] == "Country/Area":
            population[int(r[c_loc])] = round(float(r[c_pop]) * 1000)
        elif str(r[c_nom]).strip() == "Sub-Saharan Africa":
            pop_ssa = round(float(r[c_pop]) * 1000)
    wp.close()
    assert pop_ssa, "WPP : Afrique subsaharienne introuvable"
    regions.append({
        "origine": "Afrique subsaharienne", "destination": "population résidente", "code_destination": None,
        "migrants": pop_ssa, "annee": ANNEE,
    })

    # PIB par habitant (dollars courants), dernière année publiée jusqu'en 2024.
    wg = openpyxl.load_workbook(fichier(raw, "onu_pib"), read_only=True, data_only=True)
    lg = list(wg.worksheets[0].iter_rows(values_only=True))
    h4 = _ligne_entete(lg, "CountryID")
    ans = [c for c in lg[h4] if isinstance(c, int)]
    pib = {}
    for r in lg[h4 + 1 :]:
        if not isinstance(r[0], int):
            continue
        vals = {a: v for a, v in zip(lg[h4][2:], r[2:]) if isinstance(a, int) and a <= ANNEE and isinstance(v, (int, float))}
        if vals:
            a = max(vals)
            pib[r[0]] = (a, vals[a])
    wg.close()
    assert max(ans) >= ANNEE - 1

    pays = []
    for code, pop in sorted(population.items()):
        if code not in noms:
            continue
        n = noms[code]
        pays.append({
            "code": code,
            "pays": n["pays"],
            "iso3": n["iso3"],
            "region": n["region"],
            "sous_region": n["sous_region"],
            "emigres": emigres.get(code),
            "immigres": immigres.get(code),
            "population": pop,
            "pib_hab_usd": None if code not in pib else round(pib[code][1]),
            "annee_pib": None if code not in pib else pib[code][0],
            "annee": ANNEE,
        })
    return pays, regions
