"""data/raw/ → data/qrq.sqlite (non versionnée) + data/export/ (versionné, lu par le site)."""

import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import yaml

from . import bilan, cohortes, flux, ip1910, naissances, piscine, stock, teo2
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
    # Modèle de cohortes (générations), calé sur IP 1910 et les sorties Insee.
    pc = referentiel("cohortes")
    entrees = cohortes.preparer(raw, tables["b1_stock"], tables["bilan"], tables["naissances_parents"], pc)
    # Avant 1946, le bilan n'a pas de population : on la lit dans les pyramides (métropole).
    bilan.completer_avant_1946(tables["bilan"], {a: float(v.sum()) for a, v in entrees.ages.items() if a < 1946})
    psc = piscine.construire(tables["b1_stock"], tables["bilan"], tables["flux"], referentiel("piscine"))
    cibles = cohortes.lire_cibles_ip1910(raw)
    sorties = {f["annee"]: f["sorties_imm"] for f in tables["flux"] if f["sorties_imm"] is not None}
    sim, cal = cohortes.caler(entrees, pc, cibles, sorties)
    piscine.ajouter_generations(psc, sim)
    # Fourchette des générations selon l'hypothèse sur les G2 vivants en 1911 (U20) : recalage aux
    # deux bornes de cohortes.yaml, la référence comprise dans la fourchette.
    variantes = [sim] + [
        cohortes.caler(entrees, {**pc, "initial": {**pc["initial"], "g2_rapport_g1": r}}, cibles, sorties)[0]
        for r in pc["sensibilite"]["g2_rapport_g1"]
    ]
    piscine.ajouter_fourchette(psc, variantes)
    psc["cohortes"] = {"statut_parametres": pc["statut"], "calage": cal}
    tables["piscine"] = psc["annees"]
    tables["cohortes"] = [
        {"annee": a["annee"], "groupe": g, "tranche": f"{lo}-{hi}" if hi < 105 else f"{lo}+", "effectif": v}
        for a in sim["annees"]
        for g in cohortes.GROUPES
        for (lo, hi), v in zip(cohortes.TRANCHES, cohortes.tranches(a["etat"][g]))
    ]
    tables["cohortes_calage"] = cohortes.ecarts_calage(sim, entrees, cibles, tables["flux"], raw)
    # Pyramides des âges (Insee), pour « l'eau d'une année encore présente » dans la piscine.
    tables["ages"] = [
        {"annee": a, "age": i, "population": round(float(x))}
        for a, v in sorted(entrees.ages.items())
        for i, x in enumerate(v)
    ]
    tables["teo2"] = teo2.lire_teo2()
    tables["ip1910"] = ip1910.lire_ip1910(raw)

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
