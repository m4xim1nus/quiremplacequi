# CLAUDE.md

Guide pour Claude Code dans ce dépôt.

## Le projet

**Qui remplace qui ?** est un instrument de mesure des **questions
démographiques liées aux migrations** en France : combien, depuis quand, à
quelle vitesse, qui arrive, qui part, ce que deviennent les descendants. Il
répond, données à l'appui, à la thèse raciste du « grand remplacement ». Le
fil conducteur est la méthode de **François Héran** : rapporter au lieu
d'additionner, distinguer stock et flux, comparer dans le temps et dans
l'espace, décomposer par motif, ne jamais compter deux fois. Restitution sur
un **site web statique**, avec un module signature : **la piscine**, la
population vue comme une eau qui se renouvelle en permanence.

**Posture** : « nommer, puis mesurer ». L'accueil nomme une fois la thèse et
pose la question ; tout le reste est un instrument de mesure dont la
réfutation découle des données. Le site concède d'emblée ce qui est vrai (il
n'y a jamais eu autant d'immigrés en France ; le solde migratoire est devenu
le premier moteur de la croissance démographique) et montre que c'est le
**cadrage** qui ment, plus que les chiffres. Il montre aussi les inégalités et
les discriminations persistantes : le mélange réfute le « remplacement », les
inégalités réfutent le récit inverse d'une intégration sans friction. C'est un
instrument de preuve, pas un tract.

Cadrage complet : `docs/CADRAGE.md`. Conception de la piscine :
`docs/PISCINE.md`. Le dossier `source/` est privé et non versionné : il
contient le matériau d'origine du projet. **Le site, les docs versionnées et
les commits n'y font jamais référence.**

## Décisions de cadrage (2026-11-04, validées par Max)

- **Nom** : « Qui remplace qui ? » ; paquet et CLI `qrq` ; visé
  `quiremplacequi.technoperchoir.fr`.
- **Stack alignée sur `~/dev/deux-poids-deux-eleves`** (elle-même copiée de
  `~/dev/quifaitlaloi`) : Python 3.12 + uv + polars → SQLite + CSV/JSON,
  puis site SvelteKit adapter-static + d3, Node 22. La piscine se dessine en
  **Canvas 2D** (des milliers de particules animées), le reste en SVG d3. En
  cas de doute sur une convention (build.sh, CI, tests), copier 2p2e.
- **Données = instantané versionné** : le pipeline tourne en local,
  `data/export/` est commité, le build du site ne télécharge rien.
- **Dépôt GitHub privé** (`m4xim1nus/quiremplacequi`), public plus tard.
  Déploiement visé : Cloudflare Pages relié au dépôt (option 2 de
  `~/knowledge/wiki/syntheses/options-deploiement-web.md`).
- **Cadrage public** : nommer, puis mesurer (voir plus haut).
- **Périmètre v1** : la piscine (A), le temps long et les vagues (B1, B2,
  B5), générations et mixité (E1-E3) **avec** les inégalités (E9-E10), le
  curseur de définition (F2). L'international (C) et les motifs (D) au
  cycle 2. Codes des modules : `docs/CADRAGE.md` §4.
- La piscine telle que décrite dans `docs/PISCINE.md` §1 correspond à
  l'intention de Max ; il attend une proposition d'UI/UX et de fond.

## Décisions du spike (2026-11-05, validées par Max)

Détail : `docs/SOURCES.md` §5. Piscine mesurée de 2006 à 2022, reconstruite
et marquée de 1968 à 2005 (vanne nette) ; TeO2 ressaisi avec une référence
par cellule ; vagues en parts d'IP 1910, migrations juives en encadré
qualitatif ; la note OID de septembre 2026 traitée en v1 par F2 et un encadré.
La piscine est une proposition du site, pas une image d'Héran : on l'assume
comme une comptabilité, pas comme une explication.

## Règles dures

- **Agrégats publics uniquement** (Insee, Ined, ministère de l'Intérieur,
  Eurostat, ONU, OCDE). Pas de microdonnées sans habilitation. Presse et
  publications militantes jamais en source primaire.
