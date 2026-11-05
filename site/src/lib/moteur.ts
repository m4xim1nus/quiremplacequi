// Moteur de particules de la piscine : l'état de l'eau et son évolution dans le temps.
// Sans DOM (le dessin est dans components/Piscine.svelte) ; coordonnées normalisées (0-1) de la
// scène, converties en pixels au dessin.

import {
  alea,
  mouvements,
  particules,
  type AnneePiscine,
  type Mouvement,
  type Teinte,
  type Vanne
} from './piscine';

/** Géométrie normalisée de la scène (fractions de la largeur et de la hauteur). */
export const SCENE = {
  bassin: { x0: 0.1, x1: 0.9, haut: 0.2, bas: 0.93 },
  vannes: {
    naissances: { x: 0.22, y: 0.135 },
    arrivees: { x: 0.78, y: 0.135 },
    deces: { x: 0.1, y: 0.99 },
    departs: { x: 0.9, y: 0.99 }
  }
} as const;

export const ETATS = { eau: 0, entre: 1, sort: 2, apparait: 3, disparait: 4 } as const;

export interface Particule {
  /** Position dans l'eau (0-1 en largeur, 0-1 en hauteur depuis le fond). */
  u: number;
  v: number;
  /** Profondeur visée (les arrivées descendent doucement). */
  vCible: number;
  /** Position libre (chute ou sortie), en coordonnées de scène. */
  x: number;
  y: number;
  vx: number;
  vy: number;
  teinte: Teinte;
  etat: number;
  /** Vanne de sortie ou d'entrée (dessin), et 0-1 d'opacité. */
  vanne: Vanne | null;
  alpha: number;
  /** L'ajustement est montré (anneau gris) ou silencieux (arrondi). */
  marque: boolean;
}

export class Moteur {
  particules: Particule[] = [];
  temps = 0; // années (float)
  private annees: Map<number, AnneePiscine>;
  private capacite: number;
  private file: Mouvement[] = [];
  private curseur = 0;
  private anneeFile = -1;
  private r = alea(1);
  debut: number;
  fin: number;

  constructor(
    donnees: AnneePiscine[],
    public echelle: number
  ) {
    this.annees = new Map(donnees.map((a) => [a.annee, a]));
    this.debut = donnees[0].annee;
    this.fin = donnees[donnees.length - 1].annee;
    this.capacite = Math.max(...donnees.map((a) => a.population)) * 1.12;
    this.aller(this.debut);
  }

  /** Hauteur d'eau (fraction de la profondeur du bassin) pour une année (float). */
  niveau(t = this.temps): number {
    const a = Math.min(Math.floor(t), this.fin);
    const p0 = this.annees.get(a)!.population;
    const p1 = (this.annees.get(a + 1) ?? this.annees.get(a)!).population;
    return (p0 + (p1 - p0) * (t - a)) / this.capacite;
  }

  ligne(a: number): AnneePiscine | undefined {
    return this.annees.get(a);
  }

  /** Saut direct à une année : l'eau est reconstruite au stock exact de cette année. */
  aller(annee: number) {
    const a = Math.max(this.debut, Math.min(this.fin, Math.round(annee)));
    const l = this.annees.get(a)!;
    this.r = alea(a * 7919);
    this.particules = [];
    const ajouter = (k: number, teinte: Teinte) => {
      for (let i = 0; i < k; i++) {
        const v = this.r();
        this.particules.push(this.nouvelle(this.r(), v, v, teinte, ETATS.eau, null));
      }
    };
    ajouter(particules(l.non_immigres, this.echelle), 0);
    ajouter(particules(l.immigres, this.echelle), 1);
    // Les immigrés ne forment pas une couche : on mélange l'ordre de dessin.
    for (let i = this.particules.length - 1; i > 0; i--) {
      const j = Math.floor(this.r() * (i + 1));
      [this.particules[i], this.particules[j]] = [this.particules[j], this.particules[i]];
    }
    this.temps = a;
    this.preparer(a);
  }

  private nouvelle(
    u: number,
    v: number,
    vCible: number,
    teinte: Teinte,
    etat: number,
    vanne: Vanne | null
  ): Particule {
    return { u, v, vCible, x: 0, y: 0, vx: 0, vy: 0, teinte, etat, vanne, alpha: 1, marque: false };
  }

