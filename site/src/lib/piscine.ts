// Logique pure de la piscine (docs/PISCINE.md) : à partir d'une année de data/export/piscine.json,
// combien de particules entrent et sortent par chaque vanne, et quand. Sans DOM, testé.

export type Statut = 'mesure' | 'partiel' | 'reconstruit';

export interface AnneePiscine {
  annee: number;
  population: number;
  immigres: number;
  non_immigres: number;
  part_immigres: number;
  statut_stock: string;
  champ: string;
  rupture: boolean;
  statut_flux?: Statut | null;
  naissances?: number | null;
  deces?: number | null;
  deces_imm?: number | null;
  deces_ni?: number | null;
  deces_imm_bas?: number | null;
  deces_imm_haut?: number | null;
  entrees_imm?: number | null;
  sorties_imm?: number | null;
  net_imm?: number | null;
  entrees_ni?: number | null;
  sorties_ni?: number | null;
  net_ni?: number | null;
  ajust_imm?: number | null;
  ajust_ni?: number | null;
  non_ventile_imm?: number | null;
  non_ventile_ni?: number | null;
  // Générations (modèle de cohortes, piscine v1).
  g2a?: number;
  g2b?: number;
  g3?: number;
  autres?: number;
  naissances_g2a?: number | null;
  naissances_g2b?: number | null;
  naissances_g3?: number | null;
  naissances_autres?: number | null;
  deces_g2a?: number | null;
  deces_g2b?: number | null;
  deces_g3?: number | null;
  deces_autres?: number | null;
  regime_naissances?: string | null;
}

export interface Evenement {
  annee: number;
  code: string | null;
  libelle: string;
}

export interface DonneesPiscine {
  echelle: number;
  statut_parametres: string;
  ratio_deces: { moyen: number; min: number; max: number; calage: number[] };
  evenements: Evenement[];
  annees: AnneePiscine[];
  /**
   * Pyramides des âges : `nes_avant[Y][k]` = part de la population de l'année Y née avant le
   * 1er janvier Y − k (âgée d'au moins k ans). Ajouté au prérendu (server/donnees.ts).
   */
  nes_avant?: Record<number, number[]>;
}

/** Part de la population de l'année `y` née avant le 1er janvier de l'année `x` (x ≤ y). */
export function partNesAvant(nes: Record<number, number[]>, x: number, y: number): number {
  const v = nes[y];
  if (!v) return NaN;
  const k = y - x;
  return k < v.length ? v[k] : v[v.length - 1];
}

/**
 * Teinte = distance à la migration, du fond vers la surface de la piscine décantée :
 * 0 autres, 1 G3, 2 G2 (un parent immigré), 3 G2 (deux parents), 4 G1 (immigrés).
 */
export type Teinte = 0 | 1 | 2 | 3 | 4;
export const TEINTES: Teinte[] = [0, 1, 2, 3, 4];

export const GENERATIONS: Record<Teinte, { cle: string; libelle: string; court: string }> = {
  4: { cle: 'immigres', libelle: 'Immigrés (G1)', court: 'G1' },
  3: { cle: 'g2a', libelle: 'Enfants de deux parents immigrés (G2)', court: 'G2 · 2 parents' },
  2: { cle: 'g2b', libelle: 'Enfants d’un parent immigré (G2)', court: 'G2 · 1 parent' },
  1: { cle: 'g3', libelle: 'Petits-enfants d’immigrés (G3)', court: 'G3' },
  0: { cle: 'autres', libelle: 'Ni immigré, ni enfant ou petit-enfant d’immigré', court: 'autres' }
};

/** Effectif de chaque teinte au 1er janvier (sans générations : deux teintes, 0 et 4). */
export function stocks(l: AnneePiscine): Record<Teinte, number> {
  if (l.g2a === undefined) return { 0: l.non_immigres, 1: 0, 2: 0, 3: 0, 4: l.immigres };
  return { 0: l.autres!, 1: l.g3!, 2: l.g2b!, 3: l.g2a!, 4: l.immigres };
}

/** Naissances et décès de l'année par teinte. */
export function naissancesParTeinte(l: AnneePiscine): Record<Teinte, number> {
  if (l.naissances_autres == null) return { 0: l.naissances ?? 0, 1: 0, 2: 0, 3: 0, 4: 0 };
  return {
    0: l.naissances_autres,
    1: l.naissances_g3 ?? 0,
    2: l.naissances_g2b ?? 0,
    3: l.naissances_g2a ?? 0,
    4: 0
  };
}

