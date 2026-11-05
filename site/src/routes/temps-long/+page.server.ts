import { tempsLong } from '$lib/server/temps-long';
import { sommet } from '$lib/temps-long';

export const load = () => {
  const d = tempsLong();
  const s = d.serie;
  const an = (a: number) => s.find((p) => p.annee === a)!;
  const avant1946 = s.filter((p) => p.annee < 1946);
  const pic1 = sommet(avant1946, (p) => p.part);
  const creux = s
    .filter((p) => p.annee >= 1931 && p.annee <= 1962)
    .reduce((a, b) => (b.part < a.part ? b : a));
  const plateau = s.filter((p) => p.annee >= 1975 && p.annee <= 1999).map((p) => p.part);
  const premier = s[0];
  const dernier = s[s.length - 1];
  const g3 = (o: string) => d.g3Origines.find((x) => x.origine === o)!;
  const nb = (o: string) => d.g3Nombre.find((x) => x.origine === o)!;
  const g2 = (o: string) => d.g2.find((x) => x.origine === o)!;
  const pays = (p: string) => d.pays.find((x) => x.pays === p)!.points;
  return {
    ...d,
    chiffres: {
      premier,
      pic1,
      creux,
      plateauMin: Math.min(...plateau),
      plateauMax: Math.max(...plateau),
      a1968: an(1968),
      dernier,
      espIt: { debut: pays('Espagne, Italie')[0], fin: pays('Espagne, Italie').at(-1)! },
      portugal: sommet(pays('Portugal'), (p) => p.immigres),
      algerie: { debut: pays('Algérie')[0], fin: pays('Algérie').at(-1)! },
      g3SudFrance: g3('France').de18a59,
      g3Sud18a59: g3('Espagne, Italie, Portugal').de18a59,
      g3SudMoins18: g3('Espagne, Italie, Portugal').moins18,
      g3MaghrebMoins18: g3('Maghreb').moins18,
      g3Maghreb18a59: g3('Maghreb').de18a59,
      g3SudUn: nb('Espagne, Italie, Portugal').parts[0],
      g3MaghrebQuatre: nb('Maghreb').parts[3],
      g3SudQuatre: nb('Espagne, Italie, Portugal').parts[3],
      g2SudUn: g2('Espagne, Italie, Portugal').un,
      g2MaghrebUn: g2('Maghreb').un,
      g2EnsembleUn: g2('Ensemble des G2').un
    }
  };
};
