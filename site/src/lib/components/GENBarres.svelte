<script lang="ts">
  // Barres horizontales simples, en HTML : une valeur par ligne, axe à zéro, valeur en bout de
  // barre, bulle au survol et au focus.
  import { pc } from '$lib/generations';

  let {
    lignes,
    max = 100,
    couleur = 'var(--s1)'
  }: {
    lignes: { libelle: string; valeur: number; couleur?: string; detail?: string }[];
    max?: number;
    couleur?: string;
  } = $props();
</script>

<div class="lignes">
  {#each lignes as l (l.libelle)}
    <div class="ligne">
      <div class="libelle">{l.libelle}</div>
      <div class="piste">
        <!-- Focusable pour la bulle au clavier ; les valeurs sont aussi dans le tableau. -->
        <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
        <span
          class="barre"
          style:width="{(100 * l.valeur) / max}%"
          style:background={l.couleur ?? couleur}
          tabindex="0"
          role="img"
          aria-label="{l.libelle} : {pc(l.valeur)}"
        >
          <span class="bulle" aria-hidden="true"
            ><strong>{pc(l.valeur)}</strong> {l.detail ?? l.libelle}</span
          >
        </span>
        <span class="val">{pc(l.valeur)}</span>
      </div>
    </div>
  {/each}
</div>

<style>
  .lignes {
    display: grid;
    gap: 0.45rem;
  }
  .ligne {
    display: grid;
    grid-template-columns: minmax(8rem, 15rem) 1fr;
    align-items: center;
    gap: 0.25rem 0.75rem;
  }
  .libelle {
    font-size: var(--t-0);
    color: var(--encre);
  }
  .piste {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    height: 1.3rem;
    border-left: 1px solid var(--gris);
  }
  .barre {
    position: relative;
    height: 100%;
    border-radius: 0 4px 4px 0;
    min-width: 2px;
  }
  .val {
    font-size: var(--t-0);
    color: var(--ardoise);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .bulle {
    display: none;
    position: absolute;
    bottom: calc(100% + 6px);
    left: 100%;
    transform: translateX(-50%);
    z-index: 2;
    background: var(--papier);
    color: var(--ardoise);
    border: 1px solid var(--reglure);
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
    font-size: var(--t-0);
    white-space: nowrap;
    box-shadow: 0 2px 6px rgb(0 0 0 / 12%);
  }
  .bulle strong {
    color: var(--encre);
  }
  .barre:hover,
  .barre:focus-visible {
    filter: brightness(1.12);
  }
  .barre:hover .bulle,
  .barre:focus-visible .bulle {
    display: block;
  }
  @media (max-width: 599px) {
    .ligne {
      grid-template-columns: 1fr;
    }
  }
</style>
