import { ailleurs } from '$lib/server/ailleurs';
import { classement } from '$lib/comparaisons';

export const load = () => {
  const d = ailleurs();
  const fr = d.nesEtranger.find((x) => x.geo === 'FR')!;
  const c1 = classement(d.nesEtranger.map((x) => ({ libelle: x.pays, valeur: x.part })));
  const progression = d.nesEtranger.map((x) => ({ libelle: x.pays, valeur: x.part - x.partDebut }));
  const c2 = classement(progression);

  const a = d.asile.find((x) => x.geo === 'FR')!;
  const asileRel = classement(d.asile.map((x) => ({ libelle: x.pays, valeur: x.demandes10k })));
  const asileAbs = classement(d.asile.map((x) => ({ libelle: x.pays, valeur: x.demandes })));
  const posRel = classement(d.asile.map((x) => ({ libelle: x.pays, valeur: x.positives10k })));
  // « Prendre sa part » : part de la France dans l'UE à 27 (demandes, population, PIB).
  const part = {
    demandes: (100 * a.demandes) / d.ueAsile.demandes,
    positives: (100 * a.positives) / d.ueAsile.positives,
    population: (100 * a.population) / d.ueAsile.population,
    pib: a.pib === null ? null : (100 * a.pib) / d.ueAsile.pib
  };

  const e = d.entrees.find((x) => x.code === 'FRA');
  const c3 = classement(d.entrees.map((x) => ({ libelle: x.pays, valeur: x.total })));

  return {
    ...d,
    chiffres: {
      fr,
      rangPart: c1.rang('France'),
      nPart: c1.n,
      rangProgression: c2.rang('France'),
      progressionFr: fr.part - fr.partDebut,
      progressionUe:
        d.ue.part !== null && d.ue.partDebut !== null ? d.ue.part - d.ue.partDebut : null,
      asileFr: a,
      rangAsileRel: asileRel.rang('France'),
      rangAsileAbs: asileAbs.rang('France'),
      rangPositivesRel: posRel.rang('France'),
      nAsile: asileRel.n,
      premierAsileRel: asileRel.tri[0],
      part,
      entreesFr: e ?? null,
      rangEntrees: e ? c3.rang('France') : null,
      nEntrees: c3.n
    }
  };
};
