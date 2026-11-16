// Données de la page « Ailleurs » (C1-C5), lues dans data/export/ au prérendu.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, incertitudes } from './donnees';
import { pour10000, tranchesMedianes } from '$lib/comparaisons';

const csv = (f: string) => csvParse(readFileSync(resolve(EXPORT, f), 'utf8'));
const num = (v: string | undefined) => (v === undefined || v === '' ? null : Number(v));

/** Pays européens comparés (UE à 27 et AELE) ; le Royaume-Uni n'est plus suivi après 2019. */
const AGREGAT = 'EU27_2020';

export interface Pays {
  geo: string;
  pays: string;
}

export function ailleurs() {
  const eu = csv('eurostat.csv');
  // geo → indicateur → année → [valeur, drapeau]
  const t = new Map<string, Map<string, Map<number, [number, string]>>>();
  const noms = new Map<string, string>();
  for (const r of eu) {
    noms.set(r.geo!, r.pays!);
    if (!t.has(r.geo!)) t.set(r.geo!, new Map());
    const g = t.get(r.geo!)!;
    if (!g.has(r.indicateur!)) g.set(r.indicateur!, new Map());
    g.get(r.indicateur!)!.set(num(r.annee)!, [num(r.valeur)!, r.drapeau ?? '']);
  }
  const v = (geo: string, i: string, a: number) => t.get(geo)?.get(i)?.get(a)?.[0] ?? null;
  const drapeau = (geo: string, i: string, a: number) => t.get(geo)?.get(i)?.get(a)?.[1] ?? '';
  const pays = [...noms.keys()].filter((g) => g !== AGREGAT);

  // C1 : part des personnes nées à l'étranger, dernière année publiée pour la France.
  const anneesNaiss = [...t.get('FR')!.get('nes_etranger')!.keys()].sort((a, b) => a - b);
  const anNaiss = anneesNaiss.at(-1)!;
  const anNaissDebut = anneesNaiss[0] < 2015 ? 2015 : anneesNaiss[0];
  const part = (g: string, a: number) => {
    const f = v(g, 'nes_etranger', a);
    const tot = v(g, 'pop_naissance_total', a);
    return f === null || tot === null ? null : (100 * f) / tot;
  };
  const nesEtranger = pays
    .map((g) => ({
      geo: g,
      pays: noms.get(g)!,
      part: part(g, anNaiss),
      partDebut: part(g, anNaissDebut),
      provisoire: drapeau(g, 'nes_etranger', anNaiss).includes('p')
    }))
    .filter((x) => x.part !== null && x.partDebut !== null) as {
    geo: string;
    pays: string;
    part: number;
    partDebut: number;
    provisoire: boolean;
  }[];
  const ue = { part: part(AGREGAT, anNaiss), partDebut: part(AGREGAT, anNaissDebut) };

  // C2 : soldes naturel et migratoire (‰), séries longues pour quelques pays.
  const soldes = ['FR', 'DE', 'ES', 'IT'].map((g) => {
    const ans = [...(t.get(g)!.get('taux_naturel')?.keys() ?? [])].sort((a, b) => a - b);
    return {
      geo: g,
      pays: noms.get(g)!,
      points: ans
        .map((a) => ({
          annee: a,
          naturel: v(g, 'taux_naturel', a),
          migratoire: v(g, 'taux_migratoire', a),
          provisoire: drapeau(g, 'taux_migratoire', a).includes('p')
        }))
        .filter((p) => p.naturel !== null && p.migratoire !== null) as {
        annee: number;
        naturel: number;
        migratoire: number;
        provisoire: boolean;
      }[]
    };
  });

  // C4-C5 : asile, cumul des premières demandes et des décisions positives sur une période
  // commune ; seuls les pays qui publient chaque année de la période sont classés.
  const anneesAsile = [...t.get('FR')!.get('premieres_demandes')!.keys()].sort((a, b) => a - b);
  const anAsileFin = anneesAsile.at(-1)!;
  const anAsileDebut = anAsileFin - 10;
  const periode = Array.from({ length: anAsileFin - anAsileDebut + 1 }, (_, i) => anAsileDebut + i);
  const cumul = (g: string, i: string) => {
    const vals = periode.map((a) => v(g, i, a));
    return vals.some((x) => x === null) ? null : vals.reduce((s, x) => s! + x!, 0)!;
  };
  const popMoy = (g: string) => {
    const vals = periode.map((a) => v(g, 'population', a));
    return vals.some((x) => x === null) ? null : vals.reduce((s, x) => s! + x!, 0)! / vals.length;
  };
  const asile = pays
    .map((g) => {
      const d = cumul(g, 'premieres_demandes');
      const p = cumul(g, 'decisions_positives');
      const pop = popMoy(g);
      const pib = cumul(g, 'pib_meur');
      return d === null || p === null || pop === null
        ? null
        : {
            geo: g,
            pays: noms.get(g)!,
            demandes: d,
            positives: p,
            population: pop,
            pib,
            // Par an et pour 10 000 habitants (moyenne de la période).
            demandes10k: pour10000(d / periode.length, pop),
            positives10k: pour10000(p / periode.length, pop)
          };
    })
    .filter((x) => x !== null);
  const ueAsile = {
    demandes: cumul(AGREGAT, 'premieres_demandes')!,
    positives: cumul(AGREGAT, 'decisions_positives')!,
    population: popMoy(AGREGAT)!,
    pib: cumul(AGREGAT, 'pib_meur')!
  };
  // Série annuelle de la France (premières demandes, absolu et pour 10 000).
  const asileFrance = anneesAsile.map((a) => ({
    annee: a,
    premieres: v('FR', 'premieres_demandes', a)!,
    population: v('FR', 'population', a)!
  }));

  // C3 : entrées permanentes (OCDE) par catégorie, moyenne annuelle sur dix ans, pour
  // 10 000 habitants. Un pays est classé s'il publie, chaque année, le travail, la famille,
  // l'humanitaire et sa population ; une catégorie secondaire absente (famille accompagnante,
  // libre circulation, autres) compte pour zéro : elle n'existe pas dans ses statistiques.
  const oc = csv('ocde.csv');
  const PRINCIPALES = ['travail', 'famille', 'humanitaire'] as const;
  const CATS = [
    'travail',
    'famille',
    'famille_accompagnante',
    'humanitaire',
    'libre_circulation',
    'autres'
  ] as const;
  const ocParPays = new Map<string, { pays: string; m: Map<string, number> }>();
  for (const r of oc) {
    if (!ocParPays.has(r.pays_code!)) ocParPays.set(r.pays_code!, { pays: r.pays!, m: new Map() });
    ocParPays.get(r.pays_code!)!.m.set(`${r.indicateur}|${num(r.annee)}`, num(r.valeur)!);
  }
  const publie = (m: Map<string, number>, a: number) =>
    m.has(`population|${a}`) && PRINCIPALES.every((c) => m.has(`entrees_${c}|${a}`));
  const ocAnnees = [...new Set(oc.map((r) => num(r.annee)!))].sort((a, b) => a - b);
  // Dernière année publiée par au moins les trois quarts des pays.
  const ocFin = [...ocAnnees]
    .reverse()
    .find(
      (a) => [...ocParPays.values()].filter((p) => publie(p.m, a)).length >= 0.75 * ocParPays.size
    )!;
  const ocPeriode = Array.from({ length: 10 }, (_, i) => ocFin - 9 + i);
  const entrees = [...ocParPays.entries()]
    .map(([code, { pays: nom, m }]) => {
      if (!ocPeriode.every((a) => publie(m, a))) return null;
      const popM = ocPeriode.reduce((s, a) => s + m.get(`population|${a}`)!, 0) / 10;
      const cats = Object.fromEntries(
        CATS.map((c) => [
          c,
          pour10000(ocPeriode.reduce((s, a) => s + (m.get(`entrees_${c}|${a}`) ?? 0), 0) / 10, popM)
        ])
      ) as Record<(typeof CATS)[number], number>;
      return { code, pays: nom, cats, total: CATS.reduce((s, c) => s + cats[c], 0) };
    })
    .filter((x) => x !== null);

  // C7 : taux d'émigration (ONU) = émigrés / (population résidente + émigrés), pays d'au moins un
  // million d'habitants qui publient émigrés et PIB par habitant ; médianes par quintile de PIB.
  const onu = csv('onu_pays.csv')
    .map((r) => ({
      code: r.code!,
      pays: r.pays!,
      sousRegion: r.sous_region!,
      emigres: num(r.emigres),
      population: num(r.population)!,
      pib: num(r.pib_hab_usd),
      anneePib: num(r.annee_pib)
    }))
    .filter((r) => r.population >= 1e6 && r.emigres !== null && r.pib !== null)
    .map((r) => ({ ...r, taux: (100 * r.emigres!) / (r.population + r.emigres!) }));
  const anOnu = num(csv('onu_pays.csv')[0].annee)!;
  const quintiles = tranchesMedianes(
    onu,
    (p) => p.pib!,
    (p) => p.taux,
    5
  );
  const reg = Object.fromEntries(
    csv('onu_regions.csv').map((r) => [r.destination!, num(r.migrants)!])
  );

  // Part des immigrés selon l'Insee (définition française), même année si publiée.
  const stock = csv('b1_stock.csv');
  const insee = stock.find((r) => num(r.annee) === anNaiss) ?? stock.at(-1)!;

  const u = incertitudes();
  return {
    anNaiss,
    anNaissDebut,
    nesEtranger,
    ue,
    insee: { annee: num(insee.annee)!, part: num(insee.part_immigres)!, statut: insee.statut! },
    soldes,
    asile,
    ueAsile,
    asileFrance,
    periodeAsile: [anAsileDebut, anAsileFin] as [number, number],
    entrees,
    periodeEntrees: [ocPeriode[0], ocFin] as [number, number],
    categories: CATS,
    emigration: {
      annee: anOnu,
      pays: onu.map((p) => ({
        code: p.code,
        pays: p.pays,
        afriqueSub: p.sousRegion === 'Afrique subsaharienne',
        taux: p.taux,
        pib: p.pib!,
        population: p.population,
        emigres: p.emigres!
      })),
      quintiles,
      afrique: {
        emigres: reg['Monde'],
        population: reg['population résidente'],
        memeRegion: reg['Afrique subsaharienne'],
        nordOuest: reg["Afrique du Nord et Asie de l'Ouest"],
        europeAmerique: reg['Europe et Amérique du Nord'],
        france: reg['dont France']
      }
    },
    incertitudes: ['U12', 'U22', 'U23', 'U24']
      .filter((c) => u[c])
      .map((code) => ({ code, ...u[code] }))
  };
}
