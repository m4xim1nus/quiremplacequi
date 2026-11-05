// Copie l'instantané versionné (data/export/) dans static/donnees/, servi tel quel pour le
// téléchargement. Lancé avant `dev` et `build` (package.json).
import { cpSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';

const racine = resolve(import.meta.dirname, '../..');
const cible = resolve(import.meta.dirname, '../static/donnees');
rmSync(cible, { recursive: true, force: true });
mkdirSync(cible, { recursive: true });
const exportDir = resolve(racine, 'data/export');
for (const f of readdirSync(exportDir)) cpSync(resolve(exportDir, f), resolve(cible, f));
console.log(`donnees : ${readdirSync(cible).length} fichiers copiés dans static/donnees/`);
