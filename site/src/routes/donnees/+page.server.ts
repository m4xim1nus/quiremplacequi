import { readdirSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { EXPORT, meta } from '$lib/server/donnees';

/** Description de chaque fichier publié (data/export/). */
const FICHIERS: Record<string, string> = {
  'piscine.csv':
    'La piscine : stocks au 1er janvier et flux de chaque année, par génération, 1921-2025',
  'piscine.json': 'La piscine, avec ses paramètres, son calage et ses événements',
  'cohortes.csv':
    'Modèle de cohortes : G1, G2 (deux parents, un parent), G3 par tranche d’âge, 1911-2025',
  'cohortes_calage.csv':
    'Écarts du modèle de cohortes à ses cibles (IP 1910) et à ses témoins (descendants 2025, décès Insee)',
  'b1_stock.csv': 'Immigrés, étrangers, Français par acquisition, 1911-2025',
  'b2_nationalites.csv':
    'Part des étrangers par nationalité dans la population, 1901-2020 (métropole)',
  'b2_pays.csv': 'Immigrés par pays ou groupe de pays de naissance, 1968-2021',
  'bilan.csv': 'Bilan démographique : population, naissances, décès, soldes, 1901-2026',
  'flux.csv': 'Entrées, sorties et décès des immigrés et des non-immigrés, 2006-2024',
  'naissances_parents.csv': 'Naissances selon le pays de naissance des parents, 1998-2025',
  'naissances_detail.csv':
    'Naissances selon le pays de naissance de la mère et du second parent (UE, hors UE), 1998-2025',
  'fecondite_icf.csv':
    'Indicateur conjoncturel de fécondité ajusté, selon le pays de naissance des femmes, 2006-2021 (Insee Première 1939)',
  'fecondite_descendance.csv':
    'Descendance finale des femmes selon le lien à la migration, la génération, le pays de naissance et le diplôme (TeO1, TeO2)',
  'fecondite_arrivee.csv':
    'Naissances des immigrées selon les années écoulées depuis leur arrivée, en France ou à l’étranger (TeO2)',
  'fecondite_nationale.csv':
    'Indicateur conjoncturel de fécondité, âge moyen à l’accouchement, taux de reproduction, 1901-2025',
  'descendance_generations.csv':
    'Descendance finale des générations de femmes, France métropolitaine, 1885-1975',
  'fecondite_textes.csv':
    'Chiffres du texte de l’Insee Première 1939 (ajustement de l’indicateur), une référence par valeur',
  'onu2000.csv':
    'ONU, « Replacement Migration » (2000) : les cinq scénarios pour la France, une référence par ligne',
  'onu2000.json':
    'ONU, « Replacement Migration » (2000) : scénarios et citations du résumé en français',
  'ip1910.csv': 'Insee Première 1910 : toutes les figures, en format long',
  'teo2.csv': 'TeO2 : cellules ressaisies des tableaux et figures (une référence par cellule)',
  'incertitudes.json': 'Registre des incertitudes (codes U1…)',
  'titres.csv':
    'Premiers titres de séjour par motif et sous-motif, 2011-2024 (ministère de l’Intérieur, DSED)',
  'titres_totaux.csv':
    'Premiers titres de séjour : totaux, Britanniques, régions de nationalité, contrôle du raccord des sources DSED',
  'entrees_origine.csv':
    'Entrées d’immigrés et de non-immigrés par région de naissance (Insee, IP 2107)',
  'eurostat.csv':
    'Eurostat, pays européens : population, soldes naturel et migratoire (‰), pays de naissance, asile, PIB',
  'ocde.csv': 'OCDE : entrées à titre permanent par catégorie et population, 2014-2025',
  'onu_pays.csv':
    'ONU : émigrés, immigrés, population et PIB par habitant par pays, 2024 (noms M49 en français)',
  'onu_regions.csv': 'ONU : où vivent les émigrés d’Afrique subsaharienne, par grande région, 2024',
  'contradicteurs.json': 'Hypothèses citées des publications discutées (note de l’OID, 2026)',
  'meta.json': 'Date de calcul et sources (URL, date de téléchargement, empreinte sha256)'
};

export const load = () => {
  const m = meta() as {
    genere_le: string;
    sources: Record<
      string,
      { titre: string; page: string; telecharge_le: string; licence?: string; depot?: string }
    >;
  };
  const fichiers = readdirSync(EXPORT)
    .sort()
    .map((nom) => ({
      nom,
      description: FICHIERS[nom] ?? '',
      octets: statSync(resolve(EXPORT, nom)).size
    }));
  // Les vingt fichiers annuels de la DSED (motifs et nationalités, 2015-2024) tiennent en une ligne.
  const toutes = Object.entries(m.sources).map(([cle, s]) => ({ cle, ...s }));
  const annuels = toutes.filter((s) => /^titres_(nat_)?20\d\d$/.test(s.cle));
  const ans = annuels.map((s) => Number(s.cle.slice(-4)));
  const sources = toutes.filter((s) => !annuels.includes(s));
  if (annuels.length)
    sources.push({
      ...annuels[0],
      cle: 'titres_annuels',
      titre: `DSED : premiers titres de séjour par motif, sous-motif et nationalité, fichiers annuels définitifs ${Math.min(...ans)}-${Math.max(...ans)}`
    });
  return {
    fichiers,
    sources,
    genereLe: m.genere_le
  };
};
