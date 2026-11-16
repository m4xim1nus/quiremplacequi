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

## Étape 3 : modèle de la piscine et modules E, F2

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
- [ ] Profil d'âge à l'arrivée par époque, si une source publique agrégée le
  donne (corrige l'âge des G1).
- [ ] TeO2 : chapitre 7, figures 3 et 4 (≈ 168 cellules) ; chapitre 11,
  contradiction entre le §35 et la figure 1, signalée sur le site.
- [ ] Relecture factuelle indépendante des textes ajoutés depuis le 2026-11-05.

**Livrable** : piscine v2 et pages E, F2 relues par Max.

## Étape 4 : site v1

Conception (`docs/CONCEPTION.md`), site SvelteKit statique, mise en ligne
sur Cloudflare Pages.

## Ensuite : cycles

L'international (C), la nature des migrations (D), les projections et les
contrefactuels de la piscine (F1, F3), la rhétorique (G), la frise des
discours (B4).
