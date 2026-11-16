"""Sources et téléchargement (docs/SOURCES.md, docs/spike/insee.md).

`download` note dans `<raw>/manifeste.json` l'URL, la date de téléchargement, la taille et le
sha256 de chaque fichier : ce manifeste est recopié dans l'export et date l'instantané.

Quatre familles, un sous-dossier de data/raw/ chacune : Insee, ministère de l'Intérieur (DSED, par
data.gouv.fr), Eurostat (API SDMX) et OCDE (API SDMX). Une source sans `famille` est de l'Insee.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

INSEE = "https://www.insee.fr/fr/statistiques"
DGF = "https://static.data.gouv.fr/resources"
ESTAT = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
ESTAT_PAGE = "https://ec.europa.eu/eurostat/databrowser/view"
OCDE = "https://sdmx.oecd.org/public/rest/data"
OCDE_PAGE = "https://data-explorer.oecd.org/"

LICENCES = {
    "insee": "Licence Ouverte 2.0 (Etalab)",
    "dsed": "Licence Ouverte 2.0 (Etalab)",
    "eurostat": "CC BY 4.0 (politique de réutilisation de la Commission européenne)",
    "ocde": "CC BY 4.0 (OCDE)",
    "onu": "CC BY 3.0 IGO (ONU, Division de la population)",
}
UA = {"User-Agent": "qrq-pipeline/0.1"}

# clé locale → page et fichier sur insee.fr (Licence Ouverte 2.0)
SOURCES: dict[str, dict] = {
    "stock": {
        "page": f"{INSEE}/2381757",
        "url": f"{INSEE}/fichier/2381757/demo-etran-part-pop-etran-immig.xlsx",
        "titre": "Population immigrée et étrangère en France (1921-2025)",
    },
    "flux": {
        "page": f"{INSEE}/8998082",
        "url": f"{INSEE}/fichier/8998082/IP2107.xlsx",
        "titre": "Insee Première 2107 : flux migratoires 2006-2024",
    },
    "bilan": {
        "page": f"{INSEE}/8999013",
        "url": f"{INSEE}/fichier/8999013/1_Pop_annu_compo_evol.xlsx",
        "titre": "Bilan démographique : population au 1er janvier et composantes (séries longues)",
    },
    "naissances_parents": {
        "page": f"{INSEE}/2381382",
        "url": f"{INSEE}/fichier/2381382/demo-naiss-natio-pays-2.xlsx",
        "titre": "Naissances selon la nationalité et le pays de naissance des parents (1998-2025)",
    },
    "pays_long": {
        "page": f"{INSEE}/6793226",
        "url": f"{INSEE}/fichier/6793226/IMMFRA23-F2.xlsx",
        "titre": "Immigrés et descendants d'immigrés, éd. 2023 : histoire des migrations (1911-2021)",
    },
    "ip1910": {
        "page": f"{INSEE}/6468640",
        "url": f"{INSEE}/fichier/6468640/ip1910.xlsx",
        "titre": "Insee Première 1910 : diversité des origines et mixité des unions",
    },
    "ages": {
        "page": f"{INSEE}/8999013",
        "url": f"{INSEE}/fichier/8999013/3_Pop1janv_age.xlsx",
        "titre": "Population au 1er janvier par sexe et âge (séries longues, depuis 1901)",
    },
    "mortalite": {
        "page": f"{INSEE}/8999019",
        "url": f"{INSEE}/fichier/8999019/3_Quotients_mortalite.xlsx",
        "titre": "Quotients de mortalité par sexe et âge (séries longues, depuis 1901)",
    },
    "nes_etranger": {
        "page": f"{INSEE}/2865118",
        "url": f"{INSEE}/fichier/2865118/demo-etran-decompo-pop.xlsx",
        "titre": "Population selon le lieu de naissance et la nationalité (2006-2025)",
    },
    "ages_immigres": {
        "page": f"{INSEE}/2381759",
        "url": f"{INSEE}/fichier/2381759/demo-etran-pop-sexe-age.xlsx",
        "titre": "Population immigrée et étrangère par sexe et âge (1990-2025)",
    },
    "descendants": {
        "page": f"{INSEE}/4186761",
        "url": f"{INSEE}/fichier/4186761/demo-etran-origine-desc-immig.xlsx",
        "titre": "Origine géographique des descendants d'immigrés (2025)",
    },
    "pays": {
        "page": f"{INSEE}/2381755",
        "url": f"{INSEE}/fichier/2381755/demo-etran-repart-immig-pays.xlsx",
        "titre": "Immigrés par pays de naissance (2006-2025)",
    },
}

# Ministère de l'Intérieur, DSED, sur data.gouv.fr. Premiers titres de séjour délivrés aux
# ressortissants de pays tiers : la série publiée le 27 juin 2024 (2011-2023, France, hors
# Britanniques) et les fichiers annuels définitifs publiés en août 2026 (2015-2024, France) :
# année → (jeu de données, horodatage du fichier par motif, horodatage du fichier par nationalité).
DSED_ANNUELS = {
    2015: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2015-1", "20260819-102526", "20260819-102526"),
    2016: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2016", "20260819-100315", "20260819-100314"),
    2017: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2017", "20260819-135828", "20260819-135827"),
    2018: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2018", "20260819-145553", "20260819-145553"),
    2019: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2019", "20260820-083454", "20260820-083454"),
    2020: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2020", "20260821-101708", "20260821-101707"),
    2021: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2021", "20260821-115449", "20260821-115449"),
    2022: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2022", "20260821-121553", "20260821-121553"),
    2023: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2023", "20260821-124215", "20260821-124216"),
    2024: ("stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2024", "20260821-131354", "20260821-131354"),
}
SOURCES["titres_serie"] = {
    "famille": "dsed",
    "page": "https://www.data.gouv.fr/datasets/66a8cc809b4750710f18920c",
    "url": f"{DGF}/titres-de-sejour-publication-du-27-juin-2024/20240730-113905/"
    "les-titres-de-sejour-au-27-juin-2024-admission-au-sejour-par-motif.csv",
    "titre": "DSED : premiers titres de séjour par motif, 2011-2023 (publication du 27 juin 2024)",
}
for _a, (_jeu, _h_motif, _h_nat) in DSED_ANNUELS.items():
    SOURCES[f"titres_{_a}"] = {
        "famille": "dsed",
        "page": "https://www.data.gouv.fr/organizations/ministere-de-l-interieur/",
        "url": f"{DGF}/{_jeu}/{_h_motif}/{_a}-sejour-flux-motif-sous-motif.csv",
        "titre": f"DSED : premiers titres de séjour par motif et sous-motif, {_a} (définitif)",
    }
    SOURCES[f"titres_nat_{_a}"] = {
        "famille": "dsed",
        "page": "https://www.data.gouv.fr/organizations/ministere-de-l-interieur/",
        "url": f"{DGF}/{_jeu}/{_h_nat}/{_a}-sejour-flux-region-monde-nationalites.csv",
        "titre": f"DSED : premiers titres de séjour par nationalité, {_a} (définitif)",
    }

# Eurostat (requêtes SDMX : seules les dimensions utiles sont demandées).
for _cle, _ds, _filtre, _titre in [
    ("eurostat_indicateurs", "demo_gind", "A.JAN+NATGROWRT+CNMIGRATRT+GROWRT./?startPeriod=1960",
     "Eurostat demo_gind : population au 1er janvier, taux d'accroissement naturel, migratoire (y c. ajustement) et total"),
    ("eurostat_naissance", "migr_pop3ctb", "A.TOTAL+FOR+NAT.TOTAL.NR.T./?startPeriod=2011",
     "Eurostat migr_pop3ctb : population au 1er janvier selon le pays de naissance"),
    ("eurostat_demandes", "migr_asyappctza", "A.TOTAL.FRST+TOTAL.T.PER.TOTAL./?startPeriod=2008",
     "Eurostat migr_asyappctza : demandeurs d'asile (dont premières demandes), annuel"),
    ("eurostat_decisions", "migr_asydcfsta", "A.PER.TOTAL.T.TOTAL.TOTAL+POS+POS_RFG+POS_SPROT+POS_HUM+NEG./?startPeriod=2008",
     "Eurostat migr_asydcfsta : décisions d'asile en première instance, par type"),
    ("eurostat_pib", "nama_10_gdp", "A.CP_MEUR.B1GQ./?startPeriod=2008",
     "Eurostat nama_10_gdp : produit intérieur brut aux prix courants (millions d'euros)"),
]:
    SOURCES[_cle] = {
        "famille": "eurostat",
        "page": f"{ESTAT_PAGE}/{_ds}/default/table",
        "url": f"{ESTAT}/{_ds}/{_filtre}&format=SDMX-CSV",
        "nom": f"{_ds}.csv",
        "titre": _titre,
    }

# OCDE (Base de données sur les migrations internationales ; population historique).
SOURCES["ocde_entrees"] = {
    "famille": "ocde",
    "page": OCDE_PAGE,
    "url": f"{OCDE}/OECD.ELS.IMD,DSD_MIG_INT@DF_MIG_INT_PER,1.0/all?startPeriod=2014&format=csvfilewithlabels",
    "nom": "entrees_permanentes.csv",
    "titre": "OCDE : entrées standardisées de migrants à titre permanent, par catégorie (2014-2025)",
}
SOURCES["ocde_population"] = {
    "famille": "ocde",
    "page": OCDE_PAGE,
    "url": f"{OCDE}/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/.POP.PS._T._T.?startPeriod=2014&format=csvfilewithlabels",
    "nom": "population.csv",
    "titre": "OCDE : population historique, tous âges (2014-2025)",
}


# ONU. Le site de la Division de la population (un.org) refuse les scripts (403) : le fichier des
# stocks de migrants est déposé à la main dans data/raw/onu/ (`manuel`), le programme en note
# l'empreinte. Les populations (population.un.org), le PIB par habitant et la nomenclature M49 en
# français (unstats.un.org) se téléchargent.
SOURCES["onu_migrants"] = {
    "famille": "onu",
    "manuel": True,
    "page": "https://www.un.org/development/desa/pd/content/international-migrant-stock",
    "url": "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/"
    "undesa_pd_2024_ims_stock_by_sex_destination_and_origin.xlsx",
    "titre": "ONU DESA, International Migrant Stock 2024 : migrants par pays de destination et d'origine (1990-2024)",
}
SOURCES["onu_population"] = {
    "famille": "onu",
    "page": "https://population.un.org/wpp/",
    "url": "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/EXCEL_FILES/"
    "1_General/WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT.xlsx",
    "nom": "WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT.xlsx",
    "titre": "ONU DESA, World Population Prospects 2024 : indicateurs démographiques par pays",
}
SOURCES["onu_pib"] = {
    "famille": "onu",
    "page": "https://unstats.un.org/unsd/snaama/downloads",
    "url": "https://unstats.un.org/unsd/amaapi/api/file/9",
    "nom": "pib_par_habitant_usd.xlsx",
    "titre": "ONU, Division de statistique : PIB par habitant en dollars courants, tous pays (1970-)",
    "licence": "Conditions d'utilisation de l'ONU (réutilisation libre, source citée)",
}
SOURCES["onu_m49"] = {
    "famille": "onu",
    "page": "https://unstats.un.org/unsd/methodology/m49/overview/",
    "url": "https://unstats.un.org/unsd/methodology/m49/overview/",
    "nom": "m49.html",
    "titre": "ONU, Division de statistique : nomenclature M49 des pays et régions (noms français)",
    "licence": "Conditions d'utilisation de l'ONU (réutilisation libre, source citée)",
}


# Fécondité (page « Les naissances ») : Insee Première 1939 (fécondité des femmes nées à
# l'étranger, descendance finale selon le lien à la migration, TeO1 et TeO2) et tableaux
# rétrospectifs du bilan démographique (indicateur conjoncturel, taux de reproduction, descendance
# par génération). Le PDF de l'Insee Première sert à vérifier les chiffres de son encadré, saisis
# dans referentiels/fecondite.yaml.
SOURCES["fecondite_ip1939"] = {
    "page": f"{INSEE}/6801884",
    "url": f"{INSEE}/fichier/6801884/donnees_insee_premiere_n1939.xlsx",
    "titre": "Insee Première 1939 : combien les femmes immigrées ont-elles d'enfants ? (données, 2023)",
}
SOURCES["fecondite_ip1939_pdf"] = {
    "page": f"{INSEE}/6801884",
    "url": f"{INSEE}/fichier/version-html/6801884/ip1939.pdf",
    "titre": "Insee Première 1939 : combien les femmes immigrées ont-elles d'enfants ? (texte, 2023)",
}
SOURCES["icf"] = {
    "page": f"{INSEE}/8721207",
    "url": f"{INSEE}/fichier/8721207/3_ICF_age_moyen_femmes.xlsx",
    "titre": "Bilan démographique 2025 : indicateur conjoncturel de fécondité des femmes (1901-2025)",
}
SOURCES["reproduction"] = {
    "page": f"{INSEE}/8721207",
    "url": f"{INSEE}/fichier/8721207/5_Taux_reproduction.xlsx",
    "titre": "Bilan démographique 2025 : taux de reproduction brut et net des femmes (1901-2025)",
}
SOURCES["descendance"] = {
    "page": f"{INSEE}/8721207",
    "url": f"{INSEE}/fichier/8721207/4_Descendance_femmes.xlsx",
    "titre": "Bilan démographique 2025 : descendance des femmes par âge et par génération",
}
# Le rapport de 2000 sur les « migrations de remplacement » : la bibliothèque numérique de l'ONU
# accepte les scripts (un.org les refuse). Chiffres saisis dans referentiels/onu2000.yaml, page par
# page, et vérifiés contre ce PDF au build.
SOURCES["onu_2000"] = {
    "famille": "onu",
    "page": "https://digitallibrary.un.org/record/412547",
    "url": "https://digitallibrary.un.org/record/412547/files/unpd-egm_200010_un_2001_replacementmigration.pdf",
    "nom": "replacement_migration_2000.pdf",
    "titre": "ONU, Division de la population : Replacement Migration (ESA/P/WP.160, 2000)",
}


def famille(cle: str) -> str:
    return SOURCES[cle].get("famille", "insee")


def licence(cle: str) -> str:
    return SOURCES[cle].get("licence") or LICENCES[famille(cle)]


def fichier(raw: Path, cle: str) -> Path:
    src = SOURCES[cle]
    return raw / famille(cle) / src.get("nom", Path(src["url"].split("?")[0]).name)


def download(raw: Path, cles: list[str] | None = None) -> None:
    cles = cles or list(SOURCES)
    inconnues = set(cles) - set(SOURCES)
    if inconnues:
        raise SystemExit(f"sources inconnues : {sorted(inconnues)}")
    manifeste_f = raw / "manifeste.json"
    manifeste = json.loads(manifeste_f.read_text()) if manifeste_f.exists() else {}
    with httpx.Client(headers=UA, follow_redirects=True, timeout=120) as client:
        for cle in cles:
            src = SOURCES[cle]
            cible = fichier(raw, cle)
            cible.parent.mkdir(parents=True, exist_ok=True)
            if src.get("manuel"):
                # Déposé à la main : on n'en note que l'empreinte (et on ne le réécrit pas).
                if not cible.exists():
                    raise SystemExit(f"{cle} : déposer {src['url']} dans {cible}")
                contenu = cible.read_bytes()
            else:
                r = client.get(src["url"])
                r.raise_for_status()
                contenu = r.content
                cible.write_bytes(contenu)
            manifeste[cle] = {
                "url": src["url"],
                "page": src["page"],
                "titre": src["titre"],
                "licence": licence(cle),
                "fichier": str(cible.relative_to(raw)),
                "telecharge_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "octets": len(contenu),
                "sha256": hashlib.sha256(contenu).hexdigest(),
                **({"depot": "manuel"} if src.get("manuel") else {}),
            }
            print(f"{cle:20} {len(contenu):>9} o  {'(déposé) ' if src.get('manuel') else ''}{src['url']}")
    raw.mkdir(parents=True, exist_ok=True)
    manifeste_f.write_text(json.dumps(manifeste, ensure_ascii=False, indent=2, sort_keys=True))
