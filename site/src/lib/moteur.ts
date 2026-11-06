// Moteur de particules de la piscine : l'état de l'eau et son évolution dans le temps.
// Sans DOM (le dessin est dans components/Piscine.svelte) ; coordonnées normalisées (0-1) de la
// scène, converties en pixels au dessin.
//
// La scène se lit de haut en bas : deux robinets (naissances, arrivées) versent par des rubans
// d'épaisseur proportionnelle au débit dans les colonnes du bassin (une par génération, de largeur
// proportionnelle à l'effectif quand l'eau est décantée) ; chaque colonne se vide par le fond vers
// deux bondes (décès, départs).

import {
  alea,
  couches,
  debits,
  mouvements,
  partNesAvant,
  particules,
  somme,
  stocks,
  TEINTES,
  type AnneePiscine,
  type Debits,
  type Mouvement,
  type Teinte,
  type Vanne
} from './piscine';

/** Géométrie normalisée de la scène (fractions de la largeur et de la hauteur). */
export const SCENE = {
  bassin: { x0: 0.05, x1: 0.95, haut: 0.21, bas: 0.79 },
  /** Robinets (en haut) et bondes (en bas) : abscisse, et ordonnées du tuyau droit. */
  vannes: {
    naissances: { x: 0.3, y0: 0, y1: 0.06 },
    arrivees: { x: 0.8, y0: 0, y1: 0.06 },
    deces: { x: 0.3, y0: 0.94, y1: 1 },
    departs: { x: 0.8, y0: 0.94, y1: 1 }
  },
  /** Largeur du plus gros débit de la période (fraction de la largeur de la scène). */
  largeurMax: 0.075
} as const;

export type Vannes = { [K in keyof typeof SCENE.vannes]: { x: number; y0: number; y1: number } };

/** Sur écran étroit, les vannes se rapprochent du centre pour laisser la place aux étiquettes. */
export function geometrie(etroit: boolean): Vannes {
  if (!etroit) return SCENE.vannes;
  const v = SCENE.vannes;
  return {
    naissances: { ...v.naissances, x: 0.4 },
    arrivees: { ...v.arrivees, x: 0.66 },
    deces: { ...v.deces, x: 0.4 },
    departs: { ...v.departs, x: 0.66 }
  };
}

export const ETATS = { eau: 0, entre: 1, sort: 2, apparait: 3, disparait: 4 } as const;

type Flux = 'naissances' | 'arrivees' | 'deces' | 'departs';
const ENTREES: Flux[] = ['naissances', 'arrivees'];
const SORTIES: Flux[] = ['deces', 'departs'];

/**
 * Un ruban : le trajet d'un débit (une vanne, une teinte) entre un robinet et le haut d'une
 * colonne, ou entre le fond d'une colonne et une bonde. `xa, ya` : départ ; `xb, yb` : arrivée.
 */
export interface Ruban {
  vanne: Flux;
  teinte: Teinte;
  largeur: number;
  xa: number;
  ya: number;
  xb: number;
  yb: number;
}

/** Point d'un ruban à l'abscisse curviligne `s` (0-1) et au décalage latéral `lat` (−0,5 à 0,5). */
export function surRuban(r: Ruban, s: number, lat = 0): [number, number] {
  const k = 1 - s;
  const b0 = k * k * k;
  const b1 = 3 * k * k * s;
  const b2 = 3 * k * s * s;
  const b3 = s * s * s;
  const ym = (r.ya + r.yb) / 2;
  const d = lat * r.largeur;
  return [(b0 + b1) * (r.xa + d) + (b2 + b3) * (r.xb + d), b0 * r.ya + (b1 + b2) * ym + b3 * r.yb];
}

export interface Particule {
  /** Position dans l'eau mélangée (0-1 en largeur, 0-1 en hauteur depuis le fond). */
  u: number;
  v: number;
  /** Profondeur visée (les entrées descendent doucement depuis la surface). */
  vCible: number;
  /** Position dans sa colonne quand l'eau est décantée (0-1 en largeur). */
  rang: number;
  /** Sur un ruban : abscisse curviligne (négative pendant la descente vers la bonde). */
  s: number;
  lat: number;
  /** Position libre (départ d'une sortie), en coordonnées de scène. */
  x: number;
  y: number;
  teinte: Teinte;
  etat: number;
  vanne: Vanne | null;
  /** Opacité (0-1). */
  alpha: number;
  /** L'ajustement est montré (anneau gris) ou silencieux (arrondi). */
  marque: boolean;
  /** Présente dans l'eau à l'année de départ (`Moteur.origine`), jamais sortie depuis. */
  origine: boolean;
}

