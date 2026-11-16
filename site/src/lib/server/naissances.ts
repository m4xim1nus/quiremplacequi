// Données de la page « Les naissances » (F3, E7, F4), lues dans data/export/ au prérendu.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, incertitudes } from './donnees';

const csv = (f: string) => csvParse(readFileSync(resolve(EXPORT, f), 'utf8'));
const json = <T>(f: string): T => JSON.parse(readFileSync(resolve(EXPORT, f), 'utf8')) as T;
const num = (v: string | undefined) => (v === undefined || v === '' ? null : Number(v));

export interface AnneeNaissances {
  annee: number;
  provisoire: boolean;
  ensemble: number;
  deuxNesFrance: number;
  /** Un parent né en France, l'autre à l'étranger. */
  unParent: number;
  deuxParents: number;
  /** Mère née à l'étranger, quel que soit le second parent. */
  mereEtranger: number;
}

export interface ScenarioOnu {
  code: string;
  libelle: string;
  valeurs: Record<string, number>;
}

export function naissances() {
  // 1. Naissances selon le pays de naissance des parents (état civil).
  const np = csv('naissances_parents.csv');
  const det = csv('naissances_detail.csv');
  const v = (rows: typeof np, a: number, c: string) =>
    num(rows.find((r) => num(r.annee) === a && r.categorie === c)?.naissances)!;
  const annees: AnneeNaissances[] = [...new Set(np.map((r) => num(r.annee)!))]
    .sort((a, b) => a - b)
    .map((a) => {
      const deuxParents = v(np, a, 'deux_parents_nes_a_l_etranger');
      return {
        annee: a,
        provisoire: np.find((r) => num(r.annee) === a)!.statut === 'provisoire',
        ensemble: v(np, a, 'ensemble'),
        deuxNesFrance: v(np, a, 'deux_parents_nes_en_france'),
        unParent: v(np, a, 'un_parent_ne_a_l_etranger'),
        deuxParents,
        mereEtranger:
          v(det, a, 'mere_ue_second_france') + v(det, a, 'mere_hors_ue_second_france') + deuxParents
      };
    });

  // 2. ICF ajusté selon le pays de naissance (IP 1939, 2006-2021).
  const icfRows = csv('fecondite_icf.csv');
  const groupes = [...new Set(icfRows.map((r) => r.groupe!))];
  const icf = Object.fromEntries(
    groupes.map((g) => [
      g,
      icfRows
        .filter((r) => r.groupe === g)
        .map((r) => ({ annee: num(r.annee)!, icf: num(r.icf)! }))
        .sort((a, b) => a.annee - b.annee)
    ])
  ) as Record<string, { annee: number; icf: number }[]>;
  const textes = Object.fromEntries(
    csv('fecondite_textes.csv').map((r) => [r.cle!, num(r.valeur)!])
  );

  // 3. ICF national et seuil de remplacement (ICF / taux net de reproduction × 100).
  const nat = csv('fecondite_nationale.csv').map((r) => ({
    annee: num(r.annee)!,
    champ: r.champ as 'metropole' | 'france',
    provisoire: r.statut === 'provisoire',
    icf: num(r.icf)!,
    trn: num(r.taux_reproduction_net)!,
    seuil: (100 * num(r.icf)!) / num(r.taux_reproduction_net)!
  }));
  const generations = csv('descendance_generations.csv').map((r) => ({
    generation: num(r.generation)!,
    descendance: num(r.descendance)!
  }));

  // 4. Descendance finale (TeO).
  const df = csv('fecondite_descendance.csv').map((r) => ({
    dimension: r.dimension!,
    categorie: r.categorie!,
    groupe: r.groupe!,
    valeur: num(r.valeur)!,
    enquete: r.enquete!
  }));

  // 5. Naissances des immigrées autour de leur arrivée (TeO2).
  const arrivee = csv('fecondite_arrivee.csv').map((r) => ({
    duree: num(r.duree)!,
    enFrance: num(r.en_france)!,
    aLEtranger: num(r.a_l_etranger)!
  }));

  // 6. ONU 2000 : scénarios pour la France, et ce qui a été observé depuis (Insee).
  const o2 = csv('onu2000.csv');
  const onuMeta = json<{
    source: { document: string; cote: string; date: string };
    scenarios: Record<string, string>;
    citations: { cle: string; page: number; texte: string }[];
  }>('onu2000.json');
  const scenarios: ScenarioOnu[] = Object.entries(onuMeta.scenarios).map(([code, libelle]) => ({
    code,
    libelle,
    valeurs: Object.fromEntries(
      o2.filter((r) => r.scenario === code).map((r) => [r.indicateur!, num(r.valeur)!])
    )
  }));
  const bilan = csv('bilan.csv')
    .filter((r) => r.onglet === 'FR' && r.solde_migratoire !== '')
    .map((r) => ({
      annee: num(r.annee)!,
      soldeMigratoire: num(r.solde_migratoire)!,
      population: num(r.population)!,
      provisoire: r.statut === 'provisoire'
    }));
  // Rapport de soutien potentiel (15-64 ans pour une personne de 65 ans ou plus), au 1er janvier.
  const ages = csv('ages.csv');
  const soutien = new Map<number, { actifs: number; ages65: number }>();
  for (const r of ages) {
    const a = num(r.annee)!;
    const age = num(r.age)!;
    if (a < 1990 || age < 15) continue;
    const s = soutien.get(a) ?? { actifs: 0, ages65: 0 };
    if (age < 65) s.actifs += num(r.population)!;
    else s.ages65 += num(r.population)!;
    soutien.set(a, s);
  }
  const rapportSoutien = [...soutien.entries()]
    .map(([annee, s]) => ({ annee, rapport: s.actifs / s.ages65 }))
    .sort((a, b) => a.annee - b.annee);

  const u = incertitudes();
  return {
    annees,
    icf,
    textes,
    nationale: nat,
    generations,
    df,
    arrivee,
    onu: { ...onuMeta, scenarios },
    bilan,
    rapportSoutien,
    incertitudes: ['U25', 'U26', 'U6'].filter((c) => u[c]).map((code) => ({ code, ...u[code] }))
  };
}
