import { piscine } from '$lib/server/donnees';

export const load = () => {
  const p = piscine();
  const an = (a: number) => p.annees.find((x) => x.annee === a)!;
  const a25 = an(2025);
  const a22 = an(2022);
  const premiere = p.annees[0];
  return {
    debut: premiere.annee,
    partDebut: premiere.part_immigres,
    part2025: a25.part_immigres,
    immigres2025: a25.immigres,
    naissances2022: a22.naissances!,
    entreesImm2022: a22.entrees_imm!
  };
};
