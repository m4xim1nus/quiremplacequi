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

## Étape 2 : pipeline et piscine v0 (en cours)

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
- [ ] Revue des paramètres de `piscine.yaml` par Max.
- [x] Graphiques bruts de relecture de B1 et B2 (`pipeline/explo/relecture_b1_b2.py`, 7 figures) :
  rien à corriger ; l'emboîtement des pays de naissance entre dans `qrq check`.

**Livrable** : piscine v0 relue par Max, paramètres validés.

## Étape 3 : modèle de la piscine et modules E, F2

Modèle de cohortes calé sur les observations (piscine v2), saisies
référencées de TeO2, curseur de définition.

## Étape 4 : site v1

Conception (`docs/CONCEPTION.md`), site SvelteKit statique, mise en ligne
sur Cloudflare Pages.

## Ensuite : cycles

L'international (C), la nature des migrations (D), les projections et les
contrefactuels de la piscine (F1, F3), la rhétorique (G), la frise des
discours (B4).
