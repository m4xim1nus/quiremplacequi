import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { Moteur } from './moteur';
import { mouvements, particules, type DonneesPiscine } from './piscine';

const donnees = JSON.parse(
  readFileSync(resolve(process.cwd(), '../data/export/piscine.json'), 'utf8')
) as DonneesPiscine;
const E = donnees.echelle;
const an = (a: number) => donnees.annees.find((x) => x.annee === a)!;

describe('mouvements', () => {
  it('retombe exactement sur le stock suivant, chaque année et pour chaque teinte', () => {
    for (const [l, s] of donnees.annees.slice(0, -1).map((l, i) => [l, donnees.annees[i + 1]])) {
      const m = mouvements(l, s, E);
      for (const teinte of [0, 1] as const) {
        const solde = m.filter((x) => x.teinte === teinte).reduce((t, x) => t + x.sens, 0);
        const depart = particules(teinte ? l.immigres : l.non_immigres, E);
        const cible = particules(teinte ? s.immigres : s.non_immigres, E);
        expect(depart + solde, `${l.annee}, teinte ${teinte}`).toBe(cible);
      }
    }
  });

  it("aucune naissance n'est immigrée", () => {
    for (const l of donnees.annees.slice(0, -1)) {
      const m = mouvements(l, an(l.annee + 1), E);
      expect(m.some((x) => x.vanne === 'naissances' && x.teinte === 1)).toBe(false);
    }
  });

  it("l'effet de collecte de 2024 n'est jamais une arrivée (U5)", () => {
    const m = mouvements(an(2023), an(2024), E);
    const arrivees = m.filter((x) => x.vanne === 'arrivees' && x.teinte === 1).length;
    expect(arrivees).toBe(particules(an(2023).entrees_imm!, E));
    expect(m.filter((x) => x.vanne === 'ajustement' && x.teinte === 1).length).toBe(
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
    expect(m.comptes()).toEqual([
      particules(an(2007).non_immigres, E),
      particules(an(2007).immigres, E)
    ]);
    m.avancer(10.5, true);
    expect(Math.floor(m.temps)).toBe(2017);
  });

  it("s'arrête à la dernière année", () => {
    const m = new Moteur(donnees.annees, E);
    m.aller(2024);
    m.avancer(5, true);
    expect(m.temps).toBe(2025);
    expect(m.comptes()[1]).toBe(particules(an(2025).immigres, E));
  });
});
