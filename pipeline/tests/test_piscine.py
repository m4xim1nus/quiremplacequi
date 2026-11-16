import json

import pytest

from qrq.piscine import construire, ecart_identite, interpoler, ratio_deces, suivre_solde


def test_interpolation_entre_recensements():
    pts = {1968: 3_238_000, 1975: 3_887_000}
    assert interpoler(pts, 1968) == 3_238_000
    assert interpoler(pts, 1975) == 3_887_000
    assert interpoler(pts, 1971) == pytest.approx(3_238_000 + 3 / 7 * 649_000)


def test_suivre_solde():
    # Solde du bilan 30 puis 10 ; décès nuls (r = 0) : flux net = solde + c, stock final atteint.
    bilans = [{"annee": 2000, "population": 1000, "deces": 10, "solde_migratoire": 30},
              {"annee": 2001, "population": 1000, "deces": 10, "solde_migratoire": 10}]
    s = suivre_solde(100, 160, bilans, r=0)
    assert s == {2000: 100, 2001: 100 + 30 + 10}  # c = (60 − 40) / 2 = 10
    # Avec décès : le dernier pas retombe exactement sur le recensement suivant.
    s = suivre_solde(100, 160, bilans, r=1.0)
    d = [1.0 * s[a] / 1000 * 10 for a in (2000, 2001)]
    c = s[2001] - s[2000] - 30 + d[0]
    assert s[2001] + 10 + c - d[1] == pytest.approx(160, abs=0.5)


def test_ratio_deces():
    # 10 % des décès pour 10 % de la population : rapport 1.
    assert ratio_deces(10, 100, 1_000, 10_000) == pytest.approx(1.0)


def _jeu():
    """Mini jeu : 2004-2005 reconstruits, 2006 mesuré, 2007 stock seul."""
    stock = [
        {"annee": 2004, "immigres": 900, "statut": "definitif"},
        {"annee": 2006, "immigres": 1000, "statut": "definitif"},
        {"annee": 2007, "immigres": 1050, "statut": "definitif"},
    ]
    bilan = [
        {"annee": a, "onglet": "FR", "champ": "france", "population": p, "naissances": 100,
         "deces": 80, "solde_naturel": 20, "solde_migratoire": 30, "ajustement": 0}
        for a, p in ((2004, 10_000), (2005, 10_050), (2006, 10_100), (2007, 10_150))
    ]
    flux = [{"annee": 2006, "entrees_imm": 70, "sorties_imm": 10, "deces_imm": 8,
             "entrees_ni": 20, "sorties_ni": 50}]
    params = {"debut": 2004, "fin": 2007, "bilan_metropole_jusqua": 1989,
              "recensements": [2004, 2006], "echelle": 1, "statut": "test",
              "deces_immigres": {"calage": [2006, 2006]}, "evenements": [],
              "saisies": {"effet_collecte_2024_immigres": {"valeur": 0}}}
    return construire(stock, bilan, flux, params)


def test_regimes_et_identite():
    p = _jeu()
    ans = p["annees"]
    assert [a.get("statut_flux") for a in ans] == ["reconstruit", "reconstruit", "mesure", None]
    assert ans[1]["immigres"] == 950  # interpolé
    assert ans[2]["net_imm"] == 60 and ans[2]["ajust_imm"] == 50 - (60 - 8)
    for x, y in zip(ans, ans[1:]):
        assert ecart_identite(x, y) == 0


@pytest.mark.donnees
def test_export_piscine(export):
    p = json.loads((export / "piscine.json").read_text())
    ans = {a["annee"]: a for a in p["annees"]}
    assert ans[2006]["statut_flux"] == "mesure" and ans[2005]["statut_flux"] == "reconstruit"
    assert ans[2023]["ajust_imm"] == 242_000  # effet de collecte (U5), jamais une arrivée
    assert ans[1990]["champ"] == "france_hors_mayotte" and ans[1989]["champ"] == "metropole"
