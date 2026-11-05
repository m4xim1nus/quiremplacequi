import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, piscine } from '$lib/server/donnees';

export const load = () => {
  const p = piscine() as ReturnType<typeof piscine> & {
    cohortes: { statut_parametres: string; calage: Record<string, number> };
  };
  const cal = csvParse(readFileSync(resolve(EXPORT, 'cohortes_calage.csv'), 'utf8'));
  const ip = cal
    .filter((r) => r.temoin === 'ip1910_2020' && ['0-17', '18-59', '60 ou plus'].includes(r.cle!))
    .map((r) => ({
      groupe: r.groupe!,
      classe: r.cle!,
      modele: Number(r.modele),
      observe: Number(r.observe)
    }));
  const desc = cal.find((r) => r.temoin === 'descendants_2025' && r.cle === 'effectif')!;
  const dec = cal.filter((r) => r.temoin === 'deces_immigres_insee');
  const somme = (k: 'modele' | 'observe') => dec.reduce((s, r) => s + Number(r[k]), 0);
  return {
    statut: p.cohortes.statut_parametres,
    calage: p.cohortes.calage,
    ip,
    descendants: { modele: Number(desc.modele), observe: Number(desc.observe) },
    deces: { modele: somme('modele'), observe: somme('observe'), annees: dec.length },
    ratio: p.ratio_deces
  };
};
