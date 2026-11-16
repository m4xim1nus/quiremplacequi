<script lang="ts">
  // Cadre commun d'une figure de la page « Générations » : titre, graphique, ligne « Lecture »,
  // source, champ, statut, badges d'incertitude, CSV, et tableau équivalent repliable.
  import type { Snippet } from 'svelte';

  let {
    titre,
    lecture,
    source,
    champ,
    statut = 'Saisi depuis le livre, une référence par cellule',
    badges = [],
    csv = 'teo2.csv',
    children,
    tableau
  }: {
    titre: string;
    lecture: string;
    source: string;
    champ: string;
    statut?: string;
    badges?: string[];
    csv?: string;
    children: Snippet;
    tableau?: Snippet;
  } = $props();
</script>

<figure class="gen-figure">
  <figcaption class="titre">{titre}</figcaption>
  <div class="graphique">{@render children()}</div>
  <p class="lecture">Lecture : {lecture}</p>
  <p class="meta">
    {#each badges as b (b)}<span class="badge">{b}</span>{/each}
    <span>Source : {source}.</span>
    <span>Champ : {champ}.</span>
    <span>Statut : {statut}.</span>
    <a href="/donnees/{csv}" download>Données (CSV)</a>
  </p>
  {#if tableau}
    <details>
      <summary>Tableau des valeurs</summary>
      <div class="defile">{@render tableau()}</div>
    </details>
  {/if}
</figure>

<style>
  /* Cadre commun (docs/CONCEPTION.md §4) : filet épais à l'encre, titre en Barlow, puis lecture,
     source, champ et codes U en plaques ocre. */
  .gen-figure {
    margin: 1.75rem 0 2.75rem;
    padding-top: 1rem;
    border-top: 2px solid var(--encre);
  }
  .titre {
    font-family: var(--titre);
    font-weight: 600;
    font-size: var(--t-2);
    line-height: 1.2;
    color: var(--encre);
    margin-bottom: 0.9rem;
  }
  .lecture,
  .meta {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin: 0.6rem 0 0;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.3rem 0.9rem;
  }
  .badge {
    font-family: var(--titre);
    font-weight: 600;
    font-size: 0.8rem;
    padding: 0 0.4rem;
    border: 1.5px solid var(--repere);
    border-radius: 2px;
    color: var(--repere-texte);
    background: var(--plaque);
  }
  details {
    margin-top: 0.6rem;
    font-size: var(--t-0);
  }
  summary {
    cursor: pointer;
    color: var(--encre);
    text-decoration: underline;
    text-decoration-color: var(--repere);
    text-underline-offset: 3px;
  }
  .defile {
    overflow-x: auto;
  }
  .defile :global(table) {
    border-collapse: collapse;
    margin-top: 0.5rem;
    font-variant-numeric: tabular-nums;
  }
  .defile :global(th),
  .defile :global(td) {
    padding: 0.15rem 0.6rem;
    border-bottom: 1px solid var(--reglure);
    text-align: right;
  }
  .defile :global(th:first-child),
  .defile :global(td:first-child) {
    text-align: left;
  }
</style>
