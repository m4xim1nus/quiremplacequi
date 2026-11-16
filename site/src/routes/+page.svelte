<script lang="ts">
  import { milliers, pct } from '$lib/format';
  let { data } = $props();
  const signe = (x: number) => (x < 0 ? '−' : '+') + milliers(Math.abs(x));
</script>

<svelte:head>
  <title>Qui remplace qui ?</title>
  <meta
    name="description"
    content="Démographie et migrations en France, mesurées avec la statistique publique."
  />
</svelte:head>

<article class="page">
  <div class="colonne">
    <h1>Qui remplace qui ?</h1>
    <p class="chapeau">
      La thèse du « grand remplacement » affirme qu’une population en remplace une autre. Ce site la
      prend au mot et la mesure, avec la statistique publique : combien, depuis quand, à quelle
      vitesse, qui arrive, qui part, et ce que deviennent les enfants.
    </p>
    <p>
      Il commence par ce qui est vrai : il n’y a jamais eu autant d’immigrés en France,
      {milliers(data.immigres2025)} en 2025 (chiffre provisoire, dont environ {milliers(
        data.collecte2024
      )} dus à l’amélioration de la collecte du recensement en 2024), soit {pct(data.part2025)} de la
      population, contre {pct(data.part1931)} au sommet de 1931 et {pct(data.partDebut)} en
      {data.debut} (France métropolitaine avant 1990). Et le solde migratoire est devenu le premier moteur
      de la croissance de la population : il dépasse le solde naturel chaque année depuis
      {data.soldes.depuis}, et en {data.soldes.dernier}{data.soldes.provisoire
        ? ' (provisoire)'
        : ''}, les naissances ne compensent plus les décès ({signe(data.soldes.naturel)}, contre {signe(
        data.soldes.migratoire
      )} pour le solde migratoire). Puis il regarde ce que les chiffres bruts cachent : les départs, les
      définitions, les générations qui se mêlent.
    </p>
    <p class="brouillon">Site en construction. Textes en brouillon.</p>
  </div>

  <ul class="portes">
    <li>
      <a href="/piscine">
        <span class="titre">La piscine</span>
        <span
          >Toute la population comme une eau qui se renouvelle : en 2022, {milliers(
            data.naissances2022
          )} naissances pour {milliers(data.entreesImm2022)} arrivées d’immigrés.</span
        >
      </a>
    </li>
    <li>
      <a href="/temps-long">
        <span class="titre">Le temps long</span>
        <span
          >Les Belges, les Italiens, les Polonais, les Espagnols, les Portugais : comment une vague
          migratoire monte, puis se tarit.</span
        >
      </a>
    </li>
    <li>
      <a href="/generations">
        <span class="titre">Générations</span>
        <span
          >Combien sont-ils ? La réponse change du simple au triple selon qui l’on compte. Le
          mélange, et les discriminations.</span
        >
      </a>
    </li>
  </ul>
</article>

<style>
  .portes {
    list-style: none;
    padding: 0;
    margin: 2.5rem 0 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
    gap: 1rem;
  }
  .portes a {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    height: 100%;
    padding: 1.1rem 1.2rem;
    border: 1px solid var(--reglure);
    border-radius: 0.6rem;
    text-decoration: none;
    color: var(--ardoise);
  }
  .portes a:hover,
  .portes a:focus-visible {
    border-color: var(--lien);
  }
  .titre {
    font-weight: 700;
    font-size: var(--t-2);
    color: var(--encre);
  }
</style>
