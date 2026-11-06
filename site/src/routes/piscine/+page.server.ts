import { descendants2025, incertitudes, nesAvant, piscine, teo2 } from '$lib/server/donnees';

const CODES = ['U17', 'U19', 'U18', 'U1', 'U2', 'U3', 'U5', 'U6'];

export const load = () => {
  const p = piscine();
  p.nes_avant = nesAvant(p.annees[0].annee);
  const an = (a: number) => p.annees.find((x) => x.annee === a)!;
  const u = incertitudes();
  const a22 = an(2022);
  const a25 = an(2025);
  return {
    piscine: p,
    chiffres: {
      naissances2022: a22.naissances!,
      entreesImm2022: a22.entrees_imm!,
      deces2022: a22.deces!,
      population2022: a22.population,
      immigres1968: an(1968).immigres,
      part1968: an(1968).part_immigres,
      immigres2025: a25.immigres,
      part2025: a25.part_immigres,
      renouvellement2022: a22.naissances! / a22.population,
      nais2022: {
        g2a: a22.naissances_g2a!,
        g2b: a22.naissances_g2b!,
        g3: a22.naissances_g3!,
        autres: a22.naissances_autres!
      },
      g2a2025: a25.g2a!,
      g2b2025: a25.g2b!,
      g32025: a25.g3!,
      pop2025: a25.population,
      descendants2025: descendants2025().effectif,
      descendantsUnParent: descendants2025().part_un_parent,
      g3UnGrandParent: teo2('ch08_tableau4.yaml', '1', 'Ensemble des G3 (enquête principale)')
    },
    incertitudes: CODES.filter((c) => u[c]).map((code) => ({ code, ...u[code] }))
  };
};
