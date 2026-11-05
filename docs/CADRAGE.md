# Cadrage

Version du 2026-11-05. Projet solo de Max, sans calendrier engageant.

## 1. Message

**Cadrage public validé par Max (2026-11-04) : « nommer, puis mesurer ».**
L'accueil nomme une fois la thèse du « grand remplacement » et pose la
question que le titre retourne : *qui remplace qui ?* Tout le reste est un
instrument de mesure.

Message de départ (proposition, à valider, puis à revoir au fil des
analyses) :

> Toute population se remplace : en un siècle, les naissances et les décès
> renouvellent toute l'eau de la piscine. L'immigration y ajoute un courant
> réel, qui progresse en France, moins vite qu'ailleurs en Europe. Ses
> enfants naissent français et se mêlent aux autres, génération après
> génération, comme les Belges, les Italiens, les Polonais, les Espagnols et
> les Portugais avant eux, et malgré des discriminations qui persistent.
> Ce n'est pas un grand remplacement, c'est un grand renouvellement.

**Pas de goal seek.** Ce message est un point de départ, pas une conclusion.
Le site concède d'emblée ce qui est vrai : il n'y a jamais eu autant
d'immigrés en France ; le solde migratoire est devenu le premier moteur de la
croissance de la population. Il dit où les données manquent, et il dit où
elles ne tranchent pas encore. C'est le cas pour la question de savoir si les
descendants des immigrations postcoloniales suivront le chemin des vagues
européennes : le précédent historique est un **précédent, pas une preuve**.

## 2. Posture

1. **Être l'instrument de mesure de référence, pas un tract.**
2. **Tenir deux vérités ensemble.** La migration progresse en Europe
   occidentale et dans le monde. Elle progresse aussi en France, mais à un
   rythme moindre.
3. **Les chiffres adverses sont souvent justes ; c'est le cadrage qui
   ment** : les dénominateurs, les flux sortants, les définitions, les
   doubles comptes, les champs, la mixité, les horizons, les effets de
   composition.
4. **Les graphiques sont le champ de bataille.** D'où une charte graphique
   non négociable (§6).
5. **Honnêteté sur la miscibilité.** On montre le mélange, qui réfute le
   « remplacement ». On montre aussi les inégalités et les discriminations
   persistantes, qui réfutent le récit inverse d'une intégration sans
   friction.
6. **Les contradicteurs en version forte** (*steelman*). Exemple :
   « l'analogie italienne ou polonaise ne vaut pas pour les immigrations
   extra-européennes ». La réponse honnête est que ce n'est pas encore
   tranché, et que la persistance de la saillance des origines est en partie
   produite par les discriminations.

## 3. Publics et forme

- Grand public curieux, journalistes, enseignants (SNT, maths, EMC), militants
  qui veulent des chiffres solides.
- Un **accueil** qui pose la question et montre la piscine.
- Des pages au format **« une page = une question »** : la question, la
  visualisation, une réponse courte, « ce que disent les contradicteurs »,
  les incertitudes, les données téléchargeables. La correspondance avec les
  30 questions de *Parlons immigration en 30 questions* (Héran, 2021) est à
  étudier (spike Héran).
- Une page **« Ce qu'on ne sait pas »** alimentée par le registre des
  incertitudes (§5). C'est une force du site, pas une annexe.
- Méthode, données (CSV), sources.

## 4. Modules

Codes stables : ils servent dans la méthode, le pipeline et le site.

