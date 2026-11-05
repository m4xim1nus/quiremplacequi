import pytest

from qrq.check import verifier


@pytest.mark.donnees
def test_controles_passent(export):
    ok, lignes = verifier(export)
    assert ok, "\n".join(l for l in lignes if l.startswith("KO"))
