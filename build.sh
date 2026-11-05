#!/usr/bin/env bash
# Build exécuté par Cloudflare Pages à chaque push sur main : construit le site statique dans
# site/build/ à partir de l'instantané versionné (data/export/). Aucune source n'est téléchargée
# ici : les données se régénèrent en local (`uv run qrq download && uv run qrq build`), puis se
# commitent (CLAUDE.md, décisions de cadrage). Reproductible : `bash build.sh`.
set -euo pipefail
cd "$(dirname "$0")"
node --version

test -f data/export/meta.json && test -f data/export/piscine.json

echo "== Site"
cd site
npm ci --no-audit --no-fund
npm run build
echo "Fichiers dans site/build/ : $(find build -type f | wc -l)"
test -f build/index.html && test -f build/404.html && test -f build/_headers
test -f build/piscine.html && test -f build/temps-long.html && test -f build/generations.html
test -f build/limites.html && test -f build/methode.html && test -f build/donnees.html
test -f build/donnees/piscine.csv && test -f build/donnees/teo2.csv
