// Calculs purs des pages « Les arrivées » (D) et « Ailleurs » (C) : rapports à la population,
// classements, décomposition d'une hausse. Testés dans comparaisons.test.ts.

/** Effectif pour 10 000 habitants. */
export const pour10000 = (n: number, population: number) => (1e4 * n) / population;

export interface Valeur {
  libelle: string;
  valeur: number;
}

/** Classement décroissant ; `rang(libelle)` donne la place (1 = premier). */
export function classement(valeurs: Valeur[]) {
  const tri = [...valeurs].sort((a, b) => b.valeur - a.valeur);
  return {
    tri,
    rang: (libelle: string) => tri.findIndex((v) => v.libelle === libelle) + 1,
    n: tri.length
  };
}

/**
 * Décomposition d'une hausse entre deux années : la part de chaque composante dans la variation
 * totale (en %, la somme fait 100). Une composante en baisse a une part négative.
 */
export function decomposer(
  debut: Record<string, number>,
  fin: Record<string, number>
): { cle: string; variation: number; part: number }[] {
  const cles = Object.keys(fin);
  const total = cles.reduce((s, k) => s + fin[k] - (debut[k] ?? 0), 0);
  return cles.map((k) => {
    const variation = fin[k] - (debut[k] ?? 0);
    return { cle: k, variation, part: (100 * variation) / total };
  });
}

/** Rang en toutes lettres : 1 → « 1er », 2 → « 2e ». */
export const rangTexte = (r: number) => (r === 1 ? '1er' : `${r}e`);

export const MOTIFS = ['etudiants', 'familial', 'economique', 'humanitaire', 'divers'] as const;
export type Motif = (typeof MOTIFS)[number];
export const LIBELLES_MOTIFS: Record<Motif, string> = {
  etudiants: 'Études',
  familial: 'Famille',
  economique: 'Travail',
  humanitaire: 'Protection (asile et autres)',
  divers: 'Divers'
};

/** Première année à partir de laquelle une série reste négative jusqu'au bout (null sinon). */
export function negatifDepuis(points: { annee: number; valeur: number }[]): number | null {
  let depuis: number | null = null;
  for (const p of points) {
    if (p.valeur < 0) depuis ??= p.annee;
    else depuis = null;
  }
  return depuis;
}

/** Médiane d'une liste de nombres. */
export function mediane(xs: number[]): number {
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

/** « La hausse vient … » : chaque motif avec son article. */
export const DU_MOTIF: Record<Motif, string> = {
  etudiants: 'des études',
  familial: 'de la famille',
  economique: 'du travail',
  humanitaire: 'de la protection',
  divers: 'des autres motifs'
};

/**
 * Tranches d'effectifs égaux selon `x` (quintiles pour k = 5) et médiane de `y` dans chacune.
 * Les points sont triés par `x` ; une tranche va du plus petit au plus grand `x` qu'elle contient.
 */
export function tranchesMedianes<T>(
  points: T[],
  x: (p: T) => number,
  y: (p: T) => number,
  k: number
): { de: number; a: number; mediane: number; n: number }[] {
  const tri = [...points].sort((a, b) => x(a) - x(b));
  const n = tri.length;
  return Array.from({ length: k }, (_, i) => {
    const g = tri.slice(Math.floor((i * n) / k), Math.floor(((i + 1) * n) / k));
    return { de: x(g[0]), a: x(g[g.length - 1]), mediane: mediane(g.map(y)), n: g.length };
  });
}
