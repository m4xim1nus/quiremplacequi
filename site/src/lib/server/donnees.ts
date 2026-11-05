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

import { csvParse } from 'd3-dsv';

/** Une cellule saisie de TeO2 (pipeline/referentiels/teo2/, une référence par cellule). */
export function teo2(fichier: string, ligne: string, colonne: string): number {
  const rows = csvParse(readFileSync(resolve(EXPORT, 'teo2.csv'), 'utf8'));
  const r = rows.find((x) => x.fichier === fichier && x.ligne === ligne && x.colonne === colonne);
  if (!r) throw new Error(`TeO2 : cellule introuvable ${fichier} / ${ligne} / ${colonne}`);
  return Number(r.valeur);
}

/** Descendants d'immigrés mesurés en 2025 (enquête Emploi), témoin du modèle de cohortes. */
export function descendants2025(): { effectif: number; part_un_parent: number } {
  const rows = csvParse(readFileSync(resolve(EXPORT, 'cohortes_calage.csv'), 'utf8'));
  const f = (cle: string) =>
    Number(rows.find((r) => r.temoin === 'descendants_2025' && r.cle === cle)!.observe);
  return { effectif: f('effectif'), part_un_parent: f('part_un_parent') };
}
