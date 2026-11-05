<script lang="ts">
  // Cadre d'un graphique (charte, docs/CADRAGE.md §6) : titre, graphique, ligne « Lecture : »,
  // source, champ, statut, téléchargement, et le tableau équivalent repliable.
  import type { Snippet } from 'svelte';

  let {
    titre,
    lecture,
    source,
    champ,
    statut,
    fichiers,
    children,
    tableau
  }: {
    titre: string;
    lecture: string;
    source: string;
    champ: string;
    statut?: string;
    fichiers: string[];
    children: Snippet;
    tableau?: Snippet;
  } = $props();
</script>

<figure class="cadre">
  <h3>{titre}</h3>
  {@render children()}
  <figcaption>
    <p class="lecture">Lecture : {lecture}</p>
    <p>
      Source : {source}. Champ : {champ}.
      {#if statut}Statut : {statut}.{/if}
      Données :
      {#each fichiers as f, i (f)}<a href="/donnees/{f}">{f}</a>{i < fichiers.length - 1
          ? ', '
          : ''}{/each}.
    </p>
    {#if tableau}
      <details>
        <summary>Voir le tableau</summary>
        {@render tableau()}
      </details>
    {/if}
  </figcaption>
</figure>

<style>
  .cadre {
    margin: 1.5rem 0 2rem;
  }
  h3 {
    font-size: var(--t-1);
    margin: 0 0 0.75rem;
  }
  figcaption {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin-top: 0.75rem;
  }
  figcaption p {
    margin: 0.3rem 0;
  }
  .lecture {
    color: var(--encre);
  }
  details {
    margin-top: 0.4rem;
  }
  summary {
    cursor: pointer;
    color: var(--lien);
  }
  details :global(table) {
    border-collapse: collapse;
    font-variant-numeric: tabular-nums;
    margin-top: 0.4rem;
    display: block;
    overflow-x: auto;
    max-width: 100%;
  }
  details :global(th),
  details :global(td) {
    padding: 0.1rem 0.6rem;
    text-align: right;
    border-bottom: 1px solid var(--reglure);
    white-space: nowrap;
  }
  details :global(th:first-child),
  details :global(td:first-child) {
    text-align: left;
  }
</style>