/** Durées (secondes réelles) des trajets : robinet → surface, eau → bouche, bouche → bonde. */
const TRAJET = 1.1;
const DESCENTE = 0.45;
/** Marge de chaque côté d'une colonne décantée (fraction de la largeur du bassin). */
const MARGE = 0.006;
/** Marge relative d'une colonne de largeur `l` (fraction du bassin). */
const marge = (l: number) => Math.min(0.3, (2 * MARGE) / Math.max(l, 1e-6));

export class Moteur {
  particules: Particule[] = [];
  temps = 0; // années (float)
  private annees: Map<number, AnneePiscine>;
  private capacite: number;
  private debitMax: number;
  private file: Mouvement[] = [];
  private curseur = 0;
  private anneeFile = -1;
  private r = alea(1);
  /** 0 = eau mélangée, 1 = décantée en colonnes (non miscible) ; `decanteCible` est animé. */
  decante = 1;
  decanteCible = 1;
  bornes: Record<Teinte, [number, number]> = couches({ 0: 1, 1: 0, 2: 0, 3: 0, 4: 0 });
  rubans: Ruban[] = [];
  debut: number;
  fin: number;

  vannes: Vannes;
  /** Année de départ : l'eau de cette année est suivie (particules `origine`). */
  origine = 0;
  /** Probabilité qu'une sortie de l'année prenne une particule d'origine. */
  private pOrigine = 0;

  /**
   * `nesAvant` (pyramides des âges) : la part d'origine encore présente suit la part observée des
   * habitants nés avant l'année de départ, au lieu de dépendre du hasard des sorties.
   */
  constructor(
    donnees: AnneePiscine[],
    public echelle: number,
    etroit = false,
    private nesAvant?: Record<number, number[]>
  ) {
    this.vannes = geometrie(etroit);
    this.annees = new Map(donnees.map((a) => [a.annee, a]));
    this.debut = donnees[0].annee;
    this.fin = donnees[donnees.length - 1].annee;
    this.capacite = Math.max(...donnees.map((a) => a.population)) * 1.04;
    this.debitMax = Math.max(
      ...donnees.flatMap((l) => Object.values(debits(l)).map((r) => somme(r)))
    );
    this.aller(this.debut);
  }

  /** Hauteur d'eau (fraction de la profondeur du bassin) pour une année (float). */
  niveau(t = this.temps): number {
    const a = Math.min(Math.floor(t), this.fin);
    const p0 = this.annees.get(a)!.population;
    const p1 = (this.annees.get(a + 1) ?? this.annees.get(a)!).population;
    return (p0 + (p1 - p0) * (t - a)) / this.capacite;
  }

  /** Ordonnée (scène) de la surface. */
  surface(niveau = this.niveau()): number {
    const { haut, bas } = SCENE.bassin;
    return bas - (bas - haut) * niveau;
  }

  ligne(a: number): AnneePiscine | undefined {
    return this.annees.get(a);
  }

  /** Abscisse (scène) du centre de la colonne d'une teinte, eau décantée ou mélangée. */
  centre(t: Teinte): number {
    const { x0, x1 } = SCENE.bassin;
    const [lo, hi] = this.bornes[t];
    const dec = x0 + ((lo + hi) / 2) * (x1 - x0);
    // Eau mélangée : les rubans versent à intervalles réguliers sur toute la largeur.
    const mel = x0 + ((t + 0.5) / TEINTES.length) * (x1 - x0);
    return mel + (dec - mel) * this.decante;
  }

