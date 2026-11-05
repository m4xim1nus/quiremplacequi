from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
RAW = RACINE / "data/raw"
EXPORT = RACINE / "data/export"


@pytest.fixture
def raw() -> Path:
    if not (RAW / "manifeste.json").exists():
        pytest.skip("sources absentes : lancer `uv run qrq download`")
    return RAW


@pytest.fixture
def export() -> Path:
    if not (EXPORT / "piscine.json").exists():
        pytest.skip("export absent : lancer `uv run qrq build`")
    return EXPORT
