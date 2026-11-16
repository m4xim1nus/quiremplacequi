# Paramètres de la piscine : fiche de relecture

**Validée par Max le 2026-11-16** : toutes les recommandations retenues (☑).

Fiche à relire par Max pour passer `pipeline/referentiels/piscine.yaml` et
`pipeline/referentiels/cohortes.yaml` du statut `a_valider` à `valide`. Une ligne par
choix : sa valeur, d'où elle vient, ce qu'elle change, une recommandation. Cocher
ou corriger dans la colonne « Décision ».

Les chiffres d'effet viennent de `pipeline/explo/sensibilite_cohortes.py` (2026-11-16) :
chaque variante est recalée comme au build, puis comparée à la référence.

## 1. Ce qu'il faut retenir

- **Les parts affichées pour 2025 ne dépendent pas des paramètres libres.** Aucune
  variante testée ne déplace les G2 en 2025, et les G3 de 0,12 point au plus
  (référence : 6,4 % ; 6,0 % ; 10,2 %). Le modèle est tenu par ses
  cibles (IP 1910 en 2019-2020, sorties Insee), pas par des réglages.
- Le seul effet visible concerne les années anciennes : la part de G2 vivants en
  1911, qu'on ignore, fait varier les G3 de 1968 de 5,3 % à 6,7 %.
- Les autres choix sont de l'affichage (échelle, années, libellés des événements).
  Les libellés sont les seuls choix de **formulation**.

## 2. Modèle de cohortes (`cohortes.yaml`)

| Paramètre | Valeur | D'où elle vient | Effet mesuré | Recommandation | Décision |
|---|---|---|---|---|---|
| `debut` | 1911 | Premier stock d'immigrés publié (Insee 6793226) | Fixe le point de départ ; la piscine s'affiche dès 1921 | Garder | ☑ |
| `initial.g2_rapport_g1` | 0,8 | Inconnu : hypothèse, 0,8 enfant vivant par immigré présent | De 0,4 à 1,2 : G3 en 1968 de 5,3 % à 6,7 % (réf. 6,0 %) ; G3 en 2025 à ± 0,12 pt | Garder, et afficher la fourchette de 1968 comme incertitude (nouveau code U) | ☑ |
| `naissances.correction_deux` | calé : 0,87 | Les naissances par pays de naissance des parents comptent les Français nés à l'étranger ; corrigé pour retrouver les G2 à deux parents des 0-17 ans d'IP 1910 | Cible atteinte par construction | Garder (pas de réglage manuel) | ☑ |
| `naissances.correction_un` | calé : 0,60 | Idem, G2 à un parent | Idem | Garder | ☑ |
| `naissances.beta_ancien`, `beta_recent` | calés : 1,60 et 1,34 | G3 hors de la photo de 2019-2020, proportionnel à la part des G2 parmi les 20-44 ans | Calés sur les bords de la photo | Garder | ☑ |
| `departs.taux` | calé : 0,94 % par an | Moyenne des sorties Insee 2006-2021 | — | Garder | ☑ |
| `departs.forme` | jeunes adultes et 55-69 ans × 3 | Grille de 32 formes (`explo/calage_departs.py`) : la plus proche des parts d'immigrés par âge d'IP 1910 | Forme plate : écart max à IP 1910 de 1,16 à 1,52 pt ; parts de 2025 inchangées | Garder | ☑ |
| `calage.sorties` | 2006-2021 (2022 exclu) | 2022 atypique dans la source (U2) | 2022 inclus : taux 0,89 %, écart à IP 1910 1,31 pt ; parts inchangées | Garder l'exclusion | ☑ |
| `calage.annee_ip1910` | 2020 | Milieu de la collecte 2019-2020 | — | Garder | ☑ |

Écart connu, non résolu par un paramètre : la part des G2 à un seul parent est de
48 % dans le modèle, contre 55 % selon l'Insee en 2025. Aucune variante ne le
réduit. Il vient des cibles (IP 1910, logement ordinaire), pas d'un réglage. Il est
déjà dans `BACKLOG.md`.

## 3. Piscine (`piscine.yaml`)