  /** Les rubans de l'année en cours, à la géométrie du moment (niveau, colonnes). */
  calculerRubans(d: Debits = debits(this.ligne(Math.min(this.fin, Math.floor(this.temps)))!)) {
    const { bassin, largeurMax } = SCENE;
    const vannes = this.vannes;
    const surface = this.surface();
    const larg = (x: number) => (x / this.debitMax) * largeurMax;
    const out: Ruban[] = [];
    // Départ de chaque ruban : empilés au robinet ou à la bonde, dans l'ordre des colonnes.
    const depart: Record<string, number> = {};
    for (const v of [...ENTREES, ...SORTIES]) {
      const total = larg(somme(d[v]));
      let x = vannes[v].x - total / 2;
      for (const t of TEINTES) {
        const l = larg(d[v][t]);
        depart[`${v}-${t}`] = x + l / 2;
        x += l;
      }
    }
    // Arrivée : empilés en haut (entrées) ou au fond (sorties) de chaque colonne.
    for (const [groupe, y, yVanne] of [
      [ENTREES, surface, vannes.naissances.y1],
      [SORTIES, bassin.bas, vannes.deces.y0]
    ] as const) {
      for (const t of TEINTES) {
        const largeurs = groupe.map((v) => larg(d[v][t]));
        const total = largeurs.reduce((a, b) => a + b, 0);
        let x = this.centre(t) - total / 2;
        groupe.forEach((v, i) => {
          const l = largeurs[i];
          if (l > 0) {
            const xc = x + l / 2;
            const xv = depart[`${v}-${t}`];
            out.push(
              groupe === ENTREES
                ? { vanne: v, teinte: t, largeur: l, xa: xv, ya: yVanne, xb: xc, yb: y }
                : { vanne: v, teinte: t, largeur: l, xa: xc, ya: y, xb: xv, yb: yVanne }
            );
          }
          x += l;
        });
      }
    }
    this.rubans = out;
    return out;
  }

  private ruban(vanne: Vanne | null, teinte: Teinte): Ruban | undefined {
    return this.rubans.find((r) => r.vanne === vanne && r.teinte === teinte);
  }

  /** Saut direct à une année : l'eau est reconstruite au stock exact de cette année. */
  aller(annee: number) {
    const a = Math.max(this.debut, Math.min(this.fin, Math.round(annee)));
    const l = this.annees.get(a)!;
    this.r = alea(a * 7919);
    this.particules = [];
    const st = stocks(l);
    for (const t of TEINTES) {
      for (let i = 0, k = particules(st[t], this.echelle); i < k; i++) {
        const v = this.r();
        const p = this.nouvelle(this.r(), v, t, ETATS.eau, null);
        p.origine = true;
        this.particules.push(p);
      }
    }
    this.origine = a;
    this.bornes = couches(this.compter());
    // Ordre de dessin mélangé : aucune teinte ne recouvre les autres.
    for (let i = this.particules.length - 1; i > 0; i--) {
      const j = Math.floor(this.r() * (i + 1));
      [this.particules[i], this.particules[j]] = [this.particules[j], this.particules[i]];
    }
    this.temps = a;
    this.preparer(a);
    this.calculerRubans();
  }

  private nouvelle(u: number, v: number, teinte: Teinte, etat: number, vanne: Vanne | null) {
    return {
      u,
      v,
      vCible: v,
      rang: this.r(),
      s: 0,
      lat: 0,
      x: 0,
      y: 0,
      teinte,
      etat,
      vanne,
      alpha: 1,
      marque: false,
      origine: false
    } satisfies Particule as Particule;
  }

  private preparer(a: number) {
    const l = this.annees.get(a);
    const s = this.annees.get(a + 1);
    this.file = l && s ? mouvements(l, s, this.echelle) : [];
    this.curseur = 0;
    this.anneeFile = a;
    this.pOrigine = 0;
    if (this.nesAvant && l && s) {
      const st = stocks(s);
      const total = TEINTES.reduce<number>((n, t) => n + particules(st[t], this.echelle), 0);
      const cible = Math.round(total * partNesAvant(this.nesAvant, this.origine, a + 1));
      const reste = this.particules.filter(
        (p) => p.origine && (p.etat === ETATS.eau || p.etat === ETATS.apparait)
      ).length;
      const sorties = this.file.filter((m) => m.sens === -1).length;
      if (Number.isFinite(cible) && sorties > 0)
        this.pOrigine = Math.max(0, Math.min(1, (reste - cible) / sorties));
    }
  }

