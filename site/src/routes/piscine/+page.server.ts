import { incertitudes, piscine } from '$lib/server/donnees';

const CODES = ['U17', 'U18', 'U1', 'U2', 'U3', 'U5', 'U6'];

export const load = () => {
  const p = piscine();
  const an = (a: number) => p.annees.find((x) => x.annee === a)!;
  const u = incertitudes();
  const a22 = an(2022);
  return {
    piscine: p,
    chiffres: {
      naissances2022: a22.naissances!,
      entreesImm2022: a22.entrees_imm!,
      deces2022: a22.deces!,
      population2022: a22.population,
      immigres1968: an(1968).immigres,
      part1968: an(1968).part_immigres,
      immigres2025: an(2025).immigres,
      part2025: an(2025).part_immigres,
      renouvellement2022: a22.naissances! / a22.population
    },
    incertitudes: CODES.map((code) => ({ code, ...u[code] }))
  };
};
