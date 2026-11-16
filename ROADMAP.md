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

- [x] **Spike sources** (`docs/SOURCES.md` §6) : ministère de l'Intérieur
  par data.gouv.fr (son site refuse les scripts), Eurostat et OCDE par leurs
  API SDMX. ONU et Elipa 2 inaccessibles aux scripts : C7 et U7 reportés.
  Écart du livre pour 2017 expliqué (millésime) : pas de témoin tiré du livre.
- [x] **Pipeline** : `titres.py` (DSED, 2011-2024, raccord exact des deux
  sources contrôlé), `europe.py` (Eurostat, OCDE), entrées par origine (IP
  2107) ; 14 contrôles nouveaux dans `qrq check` ; U11 et U12 traitées, U22
  (solde Eurostat avec ajustement) et U23 (entrées « standardisées » de
  l'OCDE) ajoutées.
- [x] **Page « Les arrivées » (`/arrivees`, D)** : D1 titres par motif
  2011-2024 (petits multiples, nombre ↔ pour 10 000, décomposition de la
  hausse, Britanniques et Brexit séparés) ; D2 famille (trois catégories,
  regroupement familial situé) ; D3 étapes de l'asile sans addition ; D4
  entrées Insee et titres côte à côte (nés en Europe, non-immigrés) ; D5
  soldes des immigrés et des non-immigrés 2006-2022. Statut sous chaque
  graphique. D6 renvoyé à B4 (lois et discours ensemble).
- [x] **Page « Ailleurs » (`/ailleurs`, C)** : C1 part des nés à l'étranger
  (31 pays, France en ocre, définition Insee à côté) ; C2 hausse 2015-2025 et
  soldes naturel et migratoire en ‰ depuis 1960 (France, Allemagne, Espagne,
  Italie) ; C3 entrées permanentes par catégorie pour 10 000 habitants (OCDE,
  moyenne sur dix ans) ; C4-C5 asile, nombre ↔ pour 10 000, et « prendre sa
  part ». C7 (bosse migratoire) reporté : ONU inaccessible aux scripts.
- [x] **Renvois** : navigation, deux portes sur l'accueil, piscine → D4,
  Méthode (section « Les arrivées et les comparaisons »), Données (licences
  par source).
- [ ] Relecture factuelle indépendante.
- [ ] Revue de Max, `CHANGELOG.md` et tag.

**Livrable** : les pages C et D en ligne, relues par Max.

**Tranché en autonomie, à relire par Max** (`docs/SOURCES.md` §6) : noms des
pages ; D6 avec B4 ; Britanniques séparés ; périodes de comparaison (asile :
onze dernières années ; OCDE : dix ans). **Reste à Max** : la Drees comme
source de la fourchette des irréguliers (hors liste des sources admises) ;
une saisie manuelle de l'ONU pour C7, puisque les scripts sont refusés.

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
