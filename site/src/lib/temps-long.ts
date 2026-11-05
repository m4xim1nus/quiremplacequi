// Calculs purs de la page « Le temps long » (modules B1, B2, B3, B5) : sans DOM, testés.

export interface PointStock {
  annee: number;
  immigres: number;
  part: number;
  population: number;
  champ: string;
  statut: string;
  rupture: boolean;
}

export interface Vitesse {
  debut: number;
  fin: number;
  points: number;
  effectif: number;
  effectifParAn: number;
  partDebut: number;
  partFin: number;
}

/** Hausse de la part (en points) et de l'effectif entre deux années de la série B1. */
export function vitesse(serie: PointStock[], debut: number, fin: number): Vitesse {
  const a = serie.find((p) => p.annee === debut);
  const b = serie.find((p) => p.annee === fin);
  if (!a || !b) throw new Error(`vitesse : année absente (${debut} ou ${fin})`);
  return {
    debut,
    fin,
    points: Math.round((b.part - a.part) * 10) / 10,
    effectif: b.immigres - a.immigres,
    effectifParAn: Math.round((b.immigres - a.immigres) / (fin - debut)),
    partDebut: a.part,
    partFin: b.part
  };
}

/**
 * Coupe une série en segments continus : avant et après une rupture de série (U5), les points
 * ne sont pas comparables et ne doivent pas être reliés par un trait.
 */
export function segments<T extends { annee: number; rupture?: boolean }>(serie: T[]): T[][] {
  const out: T[][] = [];
  let courant: T[] = [];
  for (const p of serie) {
    if (p.rupture && courant.length) {
      out.push(courant);
      courant = [];
    }
    courant.push(p);
  }
  if (courant.length) out.push(courant);
  return out;
}

/** Années où le champ change (U6) : la première année du nouveau champ. */
export function changementsDeChamp(serie: PointStock[]): { annee: number; champ: string }[] {
  const out = [];
  for (let i = 1; i < serie.length; i++)
    if (serie[i].champ !== serie[i - 1].champ)
      out.push({ annee: serie[i].annee, champ: serie[i].champ });
  return out;
}

/** Sommet d'une série (première occurrence du maximum). */
export function sommet<T>(serie: T[], val: (x: T) => number): T {
  return serie.reduce((m, x) => (val(x) > val(m) ? x : m), serie[0]);
}

export interface Vague {
  nationalite: string;
  groupe: string;
  points: { annee: number; part: number }[];
  pic: { annee: number; part: number };
  derniere: { annee: number; part: number };
}

/** Une vague par nationalité, triées par année du pic puis par hauteur du pic. */
export function vagues(
  lignes: { annee: number; nationalite: string; groupe: string; part_pct: number }[]
): Vague[] {
  const par = new Map<string, Vague>();
  for (const l of lignes) {
    const v = par.get(l.nationalite) ?? {
      nationalite: l.nationalite,
      groupe: l.groupe,
      points: [],
      pic: { annee: 0, part: -1 },
      derniere: { annee: 0, part: 0 }
    };
    v.points.push({ annee: l.annee, part: l.part_pct });
    par.set(l.nationalite, v);
  }
  for (const v of par.values()) {
    v.points.sort((a, b) => a.annee - b.annee);
    v.pic = sommet(v.points, (p) => p.part);
    v.derniere = v.points[v.points.length - 1];
  }
  return [...par.values()].sort((a, b) => a.pic.annee - b.pic.annee || b.pic.part - a.pic.part);
}

export const CHAMPS_LIBELLES: Record<string, string> = {
  metropole: 'France métropolitaine',
  france_hors_mayotte: 'France hors Mayotte',
  france: 'France'
};