| Paramètre | Valeur | D'où elle vient | Effet | Recommandation | Décision |
|---|---|---|---|---|---|
| `echelle` | 10 000 personnes par particule | Lisibilité : ≈ 6 900 particules en 2025 | Affichage seulement (les comptes sont exacts à l'arrondi de la particule près, testé) | Garder | ☑ |
| `debut` / `fin` | 1921 / 2025 | Vague italienne et polonaise visible ; dernier stock publié | Affichage | Garder | ☑ |
| Avant 2006 : interpolation linéaire entre recensements | — | Pas de flux annuels d'immigrés avant 2006 | Le flux net est constant entre deux recensements : **1974 ne se voit pas** dans la piscine | Garder, et le dire sur la frise (régime « reconstruit », déjà marqué) | ☑ |
| Dates de collecte assimilées au 1er janvier | — | Recensements de mars ou février | Décalage de 2 à 3 mois, invisible à l'échelle | Garder (documenté) | ☑ |
| `bilan_metropole_jusqua` | 1989 | Suivre le champ des stocks d'immigrés (métropole jusqu'en 1982) | Évite un faux saut de population ; l'entrée des DOM tombe en 1990 (U6) | Garder | ☑ |
| `deces_immigres` hors 2006-2022 | r × part d'immigrés × décès | Rapport r observé de 2006 à 2022 : 0,98 à 1,12 (moyenne 1,05) | Fourchette affichée sur les décès estimés | Garder | ☑ |
| `saisies.effet_collecte_2024_immigres` | 242 000 | Note méthodologique Insee du 04/06/2026, p. 4 (citation dans le YAML) | Ajustement de collecte, pas un flux | Garder | ☑ |

## 4. Événements de la frise (formulations)

Ce sont les seuls textes du modèle. À valider mot à mot.

| Année | Libellé actuel | Décision |
|---|---|---|
| 1931 | Crise des années 1930 : retours et expulsions, notamment de travailleurs polonais | ☑ |
| 1939 | Seconde Guerre mondiale : pas de recensement jusqu'en 1946 ; les pyramides ne comptent pas les prisonniers hors du territoire (ajustement, pas migration) | ☑ |
| 1945 | Avant 1946, population lue dans les pyramides des âges ; solde migratoire par différence | ☑ |
| 1962 | Indépendance de l'Algérie : arrivée des rapatriés, pour la plupart non immigrés | ☑ |
| 1974 | Suspension de l'immigration de travail (juillet 1974) | ☑ |
| 1990 | Changement de champ : les départements d'outre-mer entrent dans les séries | ☑ |
| 2006 | Début des flux mesurés par l'Insee (entrées, sorties, décès d'immigrés) | ☑ |
| 2013 | Mayotte entre dans le champ des stocks au 1er janvier 2014 | ☑ |
| 2021 | Pas d'enquête annuelle de recensement en 2021 ; données 2019-2023 réajustées | ☑ |
| 2023 | Sorties pas encore publiées : flux de 2023 et 2024 incomplets | ☑ |
| 2024 | Rupture de série : nouveau protocole de collecte du recensement | ☑ |

Questions ouvertes :

- **Ajouter des jalons ?** Par exemple 1927 (loi sur la nationalité), 1945
  (ordonnance sur l'entrée et le séjour), 1976 (regroupement familial). Ma
  recommandation : non en v1. La frise de la piscine sert à expliquer des
  **mouvements des courbes**, pas l'histoire des politiques ; les jalons de discours
  et de lois relèvent de B4.
- **1962** : ajouter un ordre de grandeur des rapatriés ? Seulement si une source
  agrégée publique le donne ; sinon garder le libellé qualitatif.

## 5. Après validation

1. `statut: valide` dans les deux YAML (le site affiche alors les paramètres comme
   validés).
2. Si la fourchette de 1968 est retenue : un code `U20` dans `incertitudes.yaml`,
   affiché sur la piscine pour les années de 1921 à 1990 environ.
3. Cocher l'étape 2 dans `ROADMAP.md`.

## 6. Proposition du 2026-11-16 : le flux net avant 2006 (à valider)

| Paramètre | Valeur | D'où elle vient | Effet | Recommandation | Décision |
|---|---|---|---|---|---|
| `repartition_flux` (`piscine.yaml`) | `solde_bilan` dès 1968 | Solde migratoire annuel du bilan Insee, lui-même estimé « à partir d'informations fragmentaires provenant de sources diverses » et recalé sur chaque recensement. Aucune série publique d'entrées exploitable trouvée avant 2006 (ONI et OMI : rapports annuels non numérisés en série ; Ined : à partir de 1994 environ, non vérifié) | Le flux net des immigrés suit le solde du bilan à une constante près : 1973 : 123 000, 1974 : 47 000, 1975 : 39 000 (avant : ≈ 134 000, 135 000, 65 000, lissés). Le solde des non-immigrés devient constant entre deux recensements ; auparavant, il absorbait la cassure (−104 000 en 1974, un artefact). Parts des générations inchangées (au centième près) | Retenir `solde_bilan` dès 1968. Avant 1968 : garder le lissage (en 1962, le solde du bilan est dominé par les rapatriés, non immigrés pour la plupart) | ☐ |

Variante écartée : flux net des immigrés proportionnel au solde du bilan.
Résultats proches, mais le solde des non-immigrés varie alors sans raison
documentée (`pipeline/explo/flux_avant_2006.py`).
