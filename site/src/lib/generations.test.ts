import { describe, expect, it } from 'vitest';
import { ecartA100, etendue, paliers, pc, pts, somme, valeur, type Cellule } from './generations';
import { donneesGenerations } from './server/generations';

const c = (ligne: string, colonne: string, v: number): Cellule => ({
  fichier: 'f',
  ligne,
  colonne,
  valeur: v,
  unite: '%',
  approx: false,
  champ: '',
  precision: null
});

describe('fonctions pures', () => {
  it('paliers cumulés et étendue', () => {
    const p = paliers([
      { cle: 'a', libelle: 'A', ajout: 13, deduit: false },
      { cle: 'b', libelle: 'B', ajout: 11, deduit: false },
      { cle: 'c', libelle: 'C', ajout: 17, deduit: true }
    ]);
    expect(p.map((x) => x.cumul)).toEqual([13, 24, 41]);
    expect(etendue(p)).toBeCloseTo(41 / 13);
  });
  it('valeur manquante = erreur, pas zéro', () => {
    expect(() => valeur([c('x', 'y', 1)], 'f', 'x', 'z')).toThrow();
  });
  it('sommes et écart à 100', () => {
    const cs = [c('G1', 'a', 15), c('G1', 'b', 73), c('G1', 'c', 17), c('G1', 'd', 18)];
    expect(somme(cs, 'f', 'G1', ['a', 'b'])).toBe(88);
    expect(ecartA100(cs, 'f', 'G1')).toBe(23);
  });
  it('formats', () => {
    expect(pc(13)).toBe('13\u00a0%');
    expect(pc(9.1)).toBe('9,1\u00a0%');
    expect(pts(-2.5)).toBe('−2,5\u00a0pt');
    expect(pts(6.1)).toBe('+6,1\u00a0pt');
  });
});

describe('données de la page (export réel)', () => {
  const d = donneesGenerations();
  it('curseur de définition : 13 % → 41 %, étendue ≈ ×3,2', () => {
    expect(d.e1.paliers[0].cumul).toBe(13);
    expect(d.e1.paliers.at(-1)!.cumul).toBe(41);
    expect(d.e1.etendue).toBeGreaterThan(3.1);
    expect(d.e1.etendue).toBeLessThan(3.3);
  });
  it('mixité : les couples mixtes sont des sommes de colonnes', () => {
    expect(d.e2.lignes.map((l) => l.mixte)).toEqual([39, 59, 90, 12]);
  });
  it('la ligne G1 du tableau 4 du ch. 9 est signalée', () => {
    expect(d.e10.anomalieG1).toBe(23);
  });
});
