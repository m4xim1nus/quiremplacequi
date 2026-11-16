import { naissances, type AnneeNaissances } from '$lib/server/naissances';

// Régions de naissance de l'IP 1939 (figure 6), dans l'ordre de l'Insee.
const REGIONS: [string, string][] = [
  ['europe_du_sud', 'Italie, Espagne, Portugal'],
  ['autres_europe', 'Autres pays d’Europe'],
  ['maghreb', 'Algérie, Maroc, Tunisie'],
  ['autres_afrique', 'Autres pays d’Afrique'],
  ['turquie_moyen_orient', 'Turquie, Moyen-Orient'],
  ['autres_asie', 'Autres pays d’Asie'],
  ['amerique_oceanie', 'Amérique, Océanie']
];

export const load = () => {
  const d = naissances();
  const ans = d.annees;
  const dernier = ans.at(-1)!;
  const premier = ans[0];
  const pic = ans.reduce((a, b) => (b.ensemble > a.ensemble ? b : a));
  const parts = (a: AnneeNaissances) => ({
    auMoinsUn: (100 * (a.unParent + a.deuxParents)) / a.ensemble,
    mere: (100 * a.mereEtranger) / a.ensemble,
    deux: (100 * a.deuxParents) / a.ensemble
  });

  // ICF ajusté (IP 1939) : dernière année publiée.
  const fin = (g: string) => d.icf[g].at(-1)!;
  const anIcf = fin('ensemble').annee;
  const icf = {
    annee: anIcf,
    debut: d.icf.ensemble[0].annee,
    ensemble: fin('ensemble').icf,
    france: fin('nees_en_france').icf,
    etranger: fin('nees_a_l_etranger').icf,
    etrangerDebut: d.icf.nees_a_l_etranger[0].icf,
    franceDebut: d.icf.nees_en_france[0].icf
  };
  const contribution = icf.ensemble - icf.france;
  const naisIcf = ans.find((a) => a.annee === anIcf)!;
  const regions = REGIONS.map(([g, libelle]) => ({ libelle, icf: fin(g).icf })).sort(
    (a, b) => b.icf - a.icf
  );

  // ICF national et seuil de remplacement.
  const metro = d.nationale.filter((x) => x.champ === 'metropole');
  const france = d.nationale.filter((x) => x.champ === 'france');
  const frDer = france.at(-1)!;
  let sousSeuilDepuis: number | null = null;
  for (let i = metro.length - 1; i > 0; i--) {
    if (metro[i - 1].icf >= metro[i - 1].seuil) {
      sousSeuilDepuis = metro[i].annee;
      break;
    }
  }
  const genDer = d.generations.at(-1)!;
  // Indicateur conjoncturel de l'année des 30 ans de cette génération (métropole).
  const icfA30 = metro.find((x) => x.annee === genDer.generation + 30)!;
  const icfMax = metro.reduce((a, b) => (b.icf > a.icf ? b : a));

  // Descendance finale (TeO).
  const lien = (c: string) => d.df.find((x) => x.dimension === 'lien' && x.categorie === c)!.valeur;
  const gen = (g: string) =>
    d.df
      .filter((x) => x.dimension === 'generation' && x.groupe === g)
      .map((x) => ({ debut: Number(x.categorie.slice(0, 4)), valeur: x.valeur }))
      .sort((a, b) => a.debut - b.debut);

  // Naissances des immigrées autour de leur arrivée.
  const somme = (f: (x: (typeof d.arrivee)[number]) => number) =>
    d.arrivee.reduce((s, x) => s + f(x), 0);
  const calendrier = {
    avant: somme((x) => (x.duree < 0 ? x.enFrance + x.aLEtranger : 0)),
    etranger: somme((x) => x.aLEtranger),
    cinqAns: somme((x) => (x.duree >= 0 && x.duree <= 4 ? x.enFrance : 0)),
    annee1: d.arrivee.find((x) => x.duree === 1)!.enFrance
  };

  // ONU 2000, et ce que l'Insee a observé depuis.
  const sc = (code: string) => d.onu.scenarios.find((s) => s.code === code)!.valeurs;
  const entre = (de: number, a: number) =>
    d.bilan.filter((b) => b.annee >= de && b.annee <= a).map((b) => b.soldeMigratoire);
  const derBilan = d.bilan.at(-1)!;
  const soldesDepuis2000 = entre(2000, derBilan.annee);
  const soutien = (a: number) => d.rapportSoutien.find((x) => x.annee === a)!.rapport;
  const derSoutien = d.rapportSoutien.at(-1)!;
  const pop2050 = d.onu.scenarios.map((s) => s.valeurs.population_2050 * 1000);
  const popDer = derBilan.population;
  const derPop = derBilan.annee;

  return {
    ...d,
    regions,
    chiffres: {
      premier,
      dernier,
      pic,
      partsDernier: parts(dernier),
      partsPremier: parts(premier),
      partsIcf: parts(naisIcf),
      variation: {
        ensemble: dernier.ensemble - pic.ensemble,
        deuxNesFrance: dernier.deuxNesFrance - pic.deuxNesFrance,
        unParent: dernier.unParent - pic.unParent,
        deuxParents: dernier.deuxParents - pic.deuxParents
      },
      icf,
      contribution,
      contributionRel: (100 * contribution) / icf.france,
      textes: d.textes,
      frDer,
      seuilDer: frDer.seuil,
      seuilPremier: metro[0],
      sousSeuilDepuis,
      icfMax,
      genDer,
      icfA30,
      lien: {
        immigrees: lien('immigrees'),
        avant15: lien('arrivees_avant_15_ans'),
        apres15: lien('arrivees_15_ans_ou_plus'),
        descendantes: lien('descendantes'),
        deuxParents: lien('descendantes_deux_parents'),
        unParent: lien('descendantes_un_parent'),
        ni: lien('ni_immigrees_ni_descendantes'),
        ensemble: lien('ensemble')
      },
      genImmigrees: gen('immigrees'),
      genNonImmigrees: gen('non_immigrees'),
      calendrier,
      onu: {
        I: sc('I'),
        III: sc('III'),
        IV: sc('IV'),
        V: sc('V'),
        soldeMoyen: soldesDepuis2000.reduce((s, x) => s + x, 0) / soldesDepuis2000.length,
        soldeDe: 2000,
        soldeA: derBilan.annee,
        cumul1995_2020: entre(1995, 2020).reduce((s, x) => s + x, 0),
        soutien1995: soutien(1995),
        soutienDer: derSoutien.rapport,
        anSoutien: derSoutien.annee,
        popDer,
        anPop: derPop,
        depasseSaufV: d.onu.scenarios
          .filter((s) => s.code !== 'V')
          .every((s) => popDer > s.valeurs.population_2050 * 1000),
        pop2050Max: Math.max(...pop2050)
      }
    }
  };
};
