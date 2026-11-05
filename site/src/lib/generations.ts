// Logique pure de la page « Générations » (E1-E3, E9, E10, F2 de docs/CADRAGE.md §4) : à partir
// des cellules saisies de TeO2 et d'IP 1910, les paliers du curseur de définition et les sommes
// affichées. Sans accès disque, testée.

export interface Cellule {
  fichier: string;
  ligne: string;
  colonne: string;
  valeur: number;
  unite: string;
  approx: boolean;
  champ: string;
  precision: number | null;
}

/** Une valeur, ou une erreur explicite : une cellule manquante ne doit jamais devenir 0. */
export function valeur(cs: Cellule[], fichier: string, ligne: string, colonne: string): number {
  const c = cs.find((x) => x.fichier === fichier && x.ligne === ligne && x.colonne === colonne);
  if (!c) throw new Error(`cellule introuvable : ${fichier} / ${ligne} / ${colonne}`);
  return c.valeur;
}

export interface Palier {
  cle: string;
  libelle: string;
  ajout: number;
  cumul: number;
  /** Valeur déduite (non publiée telle quelle). */
  deduit: boolean;
}

/** Paliers cumulés : chaque étape ajoute un groupe à « ceux que l'on compte ». */
export function paliers(etapes: Omit<Palier, 'cumul'>[]): Palier[] {
  let cumul = 0;
  return etapes.map((e) => {
    cumul += e.ajout;
    return { ...e, cumul: Math.round(cumul * 10) / 10 };
  });
}

/** Rapport entre le dernier et le premier palier (« du simple au … »). */
export const etendue = (p: Palier[]) => p[p.length - 1].cumul / p[0].cumul;

/** Somme d'une ligne sur des colonnes, pour montrer de quoi un chiffre agrégé est fait. */
export function somme(cs: Cellule[], fichier: string, ligne: string, colonnes: string[]): number {
  return colonnes.reduce((s, c) => s + valeur(cs, fichier, ligne, c), 0);
}

/** Écart d'une ligne en % à 100 (pour signaler les anomalies de la source). */
export function ecartA100(cs: Cellule[], fichier: string, ligne: string): number {
  const v = cs.filter((x) => x.fichier === fichier && x.ligne === ligne && x.unite === '%');
  return v.reduce((s, x) => s + x.valeur, 0) - 100;
}

/** Format français d'un pourcentage saisi (entiers sans décimale, sinon une). */
export function pc(x: number): string {
  const s = Number.isInteger(x) ? String(x) : x.toFixed(1).replace('.', ',');
  return `${s.replace('-', '−')}\u00a0%`;
}

/** Format d'un écart en points, signé. */
export function pts(x: number): string {
  const s = Math.abs(x).toFixed(1).replace('.', ',');
  return `${x > 0 ? '+' : x < 0 ? '−' : ''}${s}\u00a0pt`;
}
