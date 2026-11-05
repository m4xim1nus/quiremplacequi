"""Sources et téléchargement (docs/SOURCES.md, docs/spike/insee.md).

`download` note dans `<raw>/manifeste.json` l'URL, la date de téléchargement, la taille et le
sha256 de chaque fichier : ce manifeste est recopié dans l'export et date l'instantané.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

INSEE = "https://www.insee.fr/fr/statistiques"
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
    "pays": {
        "page": f"{INSEE}/2381755",
        "url": f"{INSEE}/fichier/2381755/demo-etran-repart-immig-pays.xlsx",
        "titre": "Immigrés par pays de naissance (2006-2025)",
    },
}


def fichier(raw: Path, cle: str) -> Path:
    return raw / "insee" / Path(SOURCES[cle]["url"]).name


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
            r = client.get(src["url"])
            r.raise_for_status()
            cible.write_bytes(r.content)
            manifeste[cle] = {
                "url": src["url"],
                "page": src["page"],
                "titre": src["titre"],
                "fichier": str(cible.relative_to(raw)),
                "telecharge_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "octets": len(r.content),
                "sha256": hashlib.sha256(r.content).hexdigest(),
            }
            print(f"{cle:20} {len(r.content):>9} o  {src['url']}")
    raw.mkdir(parents=True, exist_ok=True)
    manifeste_f.write_text(json.dumps(manifeste, ensure_ascii=False, indent=2, sort_keys=True))
