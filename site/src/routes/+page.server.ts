import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { csvParse } from 'd3-dsv';
import { EXPORT, piscine, soldes } from '$lib/server/donnees';

/** Échelle de l'accueil : part des immigrés aux recensements (série B1), plaques choisies par règle :
 * premier point affiché, sommet d'avant 1946, sommet de 1946 à 1989 (le premier atteint), dernier
 * point (niveau de l'eau). */
function echelle(debut: number) {
  const serie = csvParse(readFileSync(resolve(EXPORT, 'b1_stock.csv'), 'utf8'))
    .map((r) => ({
      annee: Number(r.annee),
      part: Number(r.part_immigres),
      statut: r.statut!,
      champ: r.champ!
    }))
    .filter((r) => r.annee >= debut && Number.isFinite(r.part))
    .sort((a, b) => a.annee - b.annee);
  const sommet = (de: number, a: number) =>
    serie.filter((r) => r.annee >= de && r.annee < a).reduce((m, r) => (r.part > m.part ? r : m));
  const dernier = serie[serie.length - 1];
  const reperes = [serie[0], sommet(debut, 1946), sommet(1946, 1990), dernier].map(
    ({ annee, part }) => ({ annee, part })
  );
  return {
    niveau: { annee: dernier.annee, part: dernier.part },
    provisoire: dernier.statut === 'provisoire',
    metropoleJusqua: Math.max(...serie.filter((r) => r.champ === 'metropole').map((r) => r.annee)),
    reperes
  };
}

export const load = () => {
  const p = piscine();
  const an = (a: number) => p.annees.find((x) => x.annee === a)!;
  const a25 = an(2025);
  const a22 = an(2022);
  const premiere = p.annees[0];
  const so = soldes();
  return {
    echelle: echelle(p.annees[0].annee),
    soldes: {
      dernier: so.dernier,
      ...so.annee(so.dernier),
      depuis: so.migratoireDevantDepuis
    },
    debut: premiere.annee,
    partDebut: premiere.part_immigres,
    part2025: a25.part_immigres,
    immigres2025: a25.immigres,
    naissances2022: a22.naissances!,
    part1931: an(1931).part_immigres,
    collecte2024: an(2023).ajust_imm!,
    entreesImm2022: a22.entrees_imm!
  };
};
