"""Tests de la ressaisie TeO2 : lecture des YAML, contrôles de cohérence et témoins du spike.

Les témoins sont les chiffres déjà cités dans docs/spike/teo2.md et relus dans les images.
"""

import pytest

from qrq.teo2 import DOSSIER_DEFAUT, lire_teo2, verifier_teo2


@pytest.fixture(scope="module")
def lignes() -> list[dict]:
    return lire_teo2(DOSSIER_DEFAUT)


def val(lignes, fichier, ligne, colonne):
    trouvees = [
        c["valeur"]
        for c in lignes
        if c["fichier"] == fichier and c["ligne"] == ligne and c["colonne"] == colonne
    ]
    assert len(trouvees) == 1, (fichier, ligne, colonne, trouvees)
    return trouvees[0]


def cellule(ligne="a", colonne="b", valeur=50, unite="%", fichier="x.yaml", **kw):
    return {"fichier": fichier, "chapitre": 0, "objet": "T", "ligne": ligne, "colonne": colonne,
            "valeur": valeur, "unite": unite, "approx": False, "champ": "", "precision": None, **kw}


# --- lire_teo2 ---------------------------------------------------------------------------------

def test_lire_structure(lignes):
    assert len(lignes) > 400
    attendues = {"fichier", "chapitre", "objet", "ligne", "colonne", "valeur", "unite", "approx", "champ"}
    for c in lignes:
        assert attendues <= set(c)
        assert isinstance(c["valeur"], (int, float))


def test_lire_dossier_vide(tmp_path):
    assert lire_teo2(tmp_path) == []


def test_lire_yaml_minimal(tmp_path):
    (tmp_path / "t.yaml").write_text(
        "source: {chapitre: 1, objet: T, titre: t, champ: c, unite: '%'}\n"
        "cellules:\n"
        "  - {ligne: l, colonne: c1, valeur: 3, approx: false}\n"
        "  - {ligne: l, colonne: c2, valeur: 4.5, approx: true, precision: 0.5, unite: effectif}\n",
        encoding="utf-8",
    )
    a, b = lire_teo2(tmp_path)
    assert (a["unite"], a["approx"], a["precision"]) == ("%", False, None)
    assert (b["unite"], b["approx"], b["precision"], b["valeur"]) == ("effectif", True, 0.5, 4.5)


def test_pas_de_doublon_ni_anomalie_hors_g1(lignes):
    # seule anomalie connue : la ligne G1 du tableau 4 du chapitre 9 somme à 123 dans la source imprimée
    anomalies = verifier_teo2(lignes)
    assert len(anomalies) == 1
    assert "ch09_tableau4.yaml" in anomalies[0] and "G1" in anomalies[0] and "123" in anomalies[0]


def test_approx_ont_precision(lignes):
    # ch. 11 figure 1 : points sans étiquette (± 0,5) ; ch. 7 figures 3-4 : segments trop fins pour
    # porter une étiquette (± 1).
    approx = [c for c in lignes if c["approx"]]
    ch11 = [c for c in approx if c["fichier"] == "ch11_figure1.yaml"]
    ch07 = [c for c in approx if c["fichier"].startswith("ch07_figure")]
    assert len(ch11) == 32 and len(ch07) == 8 and len(approx) == 40
    assert all(c["precision"] == 0.5 and c["unite"] == "points de pourcentage" for c in ch11)
    assert all(c["precision"] == 1 and c["valeur"] <= 1 for c in ch07)


# --- verifier_teo2 (cas synthétiques) -----------------------------------------------------------

def test_verifier_doublon():
    anomalies = verifier_teo2([cellule(), cellule()], controles={})
    assert any("doublon" in a for a in anomalies)


def test_verifier_somme_ok_a_l_arrondi():
    ls = [cellule(colonne="c1", valeur=33), cellule(colonne="c2", valeur=33), cellule(colonne="c3", valeur=33)]
    ctl = {"x.yaml": [{"axe": "ligne", "pour": ["a"], "parmi": ["c1", "c2", "c3"], "attendu": 100, "tolerance": 1}]}
    assert verifier_teo2(ls, controles=ctl) == []


def test_verifier_somme_ecart():
    ls = [cellule(colonne="c1", valeur=60), cellule(colonne="c2", valeur=30)]
    ctl = {"x.yaml": [{"axe": "ligne", "pour": ["a"], "parmi": ["c1", "c2"], "attendu": 100, "tolerance": 1}]}
    (anomalie,) = verifier_teo2(ls, controles=ctl)
    assert "90" in anomalie and "100" in anomalie


def test_verifier_somme_par_colonne_et_total_ligne():
    ls = [cellule("a", "c", 40), cellule("b", "c", 61), cellule("tot", "c", 100)]
    ctl = {"x.yaml": [{"axe": "colonne", "pour": ["c"], "parmi": ["a", "b"], "attendu_ligne": "tot", "tolerance": 0}]}
    assert len(verifier_teo2(ls, controles=ctl)) == 1


