<script lang="ts">
  import Piscine from '$lib/components/Piscine.svelte';
  import { entier, milliers, pct } from '$lib/format';

  let { data } = $props();
  const c = $derived(data.chiffres);
  const r = $derived(data.piscine.ratio_deces);
  const virgule = (x: number, n = 2) => x.toFixed(n).replace('.', ',');
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
      robinets (les naissances, les arrivées), deux bondes (les décès, les départs).
    </p>
    <p class="brouillon">
      Prototype v1, en construction. Textes en brouillon. L’eau est d’abord montrée
      <strong>décantée</strong> : chaque génération forme une couche, pour en lire le volume ; le bouton
      « Mélangée » remet tout le monde dans la même eau. L’épaisseur des tuyaux suit le débit de chaque
      vanne.
    </p>
  </header>

  <Piscine donnees={data.piscine} />

  <section class="colonne">
    <h2>Ce qu’il faut regarder</h2>
    <p>
      <strong>Le robinet des naissances débite le plus.</strong> En 2022, {milliers(
        c.naissances2022
      )} naissances, contre {milliers(c.entreesImm2022)} arrivées d’immigrés et {milliers(
        c.deces2022
      )} décès. Chaque année, les naissances renouvellent à elles seules {pct(
        100 * c.renouvellement2022
      )} de l’eau : en un siècle environ, toute l’eau de la piscine est remplacée, avec ou sans immigration.
    </p>
    <p>
      <strong>Les immigrés n’ont pas de robinet « naissances ».</strong> Un immigré est né étranger
      à l’étranger : ses enfants, nés en France, entrent par le robinet commun et ne sont pas des
      immigrés. Le stock d’immigrés ne grossit que par les arrivées et ne se vide que par les décès
      et les départs. Il est passé de {milliers(c.immigres1968)} en 1968 ({pct(c.part1968)} de la population)
      à {milliers(c.immigres2025)} en 2025 ({pct(c.part2025)}).
    </p>
    <p>
      <strong>De qui naissent les enfants ?</strong> C’est la vraie question : tout le monde meurt,
      tout le monde est remplacé, et la thèse du « grand remplacement » parle de composition, pas de
      renouvellement. En 2022, sur {milliers(c.naissances2022)} naissances, environ {milliers(
        c.nais2022.g2a
      )} enfants avaient deux parents immigrés et {milliers(c.nais2022.g2b)} un seul (état civil, corrigé
      de l’écart entre « né à l’étranger » et « immigré ») ; environ {milliers(c.nais2022.g3)}
      étaient des petits-enfants d’immigrés (modèle). Ces enfants sont français dès la naissance si l’un
      de leurs parents l’est, et le deviennent sinon en principe à leur majorité (droit du sol).
    </p>
    <p>
      <strong>Si les unions restent aussi mixtes qu’aujourd’hui</strong>, leurs propres enfants
      auront le plus souvent des parents nés en France, et la teinte se diluera de génération en
      génération. Cette incorporation est « perceptible » pour les descendants des vagues
      européennes de l’entre-deux-guerres (TeO2, ch. 8) ; pour les immigrations plus récentes, il
      est trop tôt pour le dire (voir
      <a href="/generations">Générations</a>).
    </p>
    <p>
      <strong>Pas deux blocs, des couches qui se recouvrent.</strong> En 2025, le modèle compte
      {pct((100 * (c.g2a2025 + c.g2b2025)) / c.pop2025)} d’enfants d’immigrés ; l’enquête Emploi de l’Insee
      en mesure {milliers(c.descendants2025)}, soit {pct((100 * c.descendants2025) / c.pop2025)} de la
      population, dont {c.descendantsUnParent} % n’ont qu’un parent immigré. Ces catégories ne s’additionnent
      pas en un « camp » : {c.g3UnGrandParent} % des petits-enfants d’immigrés de 18 à 59 ans n’ont qu’un
      seul grand-parent immigré sur quatre (TeO2, ch. 8, tableau 4).
    </p>
  </section>

  <section class="colonne">
    <h2>Ce qu’on ne sait pas, et comment c’est montré</h2>
    <dl class="incertitudes">
      {#each data.incertitudes as u (u.code)}
        <dt><span class="code">{u.code}</span> {u.titre}</dt>
        <dd>{u.detail} <em>Dans la piscine : {u.traitement.toLowerCase()}.</em></dd>
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
    <p>
      Données : <a href="/donnees/piscine.csv">piscine.csv</a>,
      <a href="/donnees/piscine.json">piscine.json</a> (Insee, Licence Ouverte 2.0).
    </p>
  </section>
</article>

<style>
  section {
    margin-top: 2rem;
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