| Code | Module | Question | Statut |
|---|---|---|---|
| **A** | **La piscine** | Comment la population se renouvelle-t-elle (naissances, décès, entrées, sorties), et comment les générations issues de l'immigration s'y mêlent-elles ? | **v1** (`docs/PISCINE.md`) |
| A0 | La baignoire | Le stock d'immigrés seul : des entrées, des sorties et des décès, aucune naissance. | v1, première scène de A |
| **B1** | Série longue 1851-2025 | Combien d'immigrés, quelle part, depuis quand ? Ruptures et changements de concept annotés. | **v1** |
| **B2** | Vague par vague | Montée, plateau et tarissement de chaque origine (Belges, Italiens, Polonais, Espagnols, Portugais, Algériens, Marocains…). | **v1** |
| B3 | Vitesse comparée des vagues | Années 1920 contre années 2010. | v1 si les données de B1 suffisent |
| B4 | Frise des discours | Le discours de l'« invasion » à chaque vague, placé sur la courbe B1, avec ce qu'est devenue la population visée. | plus tard |
| **B5** | Ce qu'il reste d'une vague | Les descendants des vagues anciennes aujourd'hui. | **v1** |
| C1-C7 | L'espace | Comparaisons internationales : part d'immigrés, progression, entrées par catégorie pour 10 000 habitants, asile, « prendre sa part », bosse migratoire. | cycle 2 |
| D1-D6 | La nature des migrations | Titres par motif, famille contre regroupement familial, parcours de l'asile sans double compte, réconciliation Insee ↔ ministère, frise des lois. | cycle 2 |
| **E1** | Trois générations | Part des immigrés, des descendants et des petits-enfants d'immigrés, avec les conjoints. | **v1** |
| **E2** | Mixité conjugale | Les couples mixtes par génération. | **v1** |
| **E3** | Généalogies | Combien de grands-parents immigrés ont les petits-enfants d'immigrés ? | **v1** |
| E4-E8 | Langue, identification, entre-soi, fécondité, diplômes | La convergence au fil des générations. | cycle 2 (E7 alimente la piscine dès la v1) |
| **E9** | Inégalités | Sur-chômage à profil égal, ségrégation résidentielle, discriminations déclarées. | **v1** |
| **E10** | Le paradoxe | Plus intégrés et plus exposés aux discriminations que leurs parents. | **v1** |
| F1 | Projections Insee | Les scénarios officiels à l'horizon 2070. | cycle 2 (mode projection de la piscine) |
| **F2** | Le curseur de définition | « Combien sont-ils ? » selon qui l'on compte : du simple au quadruple. | **v1** |
| F3 | Le piège de la projection naïve | Projeter les écarts de fécondité sans la convergence observée. | cycle 2 |
| F4 | « Migrations de remplacement » | Ce que le mot voulait dire chez les démographes (ONU 2000, Sauvy), et son détournement. | cycle 2 |
| G1-G3 | Rhétorique et perceptions | La galerie des sophismes, chacun démonté par un mini-graphique ; perceptions contre réalité. | cycle 2 |

## 5. La grammaire Héran

Les gestes de méthode que le site encode. Le spike Héran en propose onze de
plus (H15 à H25 : contrefactuel explicite, méfiance envers les métaphores
aquatiques, multiplicateurs et « équivalents-ville », le solde migratoire qui
inclut les non-immigrés…), à trier : `docs/spike/heran.md` §3.

