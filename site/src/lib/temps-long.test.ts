import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { describe, expect, it } from 'vitest';
import { changementsDeChamp, segments, vagues, vitesse, type PointStock } from './temps-long';

const csv = (f: string) =>
  csvParse(readFileSync(resolve(process.cwd(), '../data/export', f), 'utf8'));
const serie: PointStock[] = csv('b1_stock.csv').map((r) => ({
  annee: +r.annee!,
  immigres: +r.immigres!,
  part: +r.part_immigres!,
  population: +r.population!,
  champ: r.champ!,
  statut: r.statut!,
  rupture: r.rupture === 'true'
}));

describe('temps long', () => {
  it('vitesse des années 1920 et 2010 (témoins du spike historique)', () => {
    const v20 = vitesse(serie, 1921, 1931);
    expect(v20.points).toBe(2.9);
    const v10 = vitesse(serie, 2010, 2020);
    expect(v10.points).toBe(1.7);
    expect(v10.effectif).toBe(6_847_100 - 5_514_200);
  });

  it('coupe la série à la rupture de 2024', () => {
    const s = segments(serie);
    expect(s).toHaveLength(2);
    expect(s[0].at(-1)!.annee).toBe(2023);
    expect(s[1][0].annee).toBe(2024);
  });

  it('repère les changements de champ (1990, 2014)', () => {
    expect(changementsDeChamp(serie).map((c) => c.annee)).toEqual([1990, 2014]);
  });

  it('les Italiens culminent en 1931 à 2 % de la population', () => {
    const it_ = vagues(
      csv('b2_nationalites.csv').map((r) => ({
        annee: +r.annee!,
        nationalite: r.nationalite!,
        groupe: r.groupe!,
        part_pct: +r.part_pct!
      }))
    ).find((v) => v.nationalite === 'Italiens')!;
    expect(it_.pic).toEqual({ annee: 1931, part: 2 });
  });
});
