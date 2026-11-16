<script lang="ts">
  import Piscine from '$lib/components/Piscine.svelte';
  import Detail from '$lib/components/Detail.svelte';
  import { entier, milliers, pct } from '$lib/format';
  import { STATUTS, type AnneePiscine } from '$lib/piscine';

  let { data } = $props();
  const c = $derived(data.chiffres);
  const r = $derived(data.piscine.ratio_deces);
  const virgule = (x: number, n = 2) => x.toFixed(n).replace('.', ',');
  /** Solde migratoire des immigrés de l'année : publié (entrées − sorties) ou reconstruit (net). */
  const soldeImm = (a: AnneePiscine) => {
    const v =
      a.statut_flux === 'reconstruit'
        ? a.net_imm
        : a.entrees_imm != null && a.sorties_imm != null
          ? a.entrees_imm - a.sorties_imm
          : null;
    return v == null ? '—' : (v < 0 ? '−' : '+') + entier(Math.abs(v));
  };
</script>

<svelte:head>
  <title>La piscine · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Toute la population résidant en France vue comme une eau qui se renouvelle : naissances, décès, arrivées, départs, de 1921 à 2025."
  />
</svelte:head>

<article class="page">
  <header class="colonne">
    <h1>La piscine</h1>
    <p class="chapeau">
      Toute la population résidant en France, vue comme une eau qui se renouvelle sans cesse : deux
      robinets en haut (les naissances, les arrivées), deux bondes en bas (les décès, les départs).
    </p>
    <p class="mode-emploi">
      <strong>Comment lire.</strong> Une colonne par génération, de largeur proportionnelle à son effectif
      ; l’épaisseur des rubans suit le débit de l’année. « Mélangée » remet tout le monde dans la même
      eau.
    </p>
  </header>

  <Piscine donnees={data.piscine} />

  <div class="colonne">
    <Detail titre="Les chiffres, année par année">
      <p>
        Ce que dessine la piscine, en tableau. Avant 2006, seul le solde net des immigrés est connu
        ; en 2023 et 2024, les sorties ne sont pas encore publiées ; pour 2025, la piscine ne montre
        que la population au 1er janvier. Fichier complet :
        <a href="/donnees/piscine.csv">piscine.csv</a>.
      </p>
      <div class="defile">
        <table class="annees">
          <caption class="visually-hidden"
            >La population et ses flux, de {data.piscine.annees[0].annee} à {data.piscine.annees[
              data.piscine.annees.length - 1
            ].annee}</caption
          >
          <thead>
            <tr>
              <th scope="col">Année</th>
              <th scope="col">Population</th>
              <th scope="col">Immigrés</th>
              <th scope="col">Part</th>
              <th scope="col">Naissances</th>
              <th scope="col">Décès</th>
              <th scope="col">Solde des immigrés</th>
              <th scope="col">Régime</th>
            </tr>
          </thead>
          <tbody>
            {#each data.piscine.annees as a (a.annee)}
              <tr>
                <th scope="row">{a.annee}</th>
                <td>{entier(a.population)}</td>
                <td>{entier(a.immigres)}</td>
                <td>{pct(a.part_immigres)}</td>
                <td>{a.naissances == null ? '—' : entier(a.naissances)}</td>
                <td>{a.deces == null ? '—' : entier(a.deces)}</td>
                <td>{soldeImm(a)}</td>
                <td class="regime"
                  >{a.statut_flux ? STATUTS[a.statut_flux].libelle.toLowerCase() : ''}</td
                >
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </Detail>
  </div>

  <section class="colonne">
    <h2>Ce qu’il faut regarder</h2>
    <ol class="points">
      <li>
        <strong>Le robinet des naissances débite le plus.</strong> En 2022, {milliers(
          c.naissances2022
        )} naissances contre {milliers(c.entreesImm2022)} arrivées d’immigrés. Mais elles dépassent à
        peine les décès : depuis {c.soldesDepuis}, c’est le solde migratoire qui fait l’essentiel de
        la croissance (+{milliers(c.soldes2022.migratoire)} en 2022, contre +{milliers(
          c.soldes2022.naturel
        )} pour le solde naturel). En un siècle environ, toute l’eau est remplacée, avec ou sans immigration.
      </li>
      <li>
        <strong>Les immigrés n’ont pas de robinet « naissances ».</strong> Leurs enfants, nés en
        France, ne sont pas immigrés : ils entrent dans une autre colonne. Le stock d’immigrés ne
        grossit que par les arrivées : {pct(c.part1968)} de la population en 1968 (métropole), {pct(
          c.part2025
        )} en 2025 (France, provisoire, après une amélioration de la collecte du recensement en 2024).
        Ces arrivées sont celles que compte l’Insee, pas les titres de séjour du ministère de l’Intérieur
        : <a href="/arrivees#deux-mesures">pourquoi les deux chiffres diffèrent</a>.
      </li>
      <li>
        <strong>De qui naissent les enfants ?</strong> En 2022, selon l’estimation du site, environ {milliers(
          c.nais2022.g2a
        )}
        enfants sur {milliers(c.naissances2022)} avaient deux parents immigrés, et {milliers(
          c.nais2022.g2b
        )}
        un seul.
      </li>
      <li>
        <strong>Pas deux blocs, des colonnes qui se recouvrent.</strong>
        {c.descendantsUnParent} % des enfants d’immigrés n’ont qu’un parent immigré (Insee, 2025 ; le
        modèle de la piscine, qui suit la convention de l’enquête de 2019-2020, en compte moins : U21),
        et
        {c.g3UnGrandParent} % des petits-enfants d’immigrés de 18 à 59 ans n’ont qu’un seul grand-parent
        immigré (TeO2).
      </li>
    </ol>

    <Detail>
      <p>
        Chaque année, les naissances renouvellent à elles seules {pct(100 * c.renouvellement2022)}
        de l’eau ({milliers(c.naissances2022)} naissances et {milliers(c.deces2022)} décès en 2022). Ce
        renouvellement est celui de toute population ; la thèse du « grand remplacement » parle d’autre
        chose, de composition (plus bas).
      </p>
      <p>
        Un immigré est né étranger à l’étranger. Le stock d’immigrés ne se vide que par les décès et
        les départs. Il est passé de {milliers(c.immigres1968)} en 1968 (métropole) à {milliers(
          c.immigres2025
        )} en 2025 (France, provisoire) ; environ {milliers(c.collecte2024)} de l’écart tiennent à la
        nouvelle collecte du recensement en 2024, pas à des arrivées.
      </p>
      <p>
        <strong>De qui naissent les enfants</strong> est la question de la composition. Les
        naissances de 2022 par origine des parents viennent de l’état civil, corrigé de l’écart
        entre « né à l’étranger » et « immigré » ; environ {milliers(c.nais2022.g3)}
        étaient des petits-enfants d’immigrés (modèle). Nés en France d’un parent lui-même né en France,
        ceux-ci sont français dès la naissance (double droit du sol). Les enfants d’immigrés le sont si
        l’un de leurs parents est français ; sinon, ils le deviennent à 18 ans s’ils résident en France
        et y ont résidé au moins cinq ans depuis l’âge de 11 ans (code civil, art. 21-7).
      </p>
      <p>
        Les unions d’aujourd’hui donnent une indication sur la génération suivante : parmi ceux qui
        vivent en couple, {c.majoritaireUnParent} % des enfants d’un seul parent immigré ont un conjoint
        de la population majoritaire, contre {c.majoritaireDeuxParents} % des enfants de deux parents
        immigrés (TeO2, ch. 8, tableau 3). L’incorporation est « perceptible » pour les descendants des
        vagues européennes de l’entre-deux-guerres (TeO2, ch. 8) ; pour les immigrations plus récentes,
        il est trop tôt pour le dire (voir <a href="/generations">Générations</a>).
      </p>
      <p>
        En 2025, le modèle compte {pct((100 * (c.g2a2025 + c.g2b2025)) / c.pop2025)} d’enfants d’immigrés
        ; l’enquête Emploi de l’Insee en mesure {milliers(c.descendants2025)}, soit {pct(
          (100 * c.descendants2025) / c.pop2025
        )} de la population. L’enquête ne compte que les logements ordinaires, hors Mayotte ; le modèle,
        toute la population (U19).
      </p>
    </Detail>
  </section>

  <section class="colonne">
    <Detail
      encadre
      niveau={2}
      titre="Ce qu’on ne sait pas, et comment c’est montré"
      resume="Avant 2006, seul le solde net est connu ; les enfants et petits-enfants d’immigrés viennent d’un modèle ; les champs et la collecte changent."
    >
      <dl class="incertitudes">
        {#each data.incertitudes as u (u.code)}
          <dt><span class="code">{u.code}</span> {u.titre}</dt>
          <dd>
            {u.detail}
            <em
              >Dans la piscine : {u.traitement.charAt(0).toLowerCase() + u.traitement.slice(1)}.</em
            >
          </dd>
        {/each}
      </dl>
      <p>
        Les enfants et petits-enfants d’immigrés viennent d’un modèle de cohortes : la statistique
        publique les mesure par enquête (2019-2020, 2025), pas chaque année. Le modèle vieillit les
        générations âge par âge, avec la mortalité nationale ; il est calé sur l’état civil et sur
        l’enquête de 2019-2020, et contrôlé par le nombre de descendants mesuré en 2025 et par les
        décès d’immigrés estimés par l’Insee. Paramètre de la vanne des décès (statut : <strong
          >{data.piscine.statut_parametres === 'valide' ? 'validé' : 'à valider'}</strong
        >) : avant 2006 et après 2022, les décès d’immigrés sont estimés en appliquant à leur part
        dans la population le rapport observé de {r.calage[0]} à {r.calage[1]} entre leur part dans les
        décès et leur part dans la population : {virgule(r.moyen)} en moyenne, de {virgule(r.min)} à {virgule(
          r.max
        )}
        selon les années (fourchette des estimations). Une particule représente {entier(
          data.piscine.echelle
        )} personnes (le double sur petit écran).
      </p>
    </Detail>
    <p>
      Données : <a href="/donnees/piscine.csv">piscine.csv</a>,
      <a href="/donnees/piscine.json">piscine.json</a> (Insee, Licence Ouverte 2.0).
    </p>
  </section>
</article>

<style>
  .defile {
    overflow-x: auto;
    max-height: 32rem;
    overflow-y: auto;
  }
  .annees {
    border-collapse: collapse;
    font-size: var(--t-0);
    font-variant-numeric: tabular-nums;
  }
  .annees th,
  .annees td {
    padding: 0.15rem 0.6rem;
    border-bottom: 1px solid var(--reglure);
    text-align: right;
    white-space: nowrap;
  }
  .annees thead th {
    position: sticky;
    top: 0;
    background: var(--papier);
  }
  .annees .regime {
    text-align: left;
    color: var(--ardoise);
  }
  section {
    margin-top: 2rem;
  }
  .mode-emploi {
    color: var(--ardoise);
  }
  .points {
    padding-left: 1.4rem;
  }
  .points li {
    margin: 0.6rem 0;
  }
  .incertitudes dt {
    font-weight: 600;
    margin-top: 0.75rem;
  }
  .incertitudes dd {
    margin: 0.15rem 0 0;
    color: var(--ardoise);
  }
  .code {
    font-size: var(--t-0);
    color: var(--gris);
    font-variant-numeric: tabular-nums;
  }
</style>
