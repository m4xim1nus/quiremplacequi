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

## Étape 2 : pipeline et piscine v0 (prochaine)

Package `qrq` (`download` → `build` → `check`), tests des identités
comptables, `incertitudes.yaml`. Séries de B1 et B2, bilans démographiques,
flux. Piscine v0 (1968-2025, 4 vannes, 2 teintes) en prototype local, avec
les graphiques bruts de relecture.

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
