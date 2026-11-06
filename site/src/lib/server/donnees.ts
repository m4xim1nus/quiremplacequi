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

/**
 * Pyramides des âges (Insee) réduites à ce qu'en lit la piscine : pour chaque année Y, la part de
 * la population âgée d'au moins k ans au 1er janvier, c'est-à-dire née avant le 1er janvier Y − k,
 * pour k de 0 à Y − `debut` (au plus 105, dernier âge de la pyramide).
 */
export function nesAvant(debut: number): Record<number, number[]> {
  const rows = csvParse(readFileSync(resolve(EXPORT, 'ages.csv'), 'utf8'));
  const par = new Map<number, number[]>();
  for (const r of rows) {
    const a = Number(r.annee);
    if (a < debut) continue;
    if (!par.has(a)) par.set(a, []);
    par.get(a)![Number(r.age)] = Number(r.population);
  }
  const out: Record<number, number[]> = {};
  for (const [a, v] of par) {
    const total = v.reduce((s, x) => s + x, 0);
    const parts: number[] = [];
    let cumul = total;
    for (let k = 0; k <= Math.min(a - debut, v.length - 1); k++) {
      parts.push(Math.round((cumul / total) * 1e5) / 1e5);
      cumul -= v[k];
    }
    out[a] = parts;
  }
  return out;
}
