# La piscine : proposition de conception

Version du 2026-11-05 : proposition de Claude, à discuter avec Max. Les
valeurs citées viennent du spike des sources (`docs/SOURCES.md`, détail dans
`docs/spike/insee.md`).

## 1. L'image

Toute la population résidant en France est une **piscine dont l'eau se
renouvelle en permanence**. Elle a quatre vannes : deux qui remplissent (les
naissances, les arrivées) et deux qui vident (les décès, les départs). La
teinte de l'eau dit la **distance à la migration** : immigré (G1), enfant
d'immigré (G2), petit-enfant (G3), et le reste. Les unions mixtes mélangent
les teintes à la génération suivante. Max a confirmé (2026-11-04) que c'est
l'une des visualisations qu'il envisage, et qu'elle demande un travail d'UI/UX
et de fond.

Ce n'est pas une image d'Héran : le spike ne l'a trouvée ni chez lui ni chez
Le Bras. Héran se méfie même des métaphores aquatiques, qui « transpliquent »
(cours du 3/12/2021). Le site l'assume donc comme **sa** proposition, et comme
une **comptabilité** (ce qui entre, ce qui sort, ce qui reste), pas comme une
explication des migrations.

## 2. Ce qu'elle doit faire comprendre, dans l'ordre

1. **Toute population se remplace.** Les naissances et les décès (726 000 et
   675 000 en 2022, soit ≈ 1 % de l'eau chacun) renouvellent toute la piscine en un
   siècle environ, avec ou sans immigration. Le mot « remplacement » décrit
   d'abord la condition de toute population.
2. **L'immigré n'a pas de robinet « naissances ».** Le stock d'immigrés ne
   grossit que par les arrivées ; il se vide par les décès et les départs.
   Leurs enfants entrent par le robinet commun, nés en France, avec une autre
   teinte. C'est l'identité comptable du projet, rendue visible : la
   **baignoire** (le stock d'immigrés seul) est la première scène.
3. **Les teintes se diluent au lieu de former un bloc.** La G2 naît souvent
   d'un seul parent immigré ; la G3 a le plus souvent un ou deux
   grands-parents immigrés sur quatre. Les vagues passées (Italiens,
   Polonais, Espagnols, Portugais) montent, plafonnent, puis s'écoulent par
   les décès et les retours, pendant que leurs descendants se répartissent
   dans toute l'eau.

### L'objection forte, à affronter dans la piscine même

L'argument 1 est vrai mais faible : un contradicteur répondra que tout le
monde meurt, et que la question est de savoir **de qui naissent les
enfants**. C'est la statistique favorite de la thèse adverse : la part des
naissances dont au moins un parent est né à l'étranger. La piscine doit donc
montrer **ce qui coule par le robinet « naissances »** :

- la part des naissances par origine des parents (deux parents nés à
  l'étranger, un seul, aucun), mesurée chaque année par l'Insee depuis 1998 :
  en 2025, 19,4 % des naissances ont deux parents nés à l'étranger et 15,1 %
  un seul. « Né à l'étranger » n'est pas « immigré » (les Français nés à
  l'étranger y sont comptés) ;
- le fait que les enfants de couples mixtes y sont comptés, et que leurs
  propres enfants auront trois grands-parents sur quatre nés en France ;
- la convergence de la fécondité dès la G2 (TeO2 ch. 17) : le robinet ne
  « pompe » pas plus fort pour une teinte d'une génération à l'autre.

C'est ce qui rend la piscine supérieure au discours : elle ne nie pas le
chiffre adverse, elle le place dans le cycle complet des générations.

## 3. Deux arrangements des mêmes particules

Chaque particule représente un nombre fixe de personnes (par exemple 1
particule = 10 000 personnes : ≈ 6 900 particules en 2025, ≈ 3 600 en 1851 ;
en 2022, 73 naissances, 68 décès, 49 arrivées dont 38 d'immigrés, et 22
 départs par an à l'écran). Les compteurs affichent
les valeurs exactes, et les particules servent à illustrer.

**a. La piscine** (vue d'ensemble, scènes 1 à 3). Un bassin vu en coupe, avec
les vannes sur les bords. L'eau s'agite doucement ; le niveau suit la
population. C'est l'image d'accueil.

**b. La pyramide vivante** (vue analytique). Les mêmes particules se
rangent par âge : la hauteur donne l'âge, la largeur l'effectif à cet âge, ce
qui fait une pyramide des âges qui *coule*. Les naissances entrent par le fond
(âge 0). L'eau monte avec le temps, d'un an par an. Les décès s'évaporent
surtout en haut. Les arrivées entrent à mi-hauteur (≈ 20-35 ans). Une vague
apparaît alors comme une **bande colorée qui monte et s'évapore** : les
Italiens de l'entre-deux-guerres arrivent jeunes en 1925 et atteignent le
haut vers 1990. Leurs enfants (une teinte plus claire) sont déjà répartis en
dessous, et leurs petits-enfants plus bas encore. **Le tarissement d'une vague
se lit sans un mot.**

Le passage d'un arrangement à l'autre se fait par une transition animée des
mêmes particules. Le lecteur comprend que c'est la même eau.

```
  a. piscine                         b. pyramide vivante
  naissances ▼   arrivées ▼          âge
  ┌─────────────────────────┐        100 ┊        ·  ·        ┊  ← décès (évaporation)
  │ ~~~~~~~~~~~~~~~~~~~~~~~ │         80 ┊     ░░░░▒▒░░░      ┊
  │ ░░▒░░░░░▓░░░░▒░░░░░░▒░░ │         60 ┊   ░░░░▒▓▒░░░░░    ┊
  │ ░░░░▒░░░░░░░▓▓░░░░▒░░░░ │         40 ┊  ░░░▓▓▓▒▒░░░░░░   ┊  ← arrivées (≈ 25 ans)
  │ ░▒░░░░▓░░░░░░░░▒░░░░░░░ │         20 ┊  ░░░▒▒▒░░░░░░░░   ┊
  └─────────────────────────┘          0 ┊ ░░░░▒░░░░░░░░░░░  ┊  ← naissances
  décès ▼        départs ▼                  ▓ G1   ▒ G2   ░ autres
```

## 4. Le récit (scrollytelling), puis le bac à sable

1. **La baignoire** : les seuls immigrés, de 1968 à 2025. Trois vannes,
   aucune naissance. Le compteur du stock et sa part.
2. **La piscine** : toute la population, avec le robinet des naissances, qui
   débite bien plus que celui des arrivées (726 000 naissances contre 375 000
   arrivées d'immigrés en 2022).
3. **Ce qui coule par le robinet** : les naissances par origine des parents,
   l'objection forte (§2) et sa réponse.
4. **La pyramide vivante** : les teintes se diluent, génération après
   génération.
5. **Une vague qui se tarit** (1851-2025) : la vague italienne ou polonaise,
   d'un bout à l'autre, et ce qu'il en reste (B5).
6. **Aujourd'hui** : les immigrations postcoloniales sont plus récentes ;
   leur G3 est jeune. Les données montrent le mélange en cours (TeO2) et
   ne tranchent pas encore la suite. C'est un précédent, pas une preuve.
7. **À vous** (cycle 2) : choisir une année, mettre l'immigration à zéro
   après 1974 ou après 2000, ou faire varier le solde migratoire, la
   fécondité et la mixité jusqu'en 2070.

Commandes permanentes : une frise du temps (lecture, pause, vitesse, saut aux
années repères), la bascule de l'arrangement, la bascule absolu ↔ part, et la
lecture d'une année au survol (les quatre débits et la composition).

## 5. Encodage visuel

- **Teinte = génération, pas origine.** Une seule famille de couleurs,
  graduée du plus saturé (G1) au plus clair (G3), qui se fond dans la teinte
  neutre de l'eau. Aucune palette par origine dans la piscine : une vague
  (Italiens, Algériens…) n'est mise en évidence qu'à la demande, par un
  contour ou un halo, jamais par une couleur permanente.
- **Variante à tester** : une teinte continue, égale à la **part des
  ascendants nés à l'étranger** (sur deux parents, puis sur quatre
  grands-parents). Les catégories G2/G3 disparaissent alors au profit d'un
  dégradé, ce qui est l'argument même contre l'idée de deux blocs. C'est plus
  juste visuellement, mais c'est un modèle et non une catégorie de la
  statistique. **À trancher sur maquette.**
- Le risque de la dilution est de suggérer que l'origine *doit* s'effacer
  (une norme assimilationniste). Le texte dit le contraire : la dilution est
  généalogique, pas identitaire. TeO2 montre que les identifications
  multiples persistent, et que la saillance des origines est en partie
  produite par les discriminations (E9-E10).
- **Incertitude dans l'image** : la vanne « départs » est floue (U2) ; avant
  1968, les particules changent d'étiquette (on compte alors des étrangers,
  U9) ; la rupture de 2024 est un trait sur la frise (U5) ; les projections
  sont hachurées (U16) ; un badge « modèle » apparaît dès que l'image n'est
  plus observée.
- **Accessibilité** : `prefers-reduced-motion` donne des états fixes par
  scène. Chaque scène a une phrase « Lecture : … » et un tableau équivalent.
  Les teintes passent le contrôle daltonisme et le contraste.

## 6. Le modèle derrière l'image

Ce que la statistique publique observe ne suffit pas à colorier chaque goutte.
La piscine sera donc un **modèle de cohortes** calé sur les observations.

- **État** : effectifs par année × âge × sexe × génération (G1, G2 à deux
  parents, G2 à un parent, G3, autres), avec en option l'origine agrégée
  (Europe, Maghreb, Afrique subsaharienne, Asie, autres) pour suivre une
  vague.
- **Observé** : la population, les naissances et les décès (séries longues
  depuis 1901) ; le stock d'immigrés à chaque recensement (dès 1911), avec 4
  classes d'âge ; les 4 vannes des immigrés et des non-immigrés de 2006 à
  2022 (les décès d'immigrés sont déjà une estimation de l'Insee) ; les
  naissances selon le pays de naissance des parents depuis 1998 ; une photo
  2019-2020 des G1, G2 et G3 par âge (IP 1910, TeO2).
- **Reconstruit** : avant 2006, le flux net d'immigrés = variation du stock +
  décès estimés. Les arrivées et les départs ne sont pas séparables : la
  piscine montre alors une vanne nette, marquée comme telle.
- **Modélisé** (paramètres en YAML, validés par Max) : la mortalité par âge
  (tables générales, sans hypothèse de surmortalité par origine), les entrées
  par âge avant 2006, les sorties, la mixité des unions par génération
  (TeO2), la fécondité par génération (convergence, TeO2 ch. 17).
- **Tests** : le modèle doit retrouver les stocks d'immigrés observés à
  chaque recensement, et les parts de G2 et de G3 de TeO2, aux tolérances
  documentées. Un écart casse le build.
- **Exports** : un JSON par arrangement (effectifs par année et par case,
  débits des vannes), calculé par le pipeline. Le navigateur se contente
  d'animer. Au cycle 2, une version allégée du modèle tournera dans le
  navigateur pour les curseurs.

## 7. Technique

Canvas 2D dans un composant Svelte (quelques milliers de particules à 60
images par seconde, sans WebGL). Les échelles, les axes et la frise sont en
d3/SVG par-dessus. Les particules sont attribuées aux cases du modèle à chaque
année. Les naissances, les arrivées, les décès et les départs sont des
particules qui entrent ou sortent par leur vanne, et l'interpolation suit le
mouvement continu de l'eau. Sur mobile, on affiche moins de particules (1 pour
20 000 personnes) et la pyramide en pleine largeur.

## 8. Étapes

| Version | Contenu | Données nécessaires |
|---|---|---|
| **v0** | 2006-2022 mesuré (4 vannes réelles), 1968-2005 reconstruit (vanne nette), 2023-2025 partiel ; 2 teintes (immigrés, non-immigrés), arrangement piscine seul | Bilans démographiques, IP 2107, stocks |
| v1 | + G2 par le robinet des naissances (origine des parents), scène 3 | Naissances par pays de naissance des parents |
| v2 | + âge : la pyramide vivante, G3, mixité, tests de calage | Structure par âge, paramètres TeO2 |
| v3 | + 1851-1968 (étrangers), une vague suivie de bout en bout | Séries historiques (spike historique) |
| cycle 2 | Projections 2070, contrefactuels, curseurs dans le navigateur | Projections Insee 2026 |

La v1 du site embarque au moins la piscine v2. La v3 dépend de ce que le
spike historique trouve sous forme exploitable.

## 9. Questions pour Max

1. Les deux arrangements (piscine et pyramide vivante) : est-ce que la
   pyramide vivante te parle, ou veux-tu rester sur l'image du bassin ?
2. Teinte par génération (catégories officielles) ou teinte continue (part
   des ascendants nés à l'étranger) ? Reco : maquetter les deux en v2 et
   trancher sur pièce.
3. Faut-il une particule = N personnes visible et assumée (« 1 point = 10 000
   personnes »), ou un rendu plus fluide, plus « eau », sans unité ? Reco :
   l'unité visible, pour l'honnêteté du compte.
