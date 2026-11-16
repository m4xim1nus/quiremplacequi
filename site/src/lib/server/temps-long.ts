// Données de la page « Le temps long » (B1, B2, B3, B5), lues dans data/export/ au prérendu.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, incertitudes, piscine, teo2 } from './donnees';
import { vagues, vitesse, type PointStock } from '$lib/temps-long';

const csv = (f: string) => csvParse(readFileSync(resolve(EXPORT, f), 'utf8'));
const num = (v: string | undefined) => (v === undefined || v === '' ? null : Number(v));

/** Pays et groupes détaillés suivis de 1968 à 2021 (les agrégats sont exclus). */
const PAYS = [
  'Espagne, Italie',
  'Portugal',
  'Algérie',
  'Maroc, Tunisie',
  'Turquie',
  'Asie du Sud-Est',
  'Chine',
  'Afrique sahélienne',
  'Afrique guinéenne ou centrale'
];

const ORIGINES = [
  'France',
  'Espagne, Italie, Portugal',
  "Autres pays de l'UE27",
  "Autres pays d'Europe",
  'Maghreb',
  "Autres pays d'Afrique",
  'Asie',
  'Autres pays du monde'
];

export function tempsLong() {
  const serie: PointStock[] = csv('b1_stock.csv').map((r) => ({
    annee: num(r.annee)!,
    immigres: num(r.immigres)!,
    part: num(r.part_immigres)!,
    population: num(r.population)!,
    champ: r.champ!,
    statut: r.statut!,
    rupture: r.rupture === 'true'
  }));

  const nat = vagues(
    csv('b2_nationalites.csv').map((r) => ({
      annee: num(r.annee)!,
      nationalite: r.nationalite!,
      groupe: r.groupe!,
      part_pct: num(r.part_pct)!
    }))
  );

  const paysBrut = csv('b2_pays.csv');
  const pays = PAYS.map((p) => ({
    pays: p,
    points: paysBrut
      .filter((r) => r.pays === p && num(r.immigres) !== null)
      .map((r) => ({ annee: num(r.annee)!, immigres: num(r.immigres)!, champ: r.champ! }))
      .sort((a, b) => a.annee - b.annee)
  }));

  const ip = csv('ip1910.csv');
  const cellule = (figure: string, ligne: string, colonne: string, bloc?: string) => {
    const r = ip.find(
      (x) =>
        x.figure === figure &&
        x.ligne === ligne &&
        x.colonne === colonne &&
        (bloc === undefined || x.bloc === bloc)
    );
    return r ? Number(r.valeur) : null;
  };
  const champIp = (figure: string) => ip.find((x) => x.figure === figure)?.champ ?? '';

  // Figure 3a : origines et nombre de grands-parents immigrés des G3.
  const B18 = 'Descendants G3 de moins de 18 ans';
  const B59 = 'Descendants G3 de 18 ans à 59 ans';
  const PART_GP = 'Part des G3 ayant au moins un grand-parent originaire du pays';
  const NB = ['Un', 'Deux', 'Trois', 'Quatre'];
  const g3Origines = ORIGINES.map((o) => ({
    origine: o,
    moins18: cellule('Figure 3a', o, PART_GP, B18),
    de18a59: cellule('Figure 3a', o, PART_GP, B59)
  }));
  const ensembleG3 = (bloc: string) =>
    ip.find((x) => x.figure === 'Figure 3a' && x.bloc === bloc && x.ligne.startsWith('Ensemble'))
      ?.ligne ?? '';
  const g3Nombre = [...ORIGINES.filter((o) => o !== 'France'), ensembleG3(B59)]
    .map((o) => ({
      origine: o,
      parts: NB.map((n) => cellule('Figure 3a', o, `Nombre de grands-parents immigrés / ${n}`, B59))
    }))
    // Origines non publiées pour les 18-59 ans (effectifs trop faibles) : écartées.
    .filter((o) => o.parts.every((v) => v !== null))
    .map((o) => ({ ...o, parts: o.parts as number[] }));

  // Figure 3b : origines des parents des G2, un ou deux parents immigrés.
  const PART_P = ip.find(
    (x) => x.figure === 'Figure 3b' && x.colonne.startsWith('Part des G2')
  )?.colonne;
  const g2 = [...ORIGINES.filter((o) => o !== 'France'), 'Ensemble des G2'].map((o) => ({
    origine: o,
    part: PART_P ? cellule('Figure 3b', o, PART_P) : null,
    un: cellule('Figure 3b', o, 'Nombre de parents immigrés : / Un') ?? 0,
    deux: cellule('Figure 3b', o, 'Nombre de parents immigrés : / Deux') ?? 0
  }));
  const g2ParentFrance = PART_P ? cellule('Figure 3b', 'France', PART_P) : null;

  // Figure 2c : origine des G3 par classe d'âge (part de la classe d'âge).
  const CLASSES = [
    '0-4',
    '5-9',
    '10-17',
    '18-24',
    '25-29',
    '30-34',
    '35-39',
    '40-44',
    '45-49',
    '50-54',
    '55-59'
  ];
  const g3Ages = ['Espagne, Italie, Portugal', 'Maghreb', "Autres pays d'Afrique"].map((o) => ({
    origine: o,
    points: CLASSES.map((c, i) => ({ i, classe: c, part: cellule('Figure 2c', c, o) })).filter(
      (p) => p.part !== null
    ) as { i: number; classe: string; part: number }[]
  }));

  // Décennie récente, brute et corrigée de l'effet de la nouvelle collecte de 2024 (U5), porté par
  // l'ajustement des immigrés de l'année 2023 dans la piscine (saisie référencée du pipeline).
  const v2015 = vitesse(serie, 2015, 2025);
  const collecte = piscine().annees.find((a) => a.annee === 2023)?.ajust_imm ?? 0;
  const s2025 = serie.find((p) => p.annee === 2025)!;
  const partCorrigee = (100 * (s2025.immigres - collecte)) / s2025.population;
  const v2015Corrigee = {
    ...v2015,
    effectif: v2015.effectif - collecte,
    effectifParAn: Math.round((v2015.effectif - collecte) / 10),
    partFin: Math.round(partCorrigee * 10) / 10,
    points: Math.round((partCorrigee - v2015.partDebut) * 10) / 10
  };

  // Figure 2c : part de chaque origine chez les 0-17 et les 18-59 ans.
  const g3Synthese = ['Espagne, Italie, Portugal', 'Maghreb'].map((o) => ({
    origine: o,
    moins18: cellule('Figure 2c', '0-17', o),
    de18a59: cellule('Figure 2c', '18-59', o)
  }));

  // Ensemble des immigrés en 2021 : série par pays (provisoire) contre série B1 (réajustée).
  const ens2021 = paysBrut.find((r) => r.pays === 'Ensemble' && r.annee === '2021');

  const u = incertitudes();
  return {
    serie,
    vitesses: {
      v1920: vitesse(serie, 1921, 1931),
      v2010: vitesse(serie, 2010, 2020),
      v2015,
      v2015Corrigee,
      collecte,
      // Entrée de Mayotte dans le champ au 1er janvier 2014 (U6) : ajustement de la piscine en 2013.
      mayotte: piscine().annees.find((a) => a.annee === 2013)?.ajust_imm ?? 0
    },
    g3Synthese,
    ensemble2021: {
      pays: ens2021 ? num(ens2021.immigres) : null,
      b1: serie.find((p) => p.annee === 2021)?.immigres ?? null
    },
    teo2UnGrandParent: teo2('ch08_tableau4.yaml', '1', 'Ensemble des G3 (enquête principale)'),
    vagues: nat,
    pays,
    g3Origines,
    g3Nombre,
    g2,
    g2ParentFrance,
    g3Ages,
    classes: CLASSES,
    champs: {
      fig3a: champIp('Figure 3a'),
      fig3b: champIp('Figure 3b'),
      fig2c: champIp('Figure 2c'),
      encadre: champIp('Encadré Figure a')
    },
    incertitudes: ['U9', 'U5', 'U6', 'U27', 'U10', 'U8'].map((code) => ({ code, ...u[code] }))
  };
}
