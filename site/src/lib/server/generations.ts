// Données de la page « Générations », lues au prérendu dans data/export/ (teo2.csv : saisie
// référencée de TeO2 ; ip1910.csv : Insee Première 1910). Aucune valeur n'est écrite à la main.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT } from './donnees';
import { ecartA100, etendue, paliers, somme, valeur, type Cellule } from '$lib/generations';

function cellules(): Cellule[] {
  return csvParse(readFileSync(resolve(EXPORT, 'teo2.csv'), 'utf8')).map((r) => ({
    fichier: r.fichier!,
    ligne: r.ligne!,
    colonne: r.colonne!,
    valeur: Number(r.valeur),
    unite: r.unite!,
    approx: r.approx === 'true',
    champ: r.champ!,
    precision: r.precision ? Number(r.precision) : null
  }));
}

function ip1910(figure: string, ligne: string, colonne: string, bloc?: string): number {
  const rows = csvParse(readFileSync(resolve(EXPORT, 'ip1910.csv'), 'utf8'));
  const r = rows.find(
    (x) =>
      x.figure === figure &&
      x.ligne === ligne &&
      x.colonne === colonne &&
      (bloc === undefined || x.bloc === bloc)
  );
  if (!r) throw new Error(`IP 1910 : cellule introuvable ${figure} / ${ligne} / ${colonne}`);
  return Number(r.valeur);
}

const POURCENT = 'Pourcentages pondérés';
const T1 = 'ch08_tableau1.yaml';
const T3 = 'ch08_tableau3.yaml';
const T4 = 'ch08_tableau4.yaml';
const T6 = 'ch08_tableau6.yaml';
const SEG = 'ch05_tableau1.yaml';
const CHO = 'ch11_figure1.yaml';
const T35 = 'ch11_texte35.yaml';
const DIS = 'ch16_tableau2.yaml';
const IDE = 'ch09_tableau4.yaml';

export const CHAMPS = {
  teo2_18_59: 'France métropolitaine, 18-59 ans, logement ordinaire, 2019-2020',
  couples: 'Personnes vivant en couple, 18-59 ans, France métropolitaine, 2019-2020',
  couples_desc: 'Enfants d’immigrés vivant en couple, 18-59 ans, France métropolitaine, 2019-2020',
  g3: 'Petits-enfants d’immigrés (G3), 18-59 ans, France métropolitaine, 2019-2020',
  g3_enfants: 'Enfants des enquêtés qui sont petits-enfants d’immigrés (G3), tous âges, 2019-2020',
  seg: '18-49 ans, France métropolitaine (TeO1 2008, TeO2 2019-2020)',
  ip1910: 'France métropolitaine, 0-59 ans, logement ordinaire, 2019-2020'
};

