import { piscine, soldes } from '$lib/server/donnees';

export const load = () => {
  const p = piscine();
  const an = (a: number) => p.annees.find((x) => x.annee === a)!;
  const a25 = an(2025);
  const a22 = an(2022);
  const premiere = p.annees[0];
  const so = soldes();
  return {
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
