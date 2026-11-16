import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { describe, expect, it } from 'vitest';
import {
  classement,
  decomposer,
  mediane,
  negatifDepuis,
  pour10000,
  rangTexte,
  tranchesMedianes
} from './comparaisons';

const csv = (f: string) =>
  csvParse(readFileSync(resolve(process.cwd(), '../data/export', f), 'utf8'));

describe('comparaisons', () => {
  it('rapporte à la population et classe', () => {
    expect(pour10000(500, 1_000_000)).toBe(5);
    const c = classement([
      { libelle: 'A', valeur: 1 },
      { libelle: 'B', valeur: 3 },
      { libelle: 'C', valeur: 2 }
    ]);
    expect(c.tri.map((v) => v.libelle)).toEqual(['B', 'C', 'A']);
    expect(c.rang('C')).toBe(2);
    expect(rangTexte(1)).toBe('1er');
    expect(rangTexte(15)).toBe('15e');
  });

  it('décompose une hausse en parts qui font 100', () => {
    const d = decomposer({ a: 10, b: 10 }, { a: 25, b: 5 });
    expect(d.find((x) => x.cle === 'a')!.part).toBe(150);
    expect(d.reduce((s, x) => s + x.part, 0)).toBeCloseTo(100);
  });

  it('repère un passage durable sous zéro', () => {
    const p = (vs: number[]) => vs.map((valeur, i) => ({ annee: 2000 + i, valeur }));
    expect(negatifDepuis(p([1, -1, 1, -1, -2]))).toBe(2003);
    expect(negatifDepuis(p([1, 2]))).toBeNull();
    expect(mediane([3, 1, 2])).toBe(2);
    expect(mediane([4, 1, 2, 3])).toBe(2.5);
  });

  it('médianes par tranches d’effectifs égaux', () => {
    const pts = [1, 2, 3, 4, 5, 6].map((v) => ({ v, y: v * 10 }));
    const t = tranchesMedianes(
      pts,
      (p) => p.v,
      (p) => p.y,
      3
    );
    expect(t.map((x) => [x.de, x.a, x.mediane, x.n])).toEqual([
      [1, 2, 15, 2],
      [3, 4, 35, 2],
      [5, 6, 55, 2]
    ]);
  });

  it('naissances : mère née à l’étranger et seuil de remplacement', () => {
    const det = csv('naissances_detail.csv').filter((r) => r.annee === '2025');
    const np = csv('naissances_parents.csv').filter((r) => r.annee === '2025');
    const n = (rows: typeof det, c: string) =>
      Number(rows.find((r) => r.categorie === c)!.naissances);
    const mere =
      n(det, 'mere_ue_second_france') +
      n(det, 'mere_hors_ue_second_france') +
      n(np, 'deux_parents_nes_a_l_etranger');
    expect(mere).toBe(169_748);
    expect(csv('naissances_parents.csv').some((r) => r.annee === '2023')).toBe(true);
    const fr = csv('fecondite_nationale.csv').find(
      (r) => r.annee === '2025' && r.champ === 'france'
    )!;
    const seuil = (100 * Number(fr.icf)) / Number(fr.taux_reproduction_net);
    expect(seuil).toBeGreaterThan(2);
    expect(seuil).toBeLessThan(2.1);
  });

  it('titres de séjour : témoin 2024 et somme des motifs', () => {
    const t = csv('titres.csv').filter((r) => r.annee === '2024');
    expect(t.reduce((s, r) => s + Number(r.titres), 0)).toBe(345_587);
    const tot = csv('titres_totaux.csv').find((r) => r.annee === '2024')!;
    expect(Number(tot.britanniques)).toBe(8_899);
  });
});
