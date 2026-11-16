# Mise en ligne

Option retenue au cadrage : **Cloudflare Pages relié au dépôt GitHub**. Cloudflare exécute
`bash build.sh` à chaque push sur `main` et publie `site/build/`. Le build ne télécharge aucune
donnée : il part de l'instantané versionné `data/export/`.

## 1. Avant le passage en public du dépôt

- [ ] **Identité des commits.** L'historique porte l'adresse de l'auteur des commits. Pour une
  signature quasi anonyme, la remplacer par l'adresse « noreply » de GitHub avant le passage en
  public (réécriture de l'historique, puis `git push --force` ; à faire pendant que le dépôt est
  encore privé, et une seule fois). Configurer ensuite `git config user.email` sur cette adresse
  dans ce dépôt.
- [x] Le dossier privé `source/` n'a jamais été commité (`git log --all -- source` est vide) ;
  aucun secret dans l'historique (vérifié le 2026-11-16).
- [ ] Passer le dépôt en public : GitHub, Settings, General, Danger Zone, Change visibility (ou
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

```bash
curl -sI https://quiremplacequi.technoperchoir.fr/ | grep -i -E "content-security|referrer|x-content"
curl -sI https://quiremplacequi.technoperchoir.fr/fonts/barlow-semi-condensed-latin-700-normal.woff2 | grep -i cache-control
curl -s https://quiremplacequi.technoperchoir.fr/piscine | grep -c 'og:image'
```

- Les en-têtes de `site/static/_headers` sont servis (CSP sans ressource tierce, cache des
  polices).
- Aucune requête vers un autre domaine (onglet Réseau du navigateur, sur chaque page).
- L'image de partage s'affiche (outil de prévisualisation d'un réseau social, ou
  `https://quiremplacequi.technoperchoir.fr/partage.png`).
- Puis : tag `v1.0.0` et `CHANGELOG.md`.

## 4. Mettre à jour les données

En local : `cd pipeline && uv run qrq download && uv run qrq build && uv run qrq check`, régénérer
l'image de partage (`uv run --with pillow --with fonttools --with brotli python site/scripts/partage.py`),
commiter `data/export/` et `site/static/partage.png`, pousser. Cloudflare reconstruit seul.
