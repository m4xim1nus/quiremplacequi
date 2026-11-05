"""data/raw/ → data/qrq.sqlite (non versionnée) + data/export/ (versionné, lu par le site)."""

import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import yaml

from . import bilan, flux, naissances, piscine, stock
from .sources import SOURCES

REFERENTIELS = Path(__file__).resolve().parents[1] / "referentiels"


def referentiel(nom: str) -> dict:
    return yaml.safe_load((REFERENTIELS / f"{nom}.yaml").read_text())


def build(raw: Path, sqlite: Path, export: Path) -> None:
    tables = {
        "b1_stock": stock.lire_stock(raw),
        "b2_pays": stock.lire_pays_long(raw),
        "b2_nationalites": stock.lire_nationalites(raw),
        "bilan": bilan.lire_bilan(raw),
        "flux": flux.lire_flux(raw),
        "naissances_parents": naissances.lire_naissances_parents(raw),
    }
    psc = piscine.construire(
        tables["b1_stock"], tables["bilan"], tables["flux"], referentiel("piscine")
    )
    tables["piscine"] = psc["annees"]

    if export.exists():
        shutil.rmtree(export)
    export.mkdir(parents=True)
    sqlite.unlink(missing_ok=True)
    with sqlite3.connect(sqlite) as con:
        for nom, lignes in tables.items():
            df = pl.DataFrame(lignes, infer_schema_length=None)
            df.write_csv(export / f"{nom}.csv")
            cols = ", ".join(f'"{c}"' for c in df.columns)
            con.execute(f"CREATE TABLE {nom} ({cols})")
            con.executemany(
                f"INSERT INTO {nom} VALUES ({', '.join('?' * len(df.columns))})", df.rows()
            )
            print(f"{nom:20} {len(df):>5} lignes")

    (export / "piscine.json").write_text(json.dumps(psc, ensure_ascii=False, indent=1))
    (export / "incertitudes.json").write_text(
        json.dumps(referentiel("incertitudes"), ensure_ascii=False, indent=1)
    )
    manifeste = json.loads((raw / "manifeste.json").read_text())
    meta = {
        "genere_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {k: manifeste[k] | {"titre": SOURCES[k]["titre"]} for k in SOURCES},
        "licence_sources": "Licence Ouverte 2.0 (Etalab)",
    }
    (export / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"export : {len(list(export.iterdir()))} fichiers dans {export}")
