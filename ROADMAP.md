# Roadmap

Projet solo, sans calendrier engageant. Chaque étape se termine par un
**livrable relu par Max** avant de passer à la suivante. Les idées non
planifiées vont dans `BACKLOG.md`. Codes des modules : `docs/CADRAGE.md` §4.

## Étape 0 : cadrage ✅ (2026-11-04)

Nom, posture (« nommer, puis mesurer »), périmètre v1, stack alignée sur
2p2e, dépôt privé : validés par Max. Règles dures (`CLAUDE.md`), cadrage
(`docs/CADRAGE.md`), proposition de conception de la piscine
(`docs/PISCINE.md`), squelette du dépôt.

## Étape 1 : spike sources ✅ (2026-11-05)

Vérifier, pour chaque module de la v1, ce qui existe, sous quelle forme et
avec quelles limites. Quatre familles, un rapport chacune dans `docs/spike/` :

- [x] `insee.md` : les données Insee contemporaines (bilans, stocks, flux,
  naissances par origine des parents, descendants, projections). Question
  clé : les 4 vannes de la piscine, immigrés et non-immigrés, 1968-2025.
- [x] `historique.md` : la série longue 1851-1968 et les vagues (B1, B2,
  B3, B5), les naturalisations, les migrations juives (U10), le repérage des
  discours (B4).
- [x] `teo2.md` : générations, mixité et inégalités (E1-E3, E9-E10, F2),
  paramètres de mixité de la piscine, accès aux microdonnées.
- [x] `heran.md` : le catalogue des graphiques d'Héran, les 30 questions, les
  cours du Collège de France, les contradicteurs.

**Livrable** : `docs/SOURCES.md`. Verdict : GO pour B1, B3, B5, E1-E3, F2 et
le robinet des naissances ; partiel pour la piscine (4 vannes mesurées de 2006
à 2022 seulement), B2, E9-E10. Quatre décisions de Max (§5). Restent ouvertes
les questions de `docs/CADRAGE.md` §9 et `docs/PISCINE.md` §9.

## Étape 2 : pipeline et piscine v0 ✅ (2026-11-16)

- [x] Package `qrq` (`download` → `build` → `check`) : 7 tableurs Insee, export
  `data/export/` (stock 1911-2025, pays 1968-2021, nationalités 1901-2020,
  bilans, flux 2006-2024, naissances par origine des parents, piscine).
  15 contrôles (identités comptables, champs, témoins), tests pytest.
- [x] Registres `incertitudes.yaml` (U1-U18) et `piscine.yaml` (paramètres à
  valider).
- [x] Site SvelteKit (copié de 2p2e) et prototype de la piscine v0 sur
  `/piscine` : 1968-2025, 4 vannes, 2 teintes, régimes mesuré / partiel /
  reconstruit affichés, ajustements de champ et de collecte visibles.
