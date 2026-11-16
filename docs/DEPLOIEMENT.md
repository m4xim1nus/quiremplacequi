# Mise en ligne

Option retenue au cadrage : **Cloudflare Pages relié au dépôt GitHub**. Cloudflare exécute
`bash build.sh` à chaque push sur `main` et publie `site/build/`. Le build ne télécharge aucune
donnée : il part de l'instantané versionné `data/export/`.

## 1. Avant le passage en public du dépôt

- [x] **Identité des commits** (2026-11-16) : historique réécrit avec l'adresse « noreply » de
  GitHub (`git filter-repo --mailmap`), poussé en force ; ce dépôt est réglé sur cette adresse
  (`git config user.email`). Les anciens commits peuvent rester joignables sur GitHub par leur
  empreinte directe tant que GitHub ne les a pas purgés : si besoin, demander la purge au support
  avant le passage en public.
- [x] Le dossier privé `source/` n'a jamais été commité (`git log --all -- source` est vide) ;
  aucun secret dans l'historique (vérifié le 2026-11-16).
- [x] Passer le dépôt en public **avant** de relier le domaine (la page « À propos » et le pied
  de page renvoient au dépôt et à ses tickets) : GitHub, Settings, General, Danger Zone, Change visibility (ou
  `gh repo edit m4xim1nus/quiremplacequi --visibility public --accept-visibility-change-consequences`).

## 2. Projet Cloudflare Pages

Dans le tableau de bord Cloudflare (compte qui porte la zone `technoperchoir.fr`) :

1. Workers & Pages, Create, Pages, **Connect to Git** ; autoriser l'application Cloudflare sur le
   dépôt `m4xim1nus/quiremplacequi` (fonctionne aussi avec un dépôt privé).
2. Réglages du build :
   - Framework preset : *None* ;
   - Build command : `bash build.sh` ;
   - Build output directory : `site/build` ;
   - Root directory : `/` ;
   - Variable d'environnement : `NODE_VERSION` = `22` (le fichier `.node-version` le dit aussi).
3. Branche de production : `main`.
4. Custom domains : ajouter `quiremplacequi.technoperchoir.fr` (enregistrement DNS créé
   automatiquement si la zone est sur le même compte).

## 3. Vérifications après le premier déploiement

Faites le 2026-11-16, toutes passées : les 8 pages, `partage.png`, les données et la page 404
répondent ; en-têtes de `_headers` servis (CSP, `nosniff`, referrer) ; polices en cache immuable ;
aucune ressource externe ni balise de mesure sur les 8 pages ; dépôt public.
Réserve : l'obfuscation des adresses de Cloudflare (Scrape Shield) remplace l'adresse de contact
et injecte un script servi par le site lui-même (`/cdn-cgi/…/email-decode.min.js`). Ni tiers ni
traceur, mais sans JavaScript l'adresse ne s'affiche pas : la désactiver pour ce sous-domaine si on
veut une page sans script injecté.

```bash
curl -sI https://quiremplacequi.technoperchoir.fr/ | grep -i -E "content-security|referrer|x-content"
curl -sI https://quiremplacequi.technoperchoir.fr/fonts/barlow-semi-condensed-latin-700-normal.woff2 | grep -i cache-control
curl -s https://quiremplacequi.technoperchoir.fr/piscine | grep -c 'og:image'
```

- Les en-têtes de `site/static/_headers` sont servis (CSP sans ressource tierce, cache des
  polices).
- Aucune requête vers un autre domaine (onglet Réseau du navigateur, sur chaque page).
- Cloudflare Web Analytics **désactivé** pour le projet (Pages, projet, Metrics) : sinon Cloudflare
  injecte un script de mesure, et la phrase « aucune mesure d'audience » deviendrait fausse.
- L'image de partage s'affiche (outil de prévisualisation d'un réseau social, ou
  `https://quiremplacequi.technoperchoir.fr/partage.png`).
- Puis : tag `v1.0.0` et `CHANGELOG.md`.

## 4. Mettre à jour les données

En local : `cd pipeline && uv run qrq download && uv run qrq build && uv run qrq check`, régénérer
l'image de partage (`uv run --with pillow --with fonttools --with brotli python site/scripts/partage.py`),
commiter `data/export/` et `site/static/partage.png`, pousser. Cloudflare reconstruit seul.