  /** Particules d'origine encore dans l'eau. */
  restantes(): number {
    let n = 0;
    for (const p of this.particules)
      if (p.origine && p.etat !== ETATS.sort && p.etat !== ETATS.disparait) n++;
    return n;
  }

  /**
   * Avance le temps de `dt` années. `instantane` (mouvement réduit) : les mouvements s'appliquent
   * sans animation.
   */
  avancer(dt: number, instantane = false) {
    const cible = Math.min(this.fin, this.temps + dt);
    while (this.temps < cible) {
      const a = Math.floor(this.temps);
      if (a !== this.anneeFile) this.preparer(a);
      const finAnnee = Math.min(cible, a + 1);
      const frac = finAnnee - a;
      while (this.curseur < this.file.length && this.file[this.curseur].t <= frac) {
        this.appliquer(this.file[this.curseur++], instantane);
      }
      this.temps = finAnnee;
      if (finAnnee === a + 1 && a + 1 <= this.fin) this.preparer(a + 1);
      if (finAnnee >= this.fin) break;
    }
  }

  private appliquer(m: Mouvement, instantane: boolean) {
    const lat = (this.r() - 0.5) * 0.8;
    if (m.sens === 1) {
      const v = this.r();
      const p = this.nouvelle(this.r(), v, m.teinte, ETATS.eau, m.vanne);
      if (instantane) {
        this.particules.push(p);
      } else if (m.vanne === 'naissances' || m.vanne === 'arrivees') {
        p.etat = ETATS.entre;
        p.s = 0;
        p.lat = lat;
        this.particules.push(p);
      } else {
        p.etat = ETATS.apparait;
        p.alpha = 0;
        p.marque = m.vanne === 'ajustement';
        this.particules.push(p);
      }
      return;
    }
    // Sortie : une particule de la bonne teinte, prise au hasard dans l'eau.
    const i = this.choisir(m.teinte);
    if (i < 0) return;
    if (instantane) {
      this.retirer(i);
      return;
    }
    const p = this.particules[i];
    p.vanne = m.vanne;
    if (m.vanne === 'ajustement' || m.vanne === 'arrondi') {
      p.etat = ETATS.disparait;
      p.marque = m.vanne === 'ajustement';
    } else {
      const [x, y] = this.position(p);
      p.etat = ETATS.sort;
      p.x = x;
      p.y = y;
      p.s = -1;
      p.lat = lat;
    }
  }

  private choisir(teinte: Teinte): number {
    const n = this.particules.length;
    const origine = this.r() < this.pOrigine;
    for (let essai = 0; essai < 400; essai++) {
      const i = Math.floor(this.r() * n);
      const p = this.particules[i];
      if (p.teinte === teinte && p.etat === ETATS.eau && p.origine === origine) return i;
    }
    for (let essai = 0; essai < 200; essai++) {
      const i = Math.floor(this.r() * n);
      const p = this.particules[i];
      if (p.teinte === teinte && p.etat === ETATS.eau) return i;
    }
    return this.particules.findIndex((p) => p.teinte === teinte && p.etat === ETATS.eau);
  }

  private retirer(i: number) {
    const dernier = this.particules.pop()!;
    if (i < this.particules.length) this.particules[i] = dernier;
  }

  /** Position (scène) d'une particule, où qu'elle soit. */
  position(p: Particule, niveau = this.niveau()): [number, number] {
    if (p.etat === ETATS.entre) {
      const r = this.ruban(p.vanne, p.teinte);
      if (r) return surRuban(r, p.s, p.lat);
    } else if (p.etat === ETATS.sort) {
      const r = this.ruban(p.vanne, p.teinte);
      if (r) {
        if (p.s >= 0) return surRuban(r, p.s, p.lat);
        // Descente vers la bouche de la colonne.
        const [bx, by] = surRuban(r, 0, p.lat);
        const k = 1 + p.s;
        const e = k * k * (3 - 2 * k);
        return [p.x + (bx - p.x) * e, p.y + (by - p.y) * e];
      }
      return [p.x, p.y];
    }
    const { x0, x1, haut, bas } = SCENE.bassin;
    const bord = 0.01;
    const hauteur = (bas - haut) * niveau;
    let u = p.u;
    if (this.decante > 0) {
      const [lo, hi] = this.bornes[p.teinte];
      const m = marge(hi - lo);
      const ud = lo + (hi - lo) * (m / 2 + (1 - m) * p.rang);
      u = u + (ud - u) * this.decante;
    }
    return [
      x0 + bord + u * (x1 - x0 - 2 * bord),
      bas - bord - p.v * Math.max(0, hauteur - 2 * bord)
    ];
  }

