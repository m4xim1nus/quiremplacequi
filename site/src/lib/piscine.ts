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
}

/** Teinte : 0 = non-immigré, 1 = immigré. */
export type Teinte = 0 | 1;

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

  pousser(n(ligne.naissances), 'naissances', 0, 1);
  pousser(n(ligne.deces_imm), 'deces', 1, -1);
  pousser(n(ligne.deces_ni), 'deces', 0, -1);
  if (ligne.statut_flux === 'reconstruit') {
    flux(ligne.net_imm, 1, 'arrivees', 'departs');
    flux(ligne.net_ni, 0, 'arrivees', 'departs');
  } else {
    pousser(n(ligne.entrees_imm), 'arrivees', 1, 1);
    pousser(n(ligne.entrees_ni), 'arrivees', 0, 1);
    pousser(n(ligne.sorties_imm), 'departs', 1, -1);
    pousser(n(ligne.sorties_ni), 'departs', 0, -1);
    // Sorties pas encore publiées (U3) : le reste non ventilé sort par la vanne des départs.
    flux(ligne.non_ventile_imm, 1, 'arrivees', 'departs');
    flux(ligne.non_ventile_ni, 0, 'arrivees', 'departs');
  }
  flux(ligne.ajust_imm, 1, 'ajustement', 'ajustement');
  flux(ligne.ajust_ni, 0, 'ajustement', 'ajustement');

  // Arrondis : on retombe sur le stock suivant.
  for (const teinte of [0, 1] as Teinte[]) {
    const depart = n(teinte ? ligne.immigres : ligne.non_immigres);
    const cible = n(teinte ? suivante.immigres : suivante.non_immigres);
    const solde = brut.filter((m) => m.teinte === teinte).reduce((s, m) => s + m.sens, 0);
    const reste = cible - depart - solde;
    if (reste !== 0) pousser(Math.abs(reste), 'arrondi', teinte, reste > 0 ? 1 : -1);
  }

  const r = alea(ligne.annee);
  return brut.map((m) => ({ ...m, t: r() })).sort((x, y) => x.t - y.t) as Mouvement[];
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
