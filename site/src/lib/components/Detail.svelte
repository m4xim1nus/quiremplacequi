<script lang="ts">
  // Repli : « Le détail » d'une section (nuances, méthode, comparaisons de sources), ou un
  // encadré (contradicteurs, limites) dont seul le titre et un résumé d'une ligne sont visibles.
  import type { Snippet } from 'svelte';

  let {
    titre = 'Le détail',
    resume,
    niveau,
    encadre = false,
    children
  }: {
    titre?: string;
    resume?: string;
    /** Le titre est un intertitre (h2, h3) : il reste dans le plan de la page. */
    niveau?: 2 | 3;
    encadre?: boolean;
    children: Snippet;
  } = $props();
</script>

<details class="detail" class:encadre>
  <summary>
    {#if niveau}
      <svelte:element this={`h${niveau}`} class="titre">{titre}</svelte:element>
    {:else}
      <span class="titre">{titre}</span>
    {/if}
    {#if resume}<span class="resume">{resume}</span>{/if}
  </summary>
  <div class="corps">{@render children()}</div>
</details>

<style>
  .detail {
    margin: 1rem 0 2rem;
    border-left: 3px solid var(--reglure);
    padding-left: 1rem;
  }
  .encadre {
    border: 1px solid var(--reglure);
    border-radius: 6px;
    padding: 0.6rem 1rem;
    margin: 2rem 0;
  }
  summary {
    cursor: pointer;
    list-style-position: outside;
    color: var(--lien);
  }
  .encadre summary {
    margin-left: 1rem;
  }
  .titre {
    display: inline;
    font-size: var(--t-1);
    font-weight: 600;
    margin: 0;
  }
  .encadre .titre {
    color: var(--encre);
    font-size: var(--t-2);
  }
  .resume {
    display: block;
    font-size: var(--t-0);
    color: var(--ardoise);
    margin-top: 0.2rem;
  }
  .corps {
    margin-top: 0.5rem;
  }
  .corps :global(p:first-child) {
    margin-top: 0.5rem;
  }
</style>
