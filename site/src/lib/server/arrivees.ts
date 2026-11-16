// Données de la page « Les arrivées » (D1-D5), lues dans data/export/ au prérendu.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, incertitudes } from './donnees';
import { MOTIFS, type Motif } from '$lib/comparaisons';

export { MOTIFS };

const csv = (f: string) => csvParse(readFileSync(resolve(EXPORT, f), 'utf8'));
const num = (v: string | undefined) => (v === undefined || v === '' ? null : Number(v));

export interface AnneeTitres {
  annee: number;
  total: number;
  britanniques: number;
  /** Titres « accord de retrait » : Britanniques déjà installés avant le Brexit. */
  brexit: number;
  motifs: Record<Motif, number>;
  famille: { francais: number; membre: number; liens: number };
  /** Réfugiés et protection subsidiaire (sous-motifs du motif humanitaire). */
  protection: number;
  population: number;
}

export function arrivees() {
  const titres = csv('titres.csv');
  const totaux = csv('titres_totaux.csv');
  const bilan = csv('bilan.csv').filter((r) => r.onglet === 'FR');
  const pop = (a: number) => num(bilan.find((r) => num(r.annee) === a)?.population)!;
  const somme = (a: number, f: (r: (typeof titres)[number]) => boolean) =>
    titres.filter((r) => num(r.annee) === a && f(r)).reduce((s, r) => s + num(r.titres)!, 0);

  const annees: AnneeTitres[] = totaux.map((t) => {
    const a = num(t.annee)!;
    const motifs = Object.fromEntries(
      MOTIFS.map((m) => [
        m,
        somme(a, (r) => r.motif === m && r.sous_motif !== 'accord_retrait_brexit')
      ])
    ) as Record<Motif, number>;
    const sm = (s: string) => somme(a, (r) => r.sous_motif === s);
    return {
      annee: a,
      total: num(t.total)!,
      britanniques: num(t.britanniques)!,
      brexit: num(t.accord_retrait_brexit)!,
      motifs,
      famille: {
        francais: sm('famille_de_francais'),
        membre: sm('membre_de_famille'),
        liens: sm('liens_personnels_familiaux')
      },
      protection: sm('refugie_apatride') + sm('protection_subsidiaire'),
      population: pop(a)
    };
  });
  const regions = Object.fromEntries(
    Object.entries(totaux.at(-1)!)
      .filter(([k]) => k.startsWith('region_'))
      .map(([k, v]) => [k.slice(7), num(v)!])
  );

  // Flux Insee (IP 2107) : entrées et sorties des immigrés et des non-immigrés.
  const flux = csv('flux.csv').map((r) => ({
    annee: num(r.annee)!,
    statut: r.statut!,
    champ: r.champ!,
    entreesImm: num(r.entrees_imm)!,
    sortiesImm: num(r.sorties_imm),
    entreesNi: num(r.entrees_ni)!,
    sortiesNi: num(r.sorties_ni),
    soldeImm: num(r.solde_imm),
    soldeNi: num(r.solde_ni)
  }));
  const origines = Object.fromEntries(
    csv('entrees_origine.csv').map((r) => [r.origine!, num(r.entrees)!])
  );
  const anneeOrigines = num(csv('entrees_origine.csv')[0].annee)!;

  // Asile en France (Eurostat) : premières demandes, décisions de première instance.
  const eu = csv('eurostat.csv').filter((r) => r.geo === 'FR');
  const asileIndic = (i: string) =>
    Object.fromEntries(
      eu.filter((r) => r.indicateur === i).map((r) => [num(r.annee)!, num(r.valeur)!])
    ) as Record<number, number>;
  const asile = {
    premieres: asileIndic('premieres_demandes'),
    decisions: asileIndic('decisions'),
    positives: asileIndic('decisions_positives'),
    refugie: asileIndic('statut_refugie'),
    subsidiaire: asileIndic('protection_subsidiaire')
  };

  const u = incertitudes();
  return {
    annees,
    regions,
    flux,
    origines,
    anneeOrigines,
    asile,
    incertitudes: ['U11', 'U2', 'U7'].filter((c) => u[c]).map((code) => ({ code, ...u[code] }))
  };
}