export function decesParTeinte(l: AnneePiscine): Record<Teinte, number> {
  if (l.deces_autres == null) return { 0: l.deces_ni ?? 0, 1: 0, 2: 0, 3: 0, 4: l.deces_imm ?? 0 };
  return {
    0: l.deces_autres,
    1: l.deces_g3 ?? 0,
    2: l.deces_g2b ?? 0,
    3: l.deces_g2a ?? 0,
    4: l.deces_imm ?? 0
  };
}

/**
 * Par où passe une particule. `ajustement` : changement de champ ou de collecte (jamais un flux),
 * montré ; `arrondi` : écart d'arrondi en particules, silencieux.
 */
export type Vanne = 'naissances' | 'arrivees' | 'deces' | 'departs' | 'ajustement' | 'arrondi';

export interface Mouvement {
  /** Instant dans l'année, entre 0 et 1. */
  t: number;
  vanne: Vanne;
  teinte: Teinte;
  /** +1 entre dans la piscine, −1 en sort. */
  sens: 1 | -1;
}

/** Nombre de particules attendu pour un effectif (arrondi au plus proche). */
export const particules = (effectif: number, echelle: number) => Math.round(effectif / echelle);

/** Générateur pseudo-aléatoire déterministe (mulberry32) : même année, même chorégraphie. */
export function alea(graine: number): () => number {
  let a = graine >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Mouvements de l'année `a` → `a + 1`. Les effectifs de chaque vanne sont arrondis en particules ;
 * l'écart d'arrondi est absorbé par un ajustement silencieux, pour que le nombre de particules de
 * chaque teinte retombe exactement sur le stock de l'année suivante.
 */
export function mouvements(ligne: AnneePiscine, suivante: AnneePiscine, echelle: number) {
  const n = (x: number | null | undefined) => particules(x ?? 0, echelle);
  const brut: Omit<Mouvement, 't'>[] = [];
  const pousser = (k: number, vanne: Vanne, teinte: Teinte, sens: 1 | -1) => {
    for (let i = 0; i < k; i++) brut.push({ vanne, teinte, sens });
  };
  const flux = (x: number | null | undefined, teinte: Teinte, entree: Vanne, sortie: Vanne) => {
    const k = n(x);
    if (k > 0) pousser(k, entree, teinte, 1);
    else if (k < 0) pousser(-k, sortie, teinte, -1);
  };

  const nais = naissancesParTeinte(ligne);
  const morts = decesParTeinte(ligne);
  for (const t of TEINTES) {
    pousser(n(nais[t]), 'naissances', t, 1);
    pousser(n(morts[t]), 'deces', t, -1);
  }
  if (ligne.statut_flux === 'reconstruit') {
    flux(ligne.net_imm, 4, 'arrivees', 'departs');
    flux(ligne.net_ni, 0, 'arrivees', 'departs');
  } else {
    pousser(n(ligne.entrees_imm), 'arrivees', 4, 1);
    pousser(n(ligne.entrees_ni), 'arrivees', 0, 1);
    pousser(n(ligne.sorties_imm), 'departs', 4, -1);
    pousser(n(ligne.sorties_ni), 'departs', 0, -1);
    // Sorties pas encore publiées (U3) : le reste non ventilé sort par la vanne des départs.
    flux(ligne.non_ventile_imm, 4, 'arrivees', 'departs');
    flux(ligne.non_ventile_ni, 0, 'arrivees', 'departs');
  }
  flux(ligne.ajust_imm, 4, 'ajustement', 'ajustement');
  flux(ligne.ajust_ni, 0, 'ajustement', 'ajustement');

  // Arrondis : on retombe sur le stock suivant, teinte par teinte.
  const s0 = stocks(ligne);
  const s1 = stocks(suivante);
  for (const teinte of TEINTES) {
    const solde = brut.filter((m) => m.teinte === teinte).reduce((s, m) => s + m.sens, 0);
    const reste = n(s1[teinte]) - n(s0[teinte]) - solde;
    if (reste !== 0) pousser(Math.abs(reste), 'arrondi', teinte, reste > 0 ? 1 : -1);
  }

  const r = alea(ligne.annee);
  return brut.map((m) => ({ ...m, t: r() })).sort((x, y) => x.t - y.t) as Mouvement[];
}

/**
 * Bornes des colonnes de la piscine décantée (fractions de la largeur du bassin, de gauche à
 * droite : autres, G3, G2 un parent, G2 deux parents, G1).
 */
export function couches(effectifs: Record<Teinte, number>): Record<Teinte, [number, number]> {
  const total = TEINTES.reduce<number>((s, t) => s + effectifs[t], 0) || 1;
  let bas = 0;
  const out = {} as Record<Teinte, [number, number]>;
  for (const t of TEINTES) {
    const h = effectifs[t] / total;
    out[t] = [bas, bas + h];
    bas += h;
  }
  return out;
}

export type Debits = Record<
  'naissances' | 'arrivees' | 'deces' | 'departs',
  Record<Teinte, number>
>;

/**
 * Débits de l'année par vanne et par teinte (épaisseur des rubans). Avant 2006 (reconstruit),
 * seul le solde net passe : positif par les arrivées, négatif par les départs. Les flux non
 * ventilés des années partielles (sorties pas encore publiées) passent par leur solde.
 */
export function debits(l: AnneePiscine): Debits {
  const vide = (): Record<Teinte, number> => ({ 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 });
  const arr = vide();
  const dep = vide();
  const pos = (x: number | null | undefined) => Math.max(0, x ?? 0);
  const neg = (x: number | null | undefined) => Math.max(0, -(x ?? 0));
  if (l.statut_flux === 'reconstruit') {
    arr[4] = pos(l.net_imm);
    arr[0] = pos(l.net_ni);
    dep[4] = neg(l.net_imm);
    dep[0] = neg(l.net_ni);
  } else {
    arr[4] = pos(l.entrees_imm) + pos(l.non_ventile_imm);
    arr[0] = pos(l.entrees_ni) + pos(l.non_ventile_ni);
    dep[4] = pos(l.sorties_imm) + neg(l.non_ventile_imm);
    dep[0] = pos(l.sorties_ni) + neg(l.non_ventile_ni);
  }
  return {
    naissances: naissancesParTeinte(l),
    arrivees: arr,
    deces: decesParTeinte(l),
    departs: dep
  };
}

export const somme = (r: Record<Teinte, number>) => TEINTES.reduce<number>((s, t) => s + r[t], 0);

/** Solde migratoire de l'année (immigrés et non-immigrés), hors ajustements de champ ou de collecte. */
export function solde(l: AnneePiscine): number {
  if (l.statut_flux === 'reconstruit') return (l.net_imm ?? 0) + (l.net_ni ?? 0);
  const v = (x: number | null | undefined) => x ?? 0;
  return (
    v(l.entrees_imm) -
    v(l.sorties_imm) +
    v(l.non_ventile_imm) +
    v(l.entrees_ni) -
    v(l.sorties_ni) +
    v(l.non_ventile_ni)
  );
}

/**
 * Cumul des flux de l'année `de` (incluse) jusqu'au 1er janvier de `a` : naissances, décès et
 * solde migratoire passés par les vannes entre les deux dates.
 */
export function cumuls(annees: AnneePiscine[], de: number, a: number) {
  let naissances = 0;
  let deces = 0;
  let migration = 0;
  for (const l of annees) {
    if (l.annee < de || l.annee >= a) continue;
    naissances += l.naissances ?? 0;
    deces += l.deces ?? 0;
    migration += solde(l);
  }
  return { naissances, deces, migration };
}

/** Libellés des régimes de données, affichés sur la piscine. */
export const STATUTS: Record<Statut, { libelle: string; detail: string }> = {
  mesure: {
    libelle: 'Mesuré',
    detail: 'Entrées, sorties et décès des immigrés publiés par l’Insee.'
  },
  partiel: {
    libelle: 'Partiel',
    detail: 'Entrées publiées ; sorties pas encore mesurées. Décès d’immigrés estimés.'
  },
  reconstruit: {
    libelle: 'Reconstruit',
    detail:
      'Avant 2006, seul le flux net des immigrés se reconstruit (recensements et décès estimés) : arrivées et départs ne sont pas séparables.'
  }
};

export const CHAMPS: Record<string, string> = {
  metropole: 'France métropolitaine',
  france_hors_mayotte: 'France hors Mayotte',
  france: 'France'
};