- [x] Revue de Max de la v0 (2026-11-05) : liquides non miscibles, débits visibles, descendants.
- [x] Piscine v1 : eau décantée (couches) ou mélangée, tuyaux d'épaisseur ∝ débit, cinq teintes
  (G1, G2 deux parents, G2 un parent, G3, autres) par le modèle de cohortes
  (`pipeline/qrq/cohortes.py`, 1911-2025, calé sur IP 1910 et les sorties Insee, contrôlé par les
  descendants 2025 et les décès d'immigrés).
- [x] Saisie référencée de TeO2 (506 cellules, `pipeline/referentiels/teo2/`).
- [x] Pages `/temps-long` (B1, B2, B3, B5) et `/generations` (E1-E3, E9-E10, F2, encadré OID),
  `/limites`, `/methode`, `/donnees` ; piscine de 1921 à 2025.
- [x] Relecture factuelle indépendante de tous les textes (2026-11-05) : 4 bloquants, 13 points à
  corriger, tous traités (cadrage de la vitesse des vagues, nationalité des enfants, encadré OID
  réduit à ce qui est établi, populations explicitées, paradoxe transversal…).
- [x] Revue de Max (2026-11-06) : pages trop « article », piscine à clarifier.
- [x] Piscine v1.1 : colonnes verticales, rubans haut → bas, frise des parts, compteur cumulé ;
  pages Générations, Le temps long et La piscine allégées (sommaire en réponses, « Le détail »
  replié).
- [x] Revue de Max (2026-11-16) : piscine v1.1 et phrases « réponse » validées ; couleurs des
  générations reprises (G2 et G3 proches de « autres », « autres » ni blanc ni presque blanc).
- [x] Revue des paramètres par Max (2026-11-16) : fiche `docs/PARAMETRES.md`, recommandations
  retenues ; `piscine.yaml` et `cohortes.yaml` en `valide`, fourchette de la condition initiale
  calculée au build et affichée (U20).
- [x] Graphiques bruts de relecture de B1 et B2 (`pipeline/explo/relecture_b1_b2.py`, 7 figures) :
  rien à corriger ; l'emboîtement des pays de naissance entre dans `qrq check`.

**Livrable** : piscine v0 relue par Max, paramètres validés.

## Étape 3 : modèle de la piscine et modules E, F2 ✅ (2026-11-16)

Le modèle de cohortes, la saisie de TeO2 et le curseur F2 existent depuis
l'étape 2. L'étape 3 traite ce qui reste de leurs limites connues.

- [x] Écart des G2 à un seul parent (48 % contre 55 %) : rupture de série de
  l'enquête Emploi en 2021 (traitement des parents d'origine inconnue),
  documentée (U21) ; le modèle garde la convention de 2019-2020.
- [x] Âge des immigrés : nouveau témoin, les recensements de 2007 à 2025 (tous
  logements, Insee 2381759), contrôlé à ± 5 points. Les jeunes adultes restent
  surestimés (≈ +2 points) ; la cause est le profil d'âge à l'arrivée, unique.
- [x] Flux avant 2006 : aucune série publique exploitable des entrées
  trouvée avant 2006. De 1968
  à 2005, le flux net des immigrés suit le solde migratoire annuel du bilan
  Insee (1974 se voit) ; le solde des non-immigrés n'absorbe plus la cassure.
  Paramètre validé par Max (`docs/PARAMETRES.md` §6).
- [x] Profil d'âge à l'arrivée par époque : aucune série publique par période
  d'arrivée ; avant 1990, profil de 2024 rajeuni à l'âge médian à l'arrivée des
  immigrés présents en 1999 (22 ans, Insee 2005). Âges au recensement à 2,6
  points au plus (5,5 avant) ; témoin des décès à −13 % (−5 % avant). Validé
  par Max (`docs/PARAMETRES.md` §7).
- [x] TeO2 : chapitre 7, figures 3 et 4 (160 cellules, seconde lecture
  indépendante identique), figure 4 affichée dans le détail de « Avec qui
  vivent-ils ? » ; chapitre 11 : la contradiction entre le §35 et la figure 1
  (et sa note de lecture) est saisie et expliquée sur la page.
- [x] Relecture factuelle indépendante (2026-11-16) : 1 bloquant, 14 points à
  corriger, 11 suggestions. Corrigés : le bloquant (hausse du stock d'immigrés :
  champ et collecte de 2024), la concession sur le solde migratoire premier
  moteur de la croissance (absente du site), les naissances estimées marquées,
  le droit du sol, la mixité « teinte se diluera » remplacée par les chiffres,
  les champs des chiffres TeO2, la fausse précision du sur-chômage, la ligne
  incohérente du ch. 9, le solde des non-immigrés « par différence », l'écart
  maximal du modèle. Restent pour Max : voir `BACKLOG.md` (2026-11-16).
- [x] Revue de Max des formulations modifiées par la relecture (2026-11-16) ;
  six suggestions appliquées.
- [x] Note de l'OID (21/9/2026) lue en entier : encadré réécrit à partir de ses
  hypothèses citées (définition, aucune émigration, unions « au hasard ») et des
  flux Insee ; valeurs saisies dans `referentiels/contradicteurs.yaml`.
- [x] Événement 1931 sourcé (Musée national de l'histoire de l'immigration) ;
  mention des Polonais retirée faute de source vérifiée.