- **Toute valeur affichée est lue par script**, jamais recopiée à la main.
  Exception : les tableaux qui n'existent qu'en PDF (TeO2, Insee Première,
  diaporamas d'Héran) se saisissent dans un fichier de référentiel, **une
  référence (document, page, figure ou tableau) par cellule**. Les scripts
  de spike (`docs/spike/scripts/`) sont du matériau daté, **pas le
  pipeline**.
- **Typage** : chaque série est un stock (au 1er janvier), un flux (sur
  l'année), un solde ou un taux. On n'additionne jamais un stock et un flux,
  et on ne compte jamais deux fois (titres + demandes d'asile).
- **Relatif à côté de l'absolu** : la bascule absolu ↔ part ↔ pour 10 000
  habitants est disponible partout où elle a un sens.
- **Les incertitudes s'affichent dans le graphique**, pas en note : registre
  `pipeline/referentiels/incertitudes.yaml` (codes `U1`…), ruptures de série
  et changements de concept matérialisés, champ affiché sur chaque graphique.
- **Modèle ≠ observation** : la piscine et les projections sont des modèles
  (paramètres en YAML, hypothèses listées, éventail). Le modèle doit
  reproduire les stocks observés sur la période historique (test). Une
  projection n'est jamais présentée comme une prévision.
- **Catégories** : seulement celles des sources (lieu de naissance,
  nationalité, ascendance ; expériences déclarées dans TeO2). Pas de proxy
  « prénoms », pas de catégorie ethno-raciale inventée. Religion : seulement
  si Max le décide.
- **Couleurs** : aucune couleur « menaçante » codée par origine. Dans la
  piscine, les teintes codent la distance à la migration (génération), pas
  l'origine.
- **Choix sensibles validés par Max** : formulations du message, paramètres
  du modèle de la piscine, choix des vagues, traitement des contradicteurs.
  Préférer une règle fixe à un jugement au cas par cas.
- Site public : **ton factuel**, méthode auditable, lisible par un
  non-spécialiste. FOSS, aucun tracker, aucun CDN tiers.

## Suivi

- `ROADMAP.md` : étapes jusqu'à la v1, puis cycles. Le détail se limite à
  l'étape en cours.
- `BACKLOG.md` : file brute, une ligne par item. Tout retour capté en
  session y va d'abord.
- `CHANGELOG.md` : créé au premier tag `v*`.

## Commandes

```bash
cd pipeline && uv sync               # environnement Python
cd pipeline && uv run qrq download   # sources Insee → data/raw/insee/ (+ manifeste.json)
cd pipeline && uv run qrq build      # → data/qrq.sqlite (non versionnée) + data/export/
cd pipeline && uv run qrq check      # identités comptables, invariants, témoins
cd pipeline && uv run pytest         # tests (les tests `donnees` exigent l'export, versionné)
cd site && npm ci && npm run dev     # site en local (copie data/export/ dans static/donnees/)
cd site && npm run check && npm test && npm run format:check
bash build.sh                        # build complet, celui de Cloudflare Pages
```

Toute nouvelle source se déclare dans `pipeline/qrq/sources.py`, sa lecture
dans un module par famille (`stock.py`, `flux.py`, `bilan.py`,
`naissances.py`), l'assemblage dans `build.py`, et ses contrôles dans
`check.py`. Les paramètres du modèle de la piscine sont dans
`pipeline/referentiels/piscine.yaml` (statut `a_valider` tant que Max ne les a
pas relus) ; le registre des incertitudes dans
`pipeline/referentiels/incertitudes.yaml`.

Site : SvelteKit statique, toute valeur affichée est lue au prérendu dans
`site/src/lib/server/donnees.ts` à partir de `data/export/` (jamais de chiffre
en dur dans les textes). La piscine : logique pure dans
`site/src/lib/piscine.ts` (testée), moteur de particules dans
`site/src/lib/moteur.ts`, dessin Canvas 2D dans
`site/src/lib/components/Piscine.svelte`. `/piscine?annee=2013&lecture` ouvre
une année et lance l'animation. Les scripts de spike
(`docs/spike/scripts/`) restent du matériau daté.

## Langue

Tout en français (docs, textes du site, commentaires, échanges), diacritiques
compris. Identifiants de code et de données en français sans diacritiques.
