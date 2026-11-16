"""Comparaisons internationales (module C) : Eurostat et OCDE, lus tels que publiés.

Deux tables longues (pays × année × indicateur), sans calcul : les rapports (pour 10 000
habitants, parts) se font au prérendu, à partir de la population de la même source.

- Eurostat (UE, AELE, Royaume-Uni jusqu'en 2019) : population au 1er janvier ; taux d'accroissement
  naturel, migratoire et total (‰) ; population selon le pays de naissance ; demandeurs d'asile
  (dont premières demandes) ; décisions de première instance ; PIB.
- OCDE : entrées standardisées de migrants à titre permanent, par catégorie (2014-2025), et
  population, pour les pays qui publient ces entrées.

Le « taux migratoire » d'Eurostat est un solde *y compris l'ajustement statistique* : il absorbe
les corrections de recensement (U22).
"""

import csv
from pathlib import Path

from .sources import fichier

# Pays retenus et noms en français (UE à 27, AELE, Royaume-Uni) ; agrégat UE à 27.
PAYS_EUROSTAT = {
    "EU27_2020": "Union européenne (27)",
    "BE": "Belgique", "BG": "Bulgarie", "CZ": "Tchéquie", "DK": "Danemark", "DE": "Allemagne",
    "EE": "Estonie", "IE": "Irlande", "EL": "Grèce", "ES": "Espagne", "FR": "France",
    "HR": "Croatie", "IT": "Italie", "CY": "Chypre", "LV": "Lettonie", "LT": "Lituanie",
    "LU": "Luxembourg", "HU": "Hongrie", "MT": "Malte", "NL": "Pays-Bas", "AT": "Autriche",
    "PL": "Pologne", "PT": "Portugal", "RO": "Roumanie", "SI": "Slovénie", "SK": "Slovaquie",
    "FI": "Finlande", "SE": "Suède", "IS": "Islande", "LI": "Liechtenstein", "NO": "Norvège",
    "CH": "Suisse", "UK": "Royaume-Uni",
}

PAYS_OCDE = {
    "AUS": "Australie", "AUT": "Autriche", "BEL": "Belgique", "CAN": "Canada", "CHE": "Suisse",
    "CHL": "Chili", "COL": "Colombie", "CRI": "Costa Rica", "CZE": "Tchéquie", "DEU": "Allemagne",
    "DNK": "Danemark", "ESP": "Espagne", "EST": "Estonie", "FIN": "Finlande", "FRA": "France",
    "GBR": "Royaume-Uni", "GRC": "Grèce", "HUN": "Hongrie", "IRL": "Irlande", "ISL": "Islande",
    "ISR": "Israël", "ITA": "Italie", "JPN": "Japon", "KOR": "Corée", "LTU": "Lituanie",
    "LUX": "Luxembourg", "LVA": "Lettonie", "MEX": "Mexique", "NLD": "Pays-Bas", "NOR": "Norvège",
    "NZL": "Nouvelle-Zélande", "POL": "Pologne", "PRT": "Portugal", "SVK": "Slovaquie",
    "SVN": "Slovénie", "SWE": "Suède", "TUR": "Türkiye", "USA": "États-Unis",
}

# Code de dimension Eurostat → indicateur exporté.
INDICATEURS = {
    "eurostat_indicateurs": ("indic_de", {
        "JAN": "population", "NATGROWRT": "taux_naturel", "CNMIGRATRT": "taux_migratoire",
        "GROWRT": "taux_croissance",
    }),
    "eurostat_naissance": ("c_birth", {"TOTAL": "pop_naissance_total", "FOR": "nes_etranger", "NAT": "nes_pays"}),
    "eurostat_demandes": ("applicant", {"TOTAL": "demandes_asile", "FRST": "premieres_demandes"}),
    "eurostat_decisions": ("decision", {
        "TOTAL": "decisions", "POS": "decisions_positives", "POS_RFG": "statut_refugie",
        "POS_SPROT": "protection_subsidiaire", "POS_HUM": "raisons_humanitaires", "NEG": "decisions_negatives",
    }),
    "eurostat_pib": ("na_item", {"B1GQ": "pib_meur"}),
}

CATEGORIES_OCDE = {
    "WO": "travail", "AC": "famille_accompagnante", "FA": "famille", "HU": "humanitaire",
    "FR": "libre_circulation", "OT": "autres",
}


def lire_eurostat(raw: Path) -> list[dict]:
    out = []
    for cle, (dim, codes) in INDICATEURS.items():
        with open(fichier(raw, cle), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["geo"] not in PAYS_EUROSTAT or r[dim] not in codes or r["OBS_VALUE"] == "":
                    continue
                out.append({
                    "geo": r["geo"],
                    "pays": PAYS_EUROSTAT[r["geo"]],
                    "annee": int(r["TIME_PERIOD"]),
                    "indicateur": codes[r[dim]],
                    "valeur": float(r["OBS_VALUE"]),
                    "drapeau": r["OBS_FLAG"],
                })
    return sorted(out, key=lambda x: (x["indicateur"], x["geo"], x["annee"]))


def lire_ocde(raw: Path) -> list[dict]:
    out = []
    with open(fichier(raw, "ocde_entrees"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["REF_AREA"] in PAYS_OCDE and r["OBS_VALUE"] != "":
                out.append({
                    "pays_code": r["REF_AREA"], "pays": PAYS_OCDE[r["REF_AREA"]],
                    "annee": int(r["TIME_PERIOD"]), "indicateur": f"entrees_{CATEGORIES_OCDE[r['MIGRATION_TYPE']]}",
                    "valeur": round(float(r["OBS_VALUE"])), "drapeau": r["OBS_STATUS"],
                })
    publient = {x["pays_code"] for x in out}
    with open(fichier(raw, "ocde_population"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["REF_AREA"] in publient and r["OBS_VALUE"] != "":
                out.append({
                    "pays_code": r["REF_AREA"], "pays": PAYS_OCDE[r["REF_AREA"]],
                    "annee": int(r["TIME_PERIOD"]), "indicateur": "population",
                    "valeur": round(float(r["OBS_VALUE"])), "drapeau": r["OBS_STATUS"],
                })
    return sorted(out, key=lambda x: (x["indicateur"], x["pays_code"], x["annee"]))
