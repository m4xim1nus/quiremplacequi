import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { Moteur } from './moteur';
import {
  cumuls,
  debits,
  mouvements,
  particules,
  partNesAvant,
  solde,
  somme,
  stocks,
  TEINTES,
  type DonneesPiscine
} from './piscine';

const donnees = JSON.parse(
  readFileSync(resolve(process.cwd(), '../data/export/piscine.json'), 'utf8')
) as DonneesPiscine;
const E = donnees.echelle;
const an = (a: number) => donnees.annees.find((x) => x.annee === a)!;

describe('mouvements', () => {
  it('retombe exactement sur le stock suivant, chaque année et pour chaque teinte', () => {
    for (const [l, s] of donnees.annees.slice(0, -1).map((l, i) => [l, donnees.annees[i + 1]])) {
      const m = mouvements(l, s, E);
      for (const teinte of TEINTES) {
        const solde = m.filter((x) => x.teinte === teinte).reduce((t, x) => t + x.sens, 0);
        const depart = particules(stocks(l)[teinte], E);
        const cible = particules(stocks(s)[teinte], E);
        expect(depart + solde, `${l.annee}, teinte ${teinte}`).toBe(cible);
      }
    }
  });

  it("aucune naissance n'est immigrée", () => {
    for (const l of donnees.annees.slice(0, -1)) {
      const m = mouvements(l, an(l.annee + 1), E);
      expect(m.some((x) => x.vanne === 'naissances' && x.teinte === 4)).toBe(false);
    }
  });

  it("l'effet de collecte de 2024 n'est jamais une arrivée (U5)", () => {
    const m = mouvements(an(2023), an(2024), E);
    const arrivees = m.filter((x) => x.vanne === 'arrivees' && x.teinte === 4).length;
    expect(arrivees).toBe(particules(an(2023).entrees_imm!, E));
    expect(m.filter((x) => x.vanne === 'ajustement' && x.teinte === 4).length).toBe(
      particules(242_000, E)
    );
  });

  it('est déterministe', () => {
    expect(mouvements(an(2010), an(2011), E)).toEqual(mouvements(an(2010), an(2011), E));
  });
});

describe('moteur', () => {
  it('suit le stock quand le temps avance', () => {
    const m = new Moteur(donnees.annees, E);
    m.aller(2006);
    m.avancer(1, true);
    expect(m.comptes()).toEqual(TEINTES.map((t) => particules(stocks(an(2007))[t], E)));
    m.avancer(10.5, true);
    expect(Math.floor(m.temps)).toBe(2017);
  });

  it("s'arrête à la dernière année", () => {
    const m = new Moteur(donnees.annees, E);
    m.aller(2024);
    m.avancer(5, true);
    expect(m.temps).toBe(2025);
    expect(m.comptes()[4]).toBe(particules(an(2025).immigres, E));
  });
});

describe('générations', () => {
  it('les G2 et les G3 ne viennent que par le robinet des naissances', () => {
    for (const l of donnees.annees.slice(0, -1)) {
      const m = mouvements(l, an(l.annee + 1), E);
      const autres = m.filter(
        (x) => [1, 2, 3].includes(x.teinte) && x.sens === 1 && x.vanne !== 'arrondi'
      );
      expect(autres.every((x) => x.vanne === 'naissances')).toBe(true);
    }
  });
});

describe('vannes et cumuls', () => {
  it('le solde de chaque année boucle sur la variation de population, aux ajustements près', () => {
    for (const l of donnees.annees.slice(0, -1)) {
      const s = an(l.annee + 1);
      if (l.naissances == null || l.deces == null) continue;
      const ecart =
        s.population -
        l.population -
        (l.naissances - l.deces + solde(l) + (l.ajust_imm ?? 0) + (l.ajust_ni ?? 0));
      expect(Math.abs(ecart), `${l.annee}`).toBeLessThan(0.002 * l.population);
    }
  });

  it('les débits des quatre vannes reprennent les mouvements de particules', () => {
    for (const a of [1930, 1990, 2010, 2023]) {
      const d = debits(an(a));
      const m = mouvements(an(a), an(a + 1), E);
      for (const v of ['naissances', 'arrivees', 'deces', 'departs'] as const) {
        const n = m.filter((x) => x.vanne === v).length;
        expect(Math.abs(n - somme(d[v]) / E), `${a} ${v}`).toBeLessThanOrEqual(3);
      }
    }
  });

  it('cumule les flux entre deux dates', () => {
    const c = cumuls(donnees.annees, 2010, 2012);
    expect(c.naissances).toBe(an(2010).naissances! + an(2011).naissances!);
    expect(cumuls(donnees.annees, 2010, 2010).naissances).toBe(0);
  });

  it('chaque ruban relie sa vanne à la colonne de sa teinte', () => {
    const m = new Moteur(donnees.annees, E);
    m.aller(2010);
    const rubans = m.calculerRubans();
    expect(rubans.some((r) => r.vanne === 'naissances' && r.teinte === 4)).toBe(false);
    const g1 = rubans.find((r) => r.vanne === 'arrivees' && r.teinte === 4)!;
    const [lo, hi] = m.bornes[4];
    const f = (g1.xb - 0.05) / 0.9;
    expect(f).toBeGreaterThan(lo);
    expect(f).toBeLessThan(hi);
  });
});

describe("l'eau d'une année", () => {
  it('la part d’origine restante suit la part des habitants nés avant l’année de départ', async () => {
    const { nesAvant } = await import('./server/donnees');
    const nes = nesAvant(donnees.annees[0].annee);
    const m = new Moteur(donnees.annees, E, false, nes);
    m.aller(1950);
    m.avancer(50, true);
    const total = m.comptes().reduce((a, b) => a + b, 0);
    const attendu = partNesAvant(nes, 1950, 2000);
    expect(attendu).toBeGreaterThan(0.3);
    expect(attendu).toBeLessThan(0.6);
    expect(Math.abs(m.restantes() / total - attendu)).toBeLessThan(0.02);
  });
});