- [x] Revue de Max (2026-11-16) : profil d'arrivée par époque, encadré OID
  réécrit, libellé de 1931 validés.

**Livrable** : piscine v2 et pages E, F2 relues par Max.

## Étape 4 : site v1 ✅ (2026-11-16)

Le contenu de la v1 existe (piscine, temps long, générations, méthode,
limites, données). L'étape 4 lui donne une forme propre, le rend publiable et
le met en ligne.

- [x] Conception (`docs/CONCEPTION.md`) : échelle limnimétrique, bleu réservé
  aux données, ocre pour les repères, Barlow Semi Condensed et Atkinson
  Hyperlegible Next ; validée par Max (2026-11-16).
- [x] Application, premier passage : jetons et polices auto-hébergées, en-tête
  et pied, accueil avec l'échelle lue dans les données, cadres de figures,
  sommaires, encadrés ; mentions « brouillon » retirées ; plus d'orange codant
  une origine (temps long) ni de rouge.
- [x] Application, second passage (revue de Max) : piscine (« Faire ressortir »
  en eau mélangée, « Voir l'eau de X se renouveler »), rampe des générations
  élargie, arrondis à 2 px partout.
- [x] Accessibilité : contrastes au seuil WCAG (gris, ocre du focus), tableau
  annuel de la piscine, compteur muet pendant la lecture ; poids : 55 Ko
  compressés pour la page la plus lourde. Mobile : à vérifier visuellement.
- [x] Page « À propos » : dépôt GitHub, contact (alias dédié), licences (MIT,
  CC BY 4.0), vie privée.
- [x] Image de partage (Open Graph), générée depuis les données
  (`site/scripts/partage.py`) ; en-têtes de sécurité en place (`_headers`).
- [x] Vérification visuelle par Max (piscine : couleurs, « Suivre l'eau »).
- [x] Relecture finale (2026-11-16) : aucune erreur de chiffre ni de citation ;
  encadré OID complété, licence des contenus, régime « partiel » documenté.
- [x] Mise en ligne (`docs/DEPLOIEMENT.md`) : identité des commits réécrite,
  dépôt public, Cloudflare Pages sur `quiremplacequi.technoperchoir.fr`,
  vérifications en ligne passées ; `CHANGELOG.md` et tag `v1.0.0`.

**Livrable** : site v1 en ligne (2026-11-16).


## Cycle 2 : l'espace et la nature des migrations (C, D)

Lancé par Max le 2026-11-16. Deux nouvelles pages, ajustées par la lecture
de *Parlons immigration en 30 questions* (Héran, 3e éd., 2021 ; lignes du
2026-11-16 dans `BACKLOG.md`) et par le catalogue des graphiques d'Héran
(`docs/spike/heran.md`). Les pages existantes ne reçoivent que des renvois :
on ne complique pas la piscine. Le livre ne sert jamais de source : chaque
chiffre est retrouvé à la source primaire.

- [ ] **Spike sources** (`docs/SOURCES.md` §6) : ministère de l'Intérieur
  (DSED, *Les étrangers en France. Rapport au Parlement* ; premiers titres
  par motif 2005-2025 ; demandes d'asile ; calendrier provisoire du
  21 janvier, consolidé du 15 juin ; Elipa 2, *Infos Migrations* n° 98) ;
  Ofpra (série longue de l'asile) ; Eurostat (asile et décisions, soldes
  naturel et migratoire, population née à l'étranger) ; ONU, *International
  Migrant Stock* 2024 (stocks par pays et matrice origine-destination) ;
  OCDE, *Perspectives des migrations internationales* (entrées permanentes
  par catégorie). Pour chacune : format, licence, accès par script, ruptures.
  Les chiffres du livre (France 14e des demandes d'asile par habitant et 16e
  des décisions positives, 2014-2020) servent de témoins, pas de valeurs.
- [ ] **Page « nature des migrations » (D)** :
  - D1 : premiers titres de séjour par motif, 2005-2025, en petits multiples,
    absolu ↔ pour 10 000 habitants, et la décomposition de la hausse ;
  - D2 : migration familiale ≠ regroupement familial ;
  - D3 : le parcours de l'asile sans double compte (demandes, décisions,
    titres de réfugié ne s'additionnent jamais) ;
  - D4 : réconciliation des entrées Insee et des titres (U11) : Européens,
    Français nés à l'étranger, mineurs, irréguliers ; une « entrée » n'est pas
    toujours un nouvel immigré (Insee Focus n° 145) ;
  - D5 : ce qu'il y a dans le solde migratoire : immigrés et non-immigrés
    séparés, 2006-2024 (déjà dans `flux.csv`) ;
  - U7 enrichie : le stock irrégulier se régularise au fil de l'eau (Elipa 2),
    fourchette seulement ;
  - statut provisoire ou consolidé affiché sous les graphiques ;
  - D6 (lois sur la courbe des titres, *policy gap*) : seulement avec une
    règle fixe de sélection des lois, validée par Max.
- [ ] **Page « la France parmi les autres » (C)** :
  - C1 : part d'immigrés par pays, avec la bascule de définition (ONU, né à
    l'étranger ; Insee, né étranger à l'étranger ; U12) ;
  - C2 : progression depuis 2000, et les soldes naturel et migratoire en ‰
    de l'Allemagne, de l'Espagne et de la France ;
  - C3 : entrées par catégorie pour 10 000 habitants (OCDE) ;
  - C4 et C5 : l'asile, demandes et décisions, absolu ↔ pour 10 000
    habitants, et « prendre sa part » (poids démographique et économique) ;
  - C7 : la bosse migratoire, et l'émigration subsaharienne mesurée (part
    des émigrés, part restée dans la région) par la matrice de l'ONU. Les
    projections à 2050 restent hors du cycle.
- [ ] **Renvois ailleurs, sans plus** : depuis la vanne d'arrivée de la
  piscine vers D4, depuis l'accueil vers les deux pages, sources nouvelles
  sur Méthode et Données.
- [ ] Relecture factuelle indépendante, revue de Max, `CHANGELOG.md` et tag.

**Livrable** : les pages C et D en ligne, relues par Max.

**À trancher par Max en cours de route** : les noms des deux pages ; la
règle de sélection des lois pour D6 ; la Drees (aide médicale d'État) comme
source de la fourchette des irréguliers, hors de la liste des sources
admises ; la Banque mondiale, citée par le livre, remplacée par la matrice
de l'ONU (même usage, source admise).

## Cycle 3 : les naissances et le mot « remplacement » (pressenti)

Une nouvelle page « Les naissances », et quelques retouches ailleurs.

- F3 et E7 : la fécondité en poids × taux, l'indicateur national avec et
  sans les immigrées, la descendance finale par génération (la convergence),
  l'incertitude de la fécondité d'avant migration (Toulemon 2004) ; trois
  niveaux jamais mêlés : naissances, indicateur conjoncturel, descendance
  finale. Seuil de remplacement sourcé (le livre dit « deux enfants »).
- Le robinet des naissances : mère immigrée, parent né à l'étranger, deux
  parents immigrés, trois notions distinctes ; légende de la piscine
  retouchée en conséquence.
- F4 : encadré « migrations de remplacement » sur la page, à partir du
  rapport de l'ONU de 2000 lu en entier (ses scénarios, sa conclusion sur le
  vieillissement, le sens des démographes) et de son détournement. **Pas de
  contrefactuel au cycle 3** : refaire « sans migrations depuis 1974 » avec
  le modèle de cohortes est une projection à rebours, qui demande la même
  mise en scène et les mêmes garde-fous que F1 ; il ira avec F1.
- Retouches : encadré Méthode « pourquoi ces catégories » (loi de 1978,
  Cnil) ; incertitude sur la sous-déclaration de l'ascendance aux
  recensements (sens : le chiffre réel est plus haut, à dire).

## Ensuite

Les projections (F1), avec les contrefactuels de la piscine et la
contre-projection de l'OID ; B2 en petits multiples, B3 « débuts
spectaculaires » ; l'intégration par cohorte, la binationalité et l'habitat
(E) ; la rhétorique (G) ; la frise des discours (B4). Le coût de
l'immigration et la religion restent hors périmètre sauf décision de Max.