| # | Geste | Traduction dans le site |
|---|---|---|
| H1 | **Relatif, pas absolu** (« le taux d'incidence, pas le nombre de cas ») | Bascule absolu ↔ part ↔ pour 10 000 habitants |
| H2 | **Stock contre flux** | Identité comptable ; la baignoire et la piscine |
| H3 | **Deux définitions de l'immigré** : définition large de l'ONU (né à l'étranger) contre définition stricte de l'Insee (né étranger à l'étranger) | Bascule de définition sur les comparaisons |
| H4 | **Comparer dans le temps et dans l'espace** | Modules B et C |
| H5 | **Décomposer par motif** ; migration familiale ≠ regroupement familial | Module D |
| H6 | **Pas de doubles comptes** | Encadrés, galerie des sophismes |
| H7 | **« Prendre sa part »** : rapporter l'accueil au poids démographique et économique | C5 |
| H8 | **Progression linéaire, pas exponentielle**, indépendante des présidents | B1 avec les mandats et les lois |
| H9 | ***Policy gap*** : des lois en série qui n'inversent pas la tendance | D6 |
| H10 | **La bosse migratoire** : ce ne sont pas les pays les plus pauvres qui émigrent le plus | C7 |
| H11 | **Convergence des comportements** (fécondité) | E7, F3, paramètres de la piscine |
| H12 | **Générations et mixité** : « infusion durable et non intrusion massive » | A, E |
| H13 | **Le savant et le politique** | Rubrique des contradicteurs |
| H14 | **Perceptions contre réalité** | G2 |

**Identité comptable du projet** (testée par le pipeline) :

```
ΔPopulation   = Naissances − Décès + Entrées − Sorties (+ ajustement)
ΔImmigrés     = Entrées_immigrés − Sorties_immigrés − Décès_immigrés      ← aucune naissance
ΔNon-immigrés = Naissances − Décès_NI + Entrées_NI − Sorties_NI
```

Le stock d'immigrés n'a pas d'accroissement naturel : leurs enfants nés en
France sortent de la catégorie par construction. C'est le moteur de la
piscine.

**Définitions (Insee, TeO2).** *Immigré* : né étranger à l'étranger, résidant
en France ; on le reste à vie, même naturalisé. *Étranger* : sans nationalité
française, éventuellement né en France. *G2* : né en France d'au moins un
parent immigré ; *G2.5* : d'un seul. *G1.5* : immigré arrivé à 16 ans ou
moins. *G3* : né en France de parents non immigrés, avec au moins un
grand-parent immigré. *Population majoritaire* : ni immigré, ni descendant
d'immigré sur deux générations, ni originaire des outre-mer.

## 6. Charte graphique et d'honnêteté

- Sous chaque graphique : la source, la date de publication, le **champ**, le
  statut (provisoire ou définitif), une ligne « Lecture : … » et le CSV.
- Les incertitudes du registre sont visibles **dans** le graphique.
- Les ruptures de série et les changements de concept sont matérialisés.
- Axes à zéro pour les niveaux ; tout axe tronqué est signalé.
- Bascule absolu ↔ relatif partout où elle a un sens (H1).
- Palette neutre ; aucune couleur « menaçante » codée par origine.
- Chaque chiffre du texte est calculé au prérendu à partir de `data/export/`.

## 7. Registre des incertitudes

Tenu en données (`pipeline/referentiels/incertitudes.yaml`), affiché sur la
page « Ce qu'on ne sait pas » et sur chaque graphique concerné. Premiers
codes (à confirmer par le spike) :

| # | Incertitude | Traitement visuel |
|---|---|---|
| U1 | Le solde migratoire n'est pas observé : on le calcule par différence | Bande d'incertitude, mention « résidu » |
| U2 | Les sorties sont un « résidu du résidu » (solde − entrées) | Vanne floue, moyennes pluriannuelles |
| U3 | Décalage : le solde n'est pas connu aussi loin que les entrées | Zone « pas encore mesuré » |
| U4 | Pas d'enquête annuelle de recensement en 2021 | Annotation |
| U5 | Rupture de série en 2024 (protocole du recensement) | Rupture tracée sur toutes les courbes |
| U6 | Champs variables (métropole, hors Mayotte, France entière) | Badge de champ |
| U7 | Les personnes en situation irrégulière sont partiellement captées par le recensement | Fourchettes seulement |
| U8 | La G3 n'est mesurable qu'avant 60 ans | Masque visuel |
| U9 | Avant 1968, surtout des étrangers par nationalité ; les naturalisations les font « disparaître » | Changement de concept tracé |
| U10 | Des vagues sans catégorie statistique (migrations juives) | Encadré « ce que la statistique ne voit pas » |
| U11 | Titres de séjour ≠ entrées | Graphique de réconciliation (cycle 2) |
| U12 | Définitions internationales différentes | Bascule de définition (cycle 2) |
| U13 | Origine des G2 à deux parents immigrés : celle du père, par convention | Note |
| U14 | Champ de TeO2 : 18-59 ans, métropole, logement ordinaire, 2019-2020 | Badge de champ |
| U15 | Données déclaratives | Mention « déclaré » |
| U16 | Projections ≠ prévisions ; aucune projection officielle par origine | Curseurs, éventail |

## 8. Garde-fous

Voir `CLAUDE.md`, règles dures. Hors périmètre par défaut, sauf décision de
Max : la religion, le coût de l'immigration, Mayotte et les outre-mer comme
sujet propre. Les personnes en situation irrégulière sont traitées seulement
en fourchettes (U7).

## 9. Questions encore ouvertes

Tranchées le 2026-11-04 : la lecture de la piscine (oui, à concevoir), la
stack (celle de 2p2e), le nom, le cadrage public, le périmètre v1 et le
dépôt privé. Restent ouvertes, avec leur recommandation (à poser à la fin du
spike, quand les données éclairent la réponse) :

1. **Plan calqué sur les 30 questions d'Héran ?** Reco : s'en inspirer pour la
   forme « une page = une question », sans le calquer (la v1 couvre moins de
   questions).
2. **Contradicteurs** : une rubrique systématique. Faut-il nommer l'OID ? Reco :
   nommer les publications précises qu'on discute (une note, un graphique),
   pas des personnes ; toujours en version forte.
3. **Héran** : inspiration ou référence explicite ? Le contacter (reprise de
   ses graphiques, corpus des « idées reçues ») ? Reco : référence explicite,
   et contact une fois qu'une v0 est montrable.
4. **Microdonnées TeO2** : faut-il demander l'accès ? (Voir le spike TeO2.)
5. **Vagues historiques en v1** : lesquelles ? Jusqu'où aller sur les
   migrations juives (données indirectes, U10) ?
6. **Mayotte et outre-mer, irréguliers, religion, coût** : dedans ou dehors ?
7. **Usage pédagogique** (SNT, maths, EMC ; lien avec le labo présidentielle
   2027) ?
