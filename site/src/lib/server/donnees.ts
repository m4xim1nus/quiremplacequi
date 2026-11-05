// Lecture de data/export/ au prérendu (Node). Rien de ce module n'est envoyé au navigateur :
// chaque page reçoit seulement ce que sa fonction `load` en extrait. Toute valeur affichée sur le
// site vient d'ici (CLAUDE.md, règles dures).
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { DonneesPiscine } from '$lib/piscine';

/** Dossier des exports versionnés, relatif à site/ (cwd de vite). */
export const EXPORT = resolve(process.cwd(), '../data/export');

const json = <T>(nom: string): T => JSON.parse(readFileSync(resolve(EXPORT, nom), 'utf8')) as T;

export const piscine = () => json<DonneesPiscine>('piscine.json');

export interface Incertitude {
  titre: string;
  detail: string;
  traitement: string;
  verifie: boolean;
  reference?: string;
}
export const incertitudes = () => json<Record<string, Incertitude>>('incertitudes.json');

export const meta = () => json<{ genere_le: string }>('meta.json');
