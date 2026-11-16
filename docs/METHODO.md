# Méthode

Version du 2026-11-05. Base de la page `/methode` du site. Paramètres :
`pipeline/referentiels/piscine.yaml` et `pipeline/referentiels/cohortes.yaml`
(statut `a_valider` tant que Max ne les a pas relus).

## 1. La piscine (`pipeline/qrq/piscine.py`)

Une ligne par année : stocks au 1er janvier, flux de l'année. Trois régimes :
`mesure` (2006-2022, IP 2107), `partiel` (2023-2024 : entrées seules),
`reconstruit` (1921-2005 : stocks des recensements, décès d'immigrés estimés,
flux net par différence). Entre deux recensements, de 1968 à 2005, le flux net
des immigrés suit année par année le solde migratoire du bilan, à une constante
près calée pour retomber sur le recensement suivant (`repartition_flux`) : le
solde des non-immigrés est supposé constant sur la période, et toute la
variation annuelle du solde estimé par l'Insee va aux immigrés. Ce solde annuel
est lui-même une estimation de l'Insee « à partir d'informations fragmentaires
provenant de sources diverses », recalée sur chaque recensement (Insee,
*Méthodes de calcul des populations antérieures à 1990*). Aucune série publique
des entrées exploitable (tableur, texte) n'a été trouvée avant 2006 : les
sources ONI et OMI sont des rapports annuels ou des publications non
numérisées en série. Avant 1968, le stock est interpolé
linéairement (1962 : l'arrivée des rapatriés domine le solde du bilan). Le
modèle de cohortes suit la même trajectoire. Population : bilan démographique, onglet FM
(métropole) jusqu'en 1989, FR ensuite ; avant 1946, population lue dans les
pyramides des âges et solde migratoire par différence ; de 1938 à 1945 l'écart
est un ajustement (prisonniers hors du territoire), pas une migration.

Identité tenue chaque année (testée) :
`immigrés(t+1) = immigrés(t) + entrées − sorties − décès + ajustement + non ventilé`.

Décès d'immigrés hors 2006-2022 : `r × (immigrés / population) × décès totaux`,
`r` = rapport moyen observé sur 2006-2022 (fourchette min-max affichée).

## 2. Le modèle de cohortes (`pipeline/qrq/cohortes.py`)

1911-2025, par âge révolu (0-105+) : G1, G2a (deux parents immigrés), G2b (un
parent), G3 (parents non immigrés dont au moins un G2). Chaque année :

1. **Mortalité** : quotients nationaux par âge (moyenne hommes-femmes), sans
   surmortalité par origine.
2. **Immigrés** : départs = taux × forme par âge (taux calé sur la moyenne des
   sorties Insee 2006-2021 ; forme choisie sur une grille,
   `pipeline/explo/calage_departs.py`, la plus proche de la structure par âge
   des immigrés en 2019-2020) ; arrivées = ce qu'il faut pour retomber sur le
   stock observé suivant, réparties selon le profil d'âge à l'arrivée (IP 2107,
   entrées de 2024).
3. **Naissances** : de 1998 à 2025, état civil (pays de naissance des parents)
   × deux corrections (deux parents nés à l'étranger → G2a ; un parent → G2b),
   calées sur les G2 des 0-17 ans d'IP 1910. Avant 1998, composition déduite de
   la photo de 2019-2020 : une classe d'âge en 2020 est née telles années, et sa
   part de G2 et de G3 parmi les nés en France donne la composition des
   naissances de ces années (hypothèse : survie et émigration identiques à
   celles des autres non-immigrés). G3 hors photo : proportionnel à la part des
   G2 parmi les 20-44 ans non immigrés.
4. Ni les G2 ni les G3 n'émigrent (U19).

**Condition initiale (U20)** : en 1911, 0,8 enfant d'immigré vivant par immigré
présent (inconnu). Le build recale le modèle avec 0,4 et 1,2
(`cohortes.yaml`, `sensibilite`) et exporte chaque année la fourchette des G2 et
des G3 (`g3_min`, `g3_max`…), affichée au survol des colonnes de la piscine.
Elle est large dans les années anciennes et s'éteint ensuite ; `qrq check`
vérifie qu'en 2025 elle reste à ± 0,15 point. Sensibilité des autres paramètres
libres : `pipeline/explo/sensibilite_cohortes.py`, synthèse dans
`docs/PARAMETRES.md`.

**Témoins indépendants** (non utilisés pour caler, contrôlés par `qrq check`) :
descendants mesurés en 2025 (enquête Emploi) à ± 10 % ; décès d'immigrés
estimés par l'Insee 2006-2022 à ± 15 % ; répartition des immigrés en quatre
classes d'âge aux recensements de 1990 à 2025 (Insee 2381759, tous logements)
à ± 3 points (ce témoin a aussi servi à choisir l'année de bascule du profil
d'arrivée : il n'est donc qu'à moitié indépendant). Écarts publiés dans `data/export/cohortes_calage.csv`.

**Limites connues** :

- *Un ou deux parents immigrés (U21).* Le modèle suit la convention de l'enquête
  Emploi 2019-2020 (IP 1910 : 49 % des G2 avec un seul parent immigré ; le
  modèle donne 49 % en 2020 et 48 % en 2025). En 2021, l'Insee a modifié le
  traitement des parents d'origine inconnue, ce qui réduit la part des « deux
  parents » ; les publications depuis 2021 donnent 55 % à 58 %. L'écart au
  témoin de 2025 est donc une rupture de série, pas un défaut du modèle : il
  n'existe pas de cible par âge dans la nouvelle convention. Le même changement
  réduit le nombre de descendants d'environ 3 %, ce qui explique une partie de
  l'écart au témoin des effectifs (le reste : Mayotte et les logements
  collectifs, inclus dans le modèle, exclus de l'enquête).
- *Âge des immigrés.* Avec un profil d'arrivée unique (entrées 2024), les
  jeunes adultes étaient surestimés par rapport à IP 1910 et au recensement
  (tous logements), jusqu'à 5,5 points ; aucune forme des départs ne corrigeait
  l'écart (grille de 160 formes). Le profil d'arrivée dépend désormais de
  l'époque (`arrivees` dans `cohortes.yaml`) : avant 1990, le profil de 2024
  rajeuni à l'âge médian à l'arrivée des immigrés présents en 1999 (22 ans ;
  Insee, *Les immigrés en France*, 2005, fiche 1.7). Écart au recensement : 2,6
  points au plus de 1990 à 2025 (contrôlé à ± 3) ; à IP 1910 : 4,3 points au
  plus par classe fine (logement ordinaire). Contrepartie : le témoin des décès
  d'immigrés passe de −5 % à −13 % (le modèle applique la mortalité nationale
  par âge ; l'Insee estime ces décès avec sa propre méthode). Aucune source
  publique ne donne l'âge à l'arrivée par période d'arrivée
  (`explo/profil_arrivee.py`). Effet sur la piscine : les totaux des G1 sont
  imposés, et les parts des générations bougent de moins de 0,1 point.
- La G3 au-delà de 60 ans n'a aucune cible.

## 3. TeO2 (`pipeline/referentiels/teo2/`)

671 cellules ressaisies depuis les images du livre, une référence par cellule
(chapitre, tableau ou figure, champ, image), relues deux fois ; valeurs lues sur
graphique marquées `approx` avec leur précision. `qrq check` signale les
anomalies de la source (ch. 9, tableau 4 : la ligne G1 somme à 123).