  /** Animation des particules (indépendante du temps des données) : `dt` en secondes réelles. */
  animer(dt: number, horloge: number, calme = false) {
    const agitation = calme ? 0 : 0.004;
    const pas = calme ? 1 : Math.min(1, dt * 2.5);
    this.decante += (this.decanteCible - this.decante) * pas;
    if (Math.abs(this.decanteCible - this.decante) < 0.002) this.decante = this.decanteCible;
    this.bornes = couches(this.compter());
    this.calculerRubans();
    const { x0, x1 } = SCENE.bassin;
    for (let i = this.particules.length - 1; i >= 0; i--) {
      const p = this.particules[i];
      if (p.etat === ETATS.eau || p.etat === ETATS.apparait || p.etat === ETATS.disparait) {
        // Courants lents et agitation : l'eau ne repose jamais.
        p.u +=
          (Math.sin(horloge * 0.6 + p.v * 9) * 0.0006 + (this.r() - 0.5) * agitation) *
          dt *
          60 *
          0.1;
        p.rang += (this.r() - 0.5) * agitation * dt * 6;
        p.v += (p.vCible - p.v) * Math.min(1, dt * 0.8) + (this.r() - 0.5) * agitation * dt * 6;
        if (p.u < 0) p.u = -p.u;
        if (p.u > 1) p.u = 2 - p.u;
        p.rang = Math.max(0, Math.min(1, p.rang));
        p.v = Math.max(0, Math.min(1, p.v));
        if (p.etat === ETATS.apparait) {
          p.alpha = Math.min(1, p.alpha + dt * 1.5);
          if (p.alpha >= 1) {
            p.etat = ETATS.eau;
            p.marque = false;
          }
        } else if (p.etat === ETATS.disparait) {
          p.alpha -= dt * 1.5;
          if (p.alpha <= 0) this.retirer(i);
        }
      } else if (p.etat === ETATS.entre) {
        p.s += dt / TRAJET;
        if (p.s >= 1) {
          // Arrivée à la surface, dans sa colonne, puis lente descente.
          const r = this.ruban(p.vanne, p.teinte);
          const x = r ? surRuban(r, 1, p.lat)[0] : (x0 + x1) / 2;
          const f = Math.max(0, Math.min(1, (x - x0) / (x1 - x0)));
          const [lo, hi] = this.bornes[p.teinte];
          p.u = f;
          const m = marge(hi - lo);
          p.rang =
            hi > lo ? Math.max(0, Math.min(1, ((f - lo) / (hi - lo) - m / 2) / (1 - m))) : 0.5;
          p.v = 1;
          p.etat = ETATS.eau;
        }
      } else if (p.etat === ETATS.sort) {
        p.s += dt / (p.s < 0 ? DESCENTE : TRAJET);
        p.alpha = p.s > 0.8 ? Math.max(0, (1 - p.s) * 5) : 1;
        if (p.s >= 1 || !this.ruban(p.vanne, p.teinte)) this.retirer(i);
      }
    }
  }

  /** Particules par teinte dans l'eau (hors entrées et sorties en cours). */
  compter(): Record<Teinte, number> {
    const c: Record<Teinte, number> = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 };
    for (const p of this.particules)
      if (p.etat === ETATS.eau || p.etat === ETATS.apparait) c[p.teinte]++;
    return c;
  }

  /** Comptes par teinte, entrées comprises, sorties exclues (tests). */
  comptes(): number[] {
    const c = [0, 0, 0, 0, 0];
    for (const p of this.particules)
      if (p.etat !== ETATS.sort && p.etat !== ETATS.disparait) c[p.teinte]++;
    return c;
  }
}