export function donneesGenerations() {
  const cs = cellules();
  const v = (f: string, l: string, c: string) => valeur(cs, f, l, c);

  // E1 et F2 : le curseur de définition.
  const g1 = v(T1, 'Immigré·e', POURCENT);
  const g2a = v(T1, 'De deux parents immigrés', POURCENT);
  const g2b = v(T1, 'G2.5 D’un parent immigré', POURCENT);
  const g3 = v(T1, 'G3 Descendant·e', POURCENT);
  const om =
    v(T1, 'Natifs et natives des Outre-mer', POURCENT) +
    v(T1, 'Descendant·e de natifs et natives des Outre-mer', POURCENT);
  const total41 = v(
    'ch08_texte_41pct.yaml',
    'Lien à l’immigration (personnel, par ascendance ou par alliance)',
    'Population de 18 à 59 ans'
  );
  const conjoints = Math.round((total41 - (g1 + g2a + g2b + g3 + om)) * 10) / 10;
  const p = paliers([
    { cle: 'g1', libelle: 'Immigrés (G1)', ajout: g1, deduit: false },
    { cle: 'g2a', libelle: 'Enfants de deux parents immigrés (G2)', ajout: g2a, deduit: false },
    { cle: 'g2b', libelle: 'Enfants d’un parent immigré (G2)', ajout: g2b, deduit: false },
    { cle: 'g3', libelle: 'Petits-enfants d’immigrés (G3)', ajout: g3, deduit: false },
    {
      cle: 'om',
      libelle: 'Originaires des outre-mer et leurs enfants (hors petits-enfants)',
      ajout: om,
      deduit: false
    },
    {
      cle: 'conjoints',
      libelle: 'Conjoints et autres liens',
      ajout: conjoints,
      deduit: true
    }
  ]);
  const ip0 = (c: string) => ip1910('Figure 1', '0-59', c);
  const pIp = paliers([
    { cle: 'g1', libelle: 'Immigrés (G1)', ajout: ip0('Immigrés  (G1)'), deduit: false },
    {
      cle: 'g2a',
      libelle: 'Enfants de deux parents immigrés (G2)',
      ajout: ip0("Descendants d'immigrés (G2) / Deux parents immigrés"),
      deduit: false
    },
    {
      cle: 'g2b',
      libelle: 'Enfants d’un parent immigré (G2)',
      ajout: ip0("Descendants d'immigrés (G2) / Un parent immigré"),
      deduit: false
    },
    {
      cle: 'g3',
      libelle: 'Petits-enfants d’immigrés (G3)',
      ajout:
        Math.round(
          (ip0("Descendants d'immigrés (G3) / Quatre  grands-parents immigrés") +
            ip0("Descendants d'immigrés (G3) / Origines mixtes")) *
            10
        ) / 10,
      deduit: false
    }
  ]);
  const ip18 = (c: string) => ip1910('Figure 1', '18-59', c);
  const ip1910_18_59 =
    Math.round(
      (ip18('Immigrés  (G1)') +
        ip18("Descendants d'immigrés (G2) / Deux parents immigrés") +
        ip18("Descendants d'immigrés (G2) / Un parent immigré") +
        ip18("Descendants d'immigrés (G3) / Quatre  grands-parents immigrés") +
        ip18("Descendants d'immigrés (G3) / Origines mixtes")) *
        10
    ) / 10;
  const g3Moins18 = (n: string) =>
    ip1910(
      'Figure 3a',
      'Ensemble des G3 de moins de 18 ans',
      `Nombre de grands-parents immigrés / ${n}`,
      'Descendants G3 de moins de 18 ans'
    );
  const sansAscendance = {
    deuxGenerations: 100 - g1 - g2a - g2b,
    troisGenerations: v(T1, 'Sans ascendance immigrée sur trois générations', POURCENT)
  };

  // E2 : mixité conjugale.
  const COLS = [
    '(a) Homogamie lien et origine',
    '(b) Homogamie origine, mais lien différent',
    '(c) Conjoint G1 d’une autre origine',
    '(d) Conjoint G2 d’une autre origine',
    '(e) Population majoritaire'
  ];
  const MIXTE = COLS.slice(2);
  const LIGNES_E2 = [
    ['G1 Immigré·e', 'Immigrés (G1)'],
    ['G2 Descendant·e (deux parents immigrés)', 'Enfants de deux parents immigrés (G2)'],
    ['G2.5 Descendant·e (un parent immigré)', 'Enfants d’un parent immigré (G2)'],
    ['Population majoritaire', 'Population majoritaire']
  ];
  const e2 = LIGNES_E2.map(([ligne, libelle]) => ({
    libelle,
    segments: COLS.map((col) => ({
      cle: col,
      valeur:
        cs.find((x) => x.fichier === T3 && x.ligne === ligne && x.colonne === col)?.valeur ?? 0
    })),
    // Pour la population majoritaire, (e) est l'homogamie : le couple mixte, c'est (c) + (d).
    mixte: somme(cs, T3, ligne, ligne === 'Population majoritaire' ? MIXTE.slice(0, 2) : MIXTE),
    majoritaire: v(T3, ligne, '(e) Population majoritaire')
  }));

  // E2 par origine : conjoint des enfants d'immigrés selon l'origine et le sexe (ch. 7, figure 4).
  // Quatre catégories, différentes de celles du tableau 3 du ch. 8 : ne pas les mélanger.
  const F4 = 'ch07_figure4.yaml';
  const COLS7 = [
    'Immigré·e de même origine',
    'Descendant·e de même origine',
    'Immigré·e ou descendant·e d’une autre origine',
    'Français·e sur deux générations'
  ];
  const GROUPES7 = [
    'Ensemble',
    'Deux parents immigrés (G2)',
    'Un parent immigré (G2.5)',
    'Maghreb',
    'Afrique subsaharienne',
    'Turquie, Moyen-Orient',
    'Asie',
    'Europe du Sud',
    'Autres UE 27',
    'Autres pays'
  ];
  const e2origine = GROUPES7.flatMap((g) =>
    ['hommes', 'femmes'].map((sexe) => ({
      libelle: `${g}, ${sexe}`,
      segments: COLS7.map((c) => ({ cle: c, valeur: v(F4, `${g}, ${sexe}`, c) }))
    }))
  );

  // E3 : généalogies des G3.
  const nbGp = ['1', '2', '3', '4'];
  const e3Ensemble = nbGp.map((n) => ({
    n,
    valeur: v(T4, n, 'Ensemble des G3 (enquête principale)'),
    nonEuropeen: v(
      T4,
      n,
      'G3 ayant au moins un grand-parent immigré non européen (enquêtes principale et complémentaire)'
    )
  }));
  const ORIGINES_T6 = [
    'Europe du Sud',
    'Autres UE 27',
    'Maghreb',
    'Afrique subsaharienne',
    'Turquie, Moyen-Orient',
    'Asie',
    'Autres pays',
    'Ensemble'
  ];
  const LIGNES_T6: Record<string, string> = {
    '1': '1 grand-parent immigré',
    '2': '2 grands-parents immigrés',
    '3': '3 grands-parents immigrés',
    '4': '4 grands-parents immigrés'
  };
  const e3Origines = ORIGINES_T6.map((o) => ({
    libelle: o,
    segments: nbGp.map((n) => ({ cle: n, valeur: v(T6, LIGNES_T6[n], o) })),
    effectif: v(T6, 'Effectif non pondéré', o)
  }));
  // TeO2 ch. 8, §39 : mixité dès les grands-parents (1 grand-parent immigré, ou 2 de lignées
  // différentes) et mixité à la génération des parents (2 grands-parents de la même lignée).
  const lignages = {
    grandsParents:
      v(T6, '1 grand-parent immigré', 'Ensemble') + v(T6, 'De lignée différente', 'Ensemble'),
    parents: v(T6, 'De la même lignée', 'Ensemble')
  };
  const ip3a = ['France', 'Espagne, Italie, Portugal', 'Maghreb'].map((o) => ({
    origine: o,
    part: ip1910(
      'Figure 3a',
      o,
      'Part des G3 ayant au moins un grand-parent originaire du pays',
      'Descendants G3 de moins de 18 ans'
    )
  }));

  // E9 : inégalités.
  const SEG_COL = 'Forte concentration d’immigrés (quintile supérieur)';
  const groupesSeg = [
    ['G1 Immigrés', 'Immigrés (G1)'],
    ['G2 Descendants d’immigrés', 'Enfants d’immigrés (G2)'],
    ['Population majoritaire', 'Population majoritaire'],
    ['Maghreb', 'origine : Maghreb'],
    ['Afrique subsaharienne', 'origine : Afrique subsaharienne'],
    ['Europe du Sud', 'origine : Europe du Sud']
  ];
  const segregation = groupesSeg.map(([l, libelle]) => ({
    libelle,
    v2008: v(SEG, l, `${SEG_COL}, 2008`),
    v2019: v(SEG, l, `${SEG_COL}, 2019`)
  }));
  const lignesCho = [...new Set(cs.filter((x) => x.fichier === CHO).map((x) => x.ligne))];
  const chomage = lignesCho.map((l) => ({
    libelle: l,
    hommes: v(CHO, l, 'Hommes'),
    femmes: v(CHO, l, 'Femmes')
  }));
  const precisionCho = cs.find((x) => x.fichier === CHO)?.precision ?? null;
  const DIS_COL = 'Discriminations autodéclarées';
  const groupesDis = [
    ['Population majoritaire', 'Population majoritaire'],
    ['G1', 'Immigrés (G1)'],
    ['G2', 'Enfants de deux parents immigrés (G2)'],
    ['G2.5', 'Enfants d’un parent immigré (G2)'],
    ['G2 Maghreb', 'Enfants d’immigrés (un ou deux parents), Maghreb'],
    ['G2 Afrique sub.', 'Enfants d’immigrés (un ou deux parents), Afrique subsaharienne'],
    ['G1 Europe du Sud', 'Immigrés, Europe du Sud'],
    ['G2 Europe du Sud', 'Enfants d’immigrés (un ou deux parents), Europe du Sud'],
    ['Ensemble', 'Ensemble']
  ];
  const discriminations = groupesDis.map(([l, libelle]) => ({
    libelle,
    valeur: v(DIS, l, DIS_COL)
  }));

  // E10 : le paradoxe.
  const generationsIde = [
    ['G1', 'Immigrés (G1)', 4],
    ['G2 (2 parents immigrés)', 'Enfants de deux parents immigrés (G2)', 3],
    ['G2.5 (1 parent immigré)', 'Enfants d’un parent immigré (G2)', 2],
    ['G3', 'Petits-enfants d’immigrés (G3)', 1],
    ['Population majoritaire', 'Population majoritaire', 0]
  ] as const;
  const identification = generationsIde.map(([l, libelle, t]) => ({
    libelle,
    teinte: t,
    valeur: v(IDE, l, 'France seule')
  }));
  const discriParGen = (
    [
      ['G1', 'Immigrés (G1)', 4],
      ['G2', 'Enfants de deux parents immigrés (G2)', 3],
      ['G2.5', 'Enfants d’un parent immigré (G2)', 2],
      ['Population majoritaire', 'Population majoritaire', 0]
    ] as const
  ).map(([l, libelle, t]) => ({ libelle, teinte: t, valeur: v(DIS, l, DIS_COL) }));

  return {
    e1: {
      paliers: p,
      etendue: etendue(p),
      total41,
      conjoints,
      om,
      ip1910: pIp,
      sansAscendance,
      g3Un: e3Ensemble[0].valeur,
      g3Moins18: { un: g3Moins18('Un'), quatre: g3Moins18('Quatre') },
      ip1910_18_59,
      lignages
    },
    e2: { colonnes: COLS, lignes: e2 },
    e2origine: { colonnes: COLS7, lignes: e2origine },
    e3: { ensemble: e3Ensemble, origines: e3Origines, ip3a },
    e9: {
      segregation,
      chomage,
      precisionCho,
      discriminations,
      // Contradiction de la source (ch. 11) : valeurs du §35 et de la note de lecture de la figure 1.
      texte35: {
        g1: {
          hommes: v(T35, '§35, immigrés d’Afrique du Nord', 'Hommes'),
          femmes: v(T35, '§35, immigrés d’Afrique du Nord', 'Femmes')
        },
        lectureG1Hommes: v(T35, 'Note de lecture de la figure 1, immigrés du Maghreb', 'Hommes')
      }
    },
    e10: { identification, discriParGen, anomalieG1: ecartA100(cs, IDE, 'G1') },
    champs: CHAMPS
  };
}

export type DonneesGenerations = ReturnType<typeof donneesGenerations>;