def test_verifier_cellule_manquante():
    ctl = {"x.yaml": [{"axe": "ligne", "pour": ["a"], "parmi": ["c1", "c2"], "attendu": 100}]}
    (anomalie,) = verifier_teo2([cellule(colonne="c1", valeur=100)], controles=ctl)
    assert "manquante" in anomalie


def test_verifier_pourcentage_hors_bornes_et_approx_sans_precision():
    anomalies = verifier_teo2([cellule(valeur=120), cellule(ligne="b", valeur=5, approx=True)], controles={})
    assert len(anomalies) == 2


# --- témoins du spike ---------------------------------------------------------------------------

def test_temoin_e1_generations(lignes):
    f = "ch08_tableau1.yaml"
    p = "Pourcentages pondérés"
    assert [val(lignes, f, r, p) for r in
            ("Immigré·e", "G2 Descendant·e", "G3 Descendant·e", "Sans ascendance immigrée sur trois générations")] == [13, 11, 10, 66]
    assert (val(lignes, f, "De deux parents immigrés", p), val(lignes, f, "G2.5 D’un parent immigré", p)) == (6, 5)
    assert (val(lignes, f, "De deux à quatre grands-parents immigrés", p), val(lignes, f, "G3.5 D’un grand-parent immigré", p)) == (4, 5)
    assert val(lignes, f, "Ensemble", "Effectifs non pondérés") == 27181
    assert [c["unite"] for c in lignes if c["fichier"] == f and c["colonne"] == "Effectifs non pondérés"] == ["effectif"] * 13


def test_temoin_41_pourcent(lignes):
    assert val(lignes, "ch08_texte_41pct.yaml", "Lien à l’immigration (personnel, par ascendance ou par alliance)", "Population de 18 à 59 ans") == 41


def test_temoin_tiers_somme(lignes):
    f, p = "ch08_tableau1.yaml", "Pourcentages pondérés"
    assert sum(val(lignes, f, r, p) for r in ("Immigré·e", "G2 Descendant·e", "G3 Descendant·e")) == 34


def test_temoin_e1_par_age(lignes):
    f = "ch08_tableau2.yaml"
    c = ["Immigré·e", "Descendant·e de deux parents immigrés", "Descendant·e d’un seul parent immigré (G2.5)",
         "Petits-enfants de deux à quatre grands-parents immigrés", "Petits-enfants d’un grand-parent immigré (G3.5)",
         "Sans ascendance immigrée sur trois générations (G4+)"]
    assert [val(lignes, f, "18-24 ans", x) for x in c] == [7, 7, 8, 4, 5, 68]
    assert [val(lignes, f, "35-39 ans", x) for x in c] == [16, 7, 5, 4, 4, 65]
    # la ligne « Ensemble » du tableau 2 reprend les pourcentages du tableau 1
    t1 = [val(lignes, "ch08_tableau1.yaml", r, "Pourcentages pondérés") for r in
          ("Immigré·e", "De deux parents immigrés", "G2.5 D’un parent immigré",
           "De deux à quatre grands-parents immigrés", "G3.5 D’un grand-parent immigré",
           "Sans ascendance immigrée sur trois générations")]
    assert [val(lignes, f, "Ensemble", x) for x in c] == t1


def test_temoin_e2_mixite(lignes):
    f, e = "ch08_tableau3.yaml", "(e) Population majoritaire"
    assert [val(lignes, f, r, e) for r in
            ("G1 Immigré·e", "G2 Descendant·e (deux parents immigrés)", "G2.5 Descendant·e (un parent immigré)", "Population majoritaire")
            ] == [29, 45, 74, 88]
    # les « 39 / 59 / 90 % » sont des sommes c + d + e, pas des cellules publiées
    sommes = []
    for r in ("G1 Immigré·e", "G2 Descendant·e (deux parents immigrés)", "G2.5 Descendant·e (un parent immigré)"):
        sommes.append(sum(val(lignes, f, r, c) for c in
                          ("(c) Conjoint G1 d’une autre origine", "(d) Conjoint G2 d’une autre origine", e)))
    assert sommes == [39, 59, 90]
    # 12 % des majoritaires en couple avec un G1 ou un G2
    assert val(lignes, f, "Population majoritaire", "(c) Conjoint G1 d’une autre origine") + \
        val(lignes, f, "Population majoritaire", "(d) Conjoint G2 d’une autre origine") == 12
    assert not [c for c in lignes if c["fichier"] == f and c["ligne"] == "Population majoritaire" and c["colonne"].startswith(("(a)", "(b)"))]


def test_temoin_e3_grands_parents(lignes):
    f = "ch08_tableau4.yaml"
    col = "Ensemble des G3 (enquête principale)"
    assert [val(lignes, f, r, col) for r in "1234"] == [56, 37, 3, 4]
    assert [val(lignes, f, r, "G3 ayant au moins un grand-parent immigré non européen (enquêtes principale et complémentaire)") for r in "1234"] == [49, 37, 5, 9]
    assert val(lignes, f, "Effectif non pondéré", col) == 778
    t6 = "ch08_tableau6.yaml"
    assert [val(lignes, t6, "4 grands-parents immigrés", c) for c in ("Turquie, Moyen-Orient", "Afrique subsaharienne", "Maghreb")] == [41, 33, 24]
    assert val(lignes, t6, "4 grands-parents immigrés", "Ensemble") == 12
    assert val(lignes, t6, "1 grand-parent immigré", "Ensemble") == 44


