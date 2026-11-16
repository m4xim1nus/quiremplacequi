import { arrivees, MOTIFS } from '$lib/server/arrivees';
import { decomposer, pour10000 } from '$lib/comparaisons';

export const load = () => {
  const d = arrivees();
  const ans = d.annees;
  const premier = ans[0];
  const dernier = ans.at(-1)!;
  const pic = ans.reduce((a, b) => (b.total - b.brexit > a.total - a.brexit ? b : a));
  const hausse = decomposer(premier.motifs, dernier.motifs);
  const familiales = ans.map((a) => a.motifs.familial);

  // Asile : dernière année publiée à la fois par Eurostat et par le ministère.
  const anAsile = Math.min(dernier.annee, Math.max(...Object.keys(d.asile.premieres).map(Number)));
  const titresAsile = ans.find((a) => a.annee === anAsile)!;

  // Soldes migratoires des immigrés et des non-immigrés (années où les sorties sont estimées).
  const soldes = d.flux
    .filter((f) => f.sortiesImm !== null && f.sortiesNi !== null)
    .map((f) => ({
      annee: f.annee,
      champ: f.champ,
      // Soldes publiés par l'Insee (arrondis au millier), pas recalculés.
      immigres: f.soldeImm!,
      nonImmigres: f.soldeNi!,
      sortiesImm: f.sortiesImm!,
      entreesNi: f.entreesNi,
      sortiesNi: f.sortiesNi!
    }));
  const cumul = (k: 'immigres' | 'nonImmigres') => soldes.reduce((s, x) => s + x[k], 0);
  // Année où les sorties d'immigrés publiées sont les plus basses (fragilité des sorties, U2).
  const sortiesMin = soldes.reduce((a, b) => (b.sortiesImm < a.sortiesImm ? b : a));
  const sortiesAutres = soldes.filter((s) => s !== sortiesMin).map((s) => s.sortiesImm);
  const fluxOrigines = d.flux.find((f) => f.annee === d.anneeOrigines)!;

  return {
    ...d,
    motifs: MOTIFS,
    chiffres: {
      premier,
      dernier,
      pic,
      hausse,
      pour10k: pour10000(dernier.total, dernier.population),
      pour10kPremier: pour10000(premier.total, premier.population),
      familialMin: Math.min(...familiales),
      familialMax: Math.max(...familiales),
      anAsile,
      premieres: d.asile.premieres[anAsile],
      decisions: d.asile.decisions[anAsile],
      positives: d.asile.positives[anAsile],
      titresProtection: titresAsile.protection,
      titresAnOrigines: ans.find((a) => a.annee === d.anneeOrigines)!,
      fluxOrigines,
      soldes,
      soldesDebut: soldes[0].annee,
      soldesFin: soldes.at(-1)!.annee,
      cumulImmigres: cumul('immigres'),
      cumulNonImmigres: cumul('nonImmigres'),
      sortiesMin: { annee: sortiesMin.annee, valeur: sortiesMin.sortiesImm },
      sortiesAutresMin: Math.min(...sortiesAutres),
      sortiesAutresMax: Math.max(...sortiesAutres),
      niToujoursNegatif: soldes.every((s) => s.nonImmigres < 0)
    }
  };
};
