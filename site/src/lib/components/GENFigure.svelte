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
  .gen-figure {
    margin: 1.5rem 0 2.5rem;
  }
  .titre {
    font-weight: 600;
    color: var(--encre);
    margin-bottom: 0.75rem;
  }
  .lecture,
  .meta {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin: 0.5rem 0 0;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem 0.8rem;
    color: var(--gris);
  }
  .badge {
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    padding: 0 0.4rem;
    border: 1px dashed currentColor;
    border-radius: 0.25rem;
    color: var(--ardoise);
  }
  details {
    margin-top: 0.5rem;
    font-size: var(--t-0);
  }
  summary {
    cursor: pointer;
    color: var(--lien);
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