  private preparer(a: number) {
    const l = this.annees.get(a);
    const s = this.annees.get(a + 1);
    this.file = l && s ? mouvements(l, s, this.echelle) : [];
    this.curseur = 0;
    this.anneeFile = a;
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
    const { vannes } = SCENE;
    if (m.sens === 1) {
      if (m.vanne === 'naissances' || m.vanne === 'arrivees') {
        const o = vannes[m.vanne];
        const p = this.nouvelle(
          0,
          1,
          this.r(),
          m.teinte,
          instantane ? ETATS.eau : ETATS.entre,
          m.vanne
        );
        p.x = o.x + (this.r() - 0.5) * 0.012;
        p.y = o.y + 0.03;
        p.vx = (m.vanne === 'naissances' ? 1 : -1) * (0.02 + this.r() * 0.05);
        p.vy = 0.05;
        if (instantane) {
          p.u = this.r();
          p.v = p.vCible;
        }
        this.particules.push(p);
      } else {
        const v = this.r();
        const p = this.nouvelle(
          this.r(),
          v,
          v,
          m.teinte,
          instantane ? ETATS.eau : ETATS.apparait,
          m.vanne
        );
        p.alpha = instantane ? 1 : 0;
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
      p.etat = ETATS.sort;
      const [x, y] = this.position(p);
      p.x = x;
      p.y = y;
      p.vx = 0;
      p.vy = 0;
    }
  }

  private choisir(teinte: Teinte): number {
    const n = this.particules.length;
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

  /** Position (scène) d'une particule dans l'eau. */
  position(p: Particule, niveau = this.niveau()): [number, number] {
    const { x0, x1, haut, bas } = SCENE.bassin;
    const marge = 0.012;
    const hauteur = (bas - haut) * niveau;
    return [
      x0 + marge + p.u * (x1 - x0 - 2 * marge),
      bas - marge - p.v * Math.max(0, hauteur - 2 * marge)
    ];
  }

  /** Animation des particules (indépendante du temps des données) : `dt` en secondes réelles. */
  animer(dt: number, horloge: number, calme = false) {
    const { bassin, vannes } = SCENE;
    const niveau = this.niveau();
    const surface = bassin.bas - (bassin.bas - bassin.haut) * niveau;
    const agitation = calme ? 0 : 0.004;
    for (let i = this.particules.length - 1; i >= 0; i--) {
      const p = this.particules[i];
      if (p.etat === ETATS.eau || p.etat === ETATS.apparait || p.etat === ETATS.disparait) {
        // Courants lents et agitation : l'eau ne repose jamais.
        p.u +=
          (Math.sin(horloge * 0.6 + p.v * 9) * 0.0006 + (this.r() - 0.5) * agitation) *
          dt *
          60 *
          0.1;
        p.v += (p.vCible - p.v) * Math.min(1, dt * 0.8) + (this.r() - 0.5) * agitation * dt * 6;
        if (p.u < 0) p.u = -p.u;
        if (p.u > 1) p.u = 2 - p.u;
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
        p.vy += 0.9 * dt;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (p.y >= surface) {
          const { x0, x1 } = bassin;
          p.u = Math.max(0, Math.min(1, (p.x - x0) / (x1 - x0)));
          p.v = 1;
          p.etat = ETATS.eau;
        }
      } else if (p.etat === ETATS.sort) {
        const o = vannes[p.vanne as 'deces' | 'departs'];
        const dx = o.x - p.x;
        const dy = o.y - p.y;
        const d = Math.hypot(dx, dy);
        const vitesse = 0.35 + (1 - Math.min(1, d)) * 0.4;
        p.x += (dx / (d || 1)) * vitesse * dt;
        p.y += (dy / (d || 1)) * vitesse * dt;
        p.alpha = Math.min(1, d * 6);
        if (d < 0.02) this.retirer(i);
      }
    }
  }

  /** Comptes de particules par teinte dans l'eau (tests et lecture). */
  comptes(): [number, number] {
    const c: [number, number] = [0, 0];
    for (const p of this.particules)
      if (p.etat !== ETATS.sort && p.etat !== ETATS.disparait) c[p.teinte]++;
    return c;
  }
}