def test_temoin_e3_origines_et_generations(lignes):
    f1, f2 = "ch08_figure1.yaml", "ch08_figure2.yaml"
    assert val(lignes, f1, "Europe du Sud", "G3") == 56
    assert [val(lignes, f1, "Maghreb", g) for g in ("G1", "G2", "G3")] == [32, 38, 6]
    assert [val(lignes, f2, g, "Europe du Sud") for g in ("G1", "G2", "G3")] == [14, 35, 51]
    assert [val(lignes, f2, g, "Maghreb") for g in ("G1", "G2", "G3")] == [46, 48, 6]
    assert [val(lignes, f2, g, "Afrique sub.") for g in ("G1", "G2", "G3")] == [67, 29, 5]


def test_temoin_e9_segregation(lignes):
    f = "ch05_tableau1.yaml"
    c = "Forte concentration d’immigrés non européens (quintile supérieur), 2019"
    assert (val(lignes, f, "Maghreb", c), val(lignes, f, "Afrique subsaharienne", c), val(lignes, f, "Population majoritaire", c)) == (36, 51, 6)
    chom = "Fort taux de chômage (quintile supérieur), 2019"
    assert (val(lignes, f, "Maghreb", chom), val(lignes, f, "Afrique subsaharienne", chom), val(lignes, f, "Population majoritaire", chom)) == (31, 33, 10)


def test_temoin_e9_sur_chomage(lignes):
    f = "ch11_figure1.yaml"
    femme_g1_maghreb = val(lignes, f, "G1 Maghreb", "Femmes")
    assert femme_g1_maghreb == pytest.approx(11.7, abs=0.5)
    assert val(lignes, f, "G1 Maghreb", "Hommes") == pytest.approx(6, abs=0.5)
    assert val(lignes, f, "G2 Maghreb", "Hommes") == pytest.approx(6, abs=0.5)
    assert val(lignes, f, "G2 Afrique sub.", "Femmes") == pytest.approx(5.7, abs=0.5)
    assert val(lignes, f, "G1 Turquie, MO", "Femmes") == pytest.approx(10, abs=0.5)
    # 16 groupes x 2 sexes
    assert len([c for c in lignes if c["fichier"] == f]) == 32


def test_temoin_e9_discriminations(lignes):
    f, a = "ch16_tableau2.yaml", "Discriminations autodéclarées"
    assert [val(lignes, f, r, a) for r in ("Population majoritaire", "G1", "G2", "G2.5")] == [14, 24, 29, 20]
    assert [val(lignes, f, r, a) for r in ("G2 Maghreb", "G2 Afrique sub.", "G2 Europe du Sud", "G2 Autres UE 27")] == [35, 41, 12, 15]
    assert (val(lignes, f, "G1 Maghreb", a), val(lignes, f, "G1 Afrique sub.", a)) == (25, 35)
    t = "Au moins un type de discrimination"
    assert (val(lignes, f, "Population majoritaire", t), val(lignes, f, "G2 Afrique sub.", t)) == (25, 52)
    # « au moins un type » englobe les deux autres indicateurs
    for r in {c["ligne"] for c in lignes if c["fichier"] == f}:
        assert val(lignes, f, r, t) >= max(val(lignes, f, r, a), val(lignes, f, r, "Discriminations situationnelles"))


def test_temoin_e10_france_seule(lignes):
    f, c = "ch09_tableau4.yaml", "France seule"
    assert [val(lignes, f, r, c) for r in ("G1", "G2 (2 parents immigrés)", "G2 Total (G2 + G2.5)", "G2.5 (1 parent immigré)", "G3", "Population majoritaire")] == [15, 39, 48, 58, 75, 78]
    comb = "Combinaison France/autre pays"
    assert [val(lignes, f, r, comb) for r in ("G1", "G2 (2 parents immigrés)", "G2 Total (G2 + G2.5)", "G2.5 (1 parent immigré)", "G3", "Population majoritaire")] == [17, 33, 29, 23, 9, 3]


def test_anomalie_g1_ch9_signalee(lignes):
    anomalies = verifier_teo2([c for c in lignes if c["fichier"] == "ch09_tableau4.yaml"])
    assert len(anomalies) == 1 and "123" in anomalies[0]


def test_temoin_fecondite(lignes):
    f = "ch17_figure1.yaml"
    assert [val(lignes, f, "Ensemble", c) for c in ("G1", "G2", "Pop. maj.")] == [2.32, 1.87, 1.87]
    assert val(lignes, f, "Afrique sub.", "G1") == 2.84
    assert val(lignes, f, "Maghreb", "G1") == 2.80
    assert all(c["unite"] == "enfants par femme" for c in lignes if c["fichier"] == f)
