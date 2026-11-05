from qrq.lecture import Annee, annee, milliers, nombre


def test_nombres_insee():
    assert nombre("7970") == 7970
    assert nombre("-71") == -71
    assert nombre("11.6") == 11.6
    assert nombre("+19p") == 19
    assert nombre("246e") == 246
    assert nombre("1 234") == 1234
    for vide in ("nd", "nd ", "///", "ns", None, ""):
        assert nombre(vide) is None
    assert milliers("7029.1") == 7_029_100


def test_annees_insee():
    assert annee("2025 (p)") == Annee(2025, "provisoire", False)
    assert annee("2024 (p)\xa0(*)") == Annee(2024, "provisoire", True)
    assert annee("2020e") == Annee(2020, "estime", False)
    assert annee(1968) == Annee(1968, "definitif", False)
    assert annee("Lecture : en 2025") is None
