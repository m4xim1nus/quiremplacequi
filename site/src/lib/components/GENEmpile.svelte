<script lang="ts">
  // Barres horizontales empilées (100 % ou partielles), en HTML : une ligne par groupe, un segment
  // par catégorie, 2 px d'espace entre segments, étiquette dans le segment s'il est assez large,
  // bulle au survol et au focus. Légende toujours présente.
  import { pc } from '$lib/generations';

  interface Segment {
    cle: string;
    valeur: number;
  }
  let {
    lignes,
    legende,
    max = 100,
    note
  }: {
    lignes: { libelle: string; segments: Segment[]; fin?: string }[];
    legende: { cle: string; libelle: string; couleur: string; claire?: boolean }[];
    max?: number;
    note?: (l: { libelle: string; segments: Segment[] }) => string;
  } = $props();

  const info = (cle: string) => legende.find((x) => x.cle === cle)!;
</script>

<ul class="legende" aria-label="Légende">
  {#each legende as l (l.cle)}
    <li><span class="cle" style:background={l.couleur}></span>{l.libelle}</li>
  {/each}
</ul>
<div class="lignes">
  {#each lignes as l (l.libelle)}
    <div class="ligne">
      <div class="libelle">{l.libelle}</div>
      <div class="piste">
        {#each l.segments.filter((s) => s.valeur > 0) as s (s.cle)}
          <!-- Focusable pour la bulle au clavier ; les valeurs sont aussi dans le tableau. -->
          <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
          <span
            class="segment"
            class:clair={info(s.cle).claire}
            style:width="{(100 * s.valeur) / max}%"
            style:background={info(s.cle).couleur}
            tabindex="0"
            role="img"
            aria-label="{l.libelle}, {info(s.cle).libelle} : {pc(s.valeur)}"
          >
            {#if s.valeur / max >= 0.1}<span class="val">{pc(s.valeur)}</span>{/if}
            <span class="bulle" aria-hidden="true"
              ><strong>{pc(s.valeur)}</strong> {info(s.cle).libelle}</span
            >
          </span>
        {/each}
      </div>
      {#if l.fin || note}<div class="fin">{l.fin ?? note?.(l)}</div>{/if}
    </div>
  {/each}
</div>

<style>
  .legende {
    list-style: none;
    padding: 0;
    margin: 0 0 0.75rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1rem;
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .cle {
    display: inline-block;
    width: 0.8em;
    height: 0.8em;
    border-radius: 2px;
    margin-right: 0.4em;
    vertical-align: -0.08em;
  }
  .lignes {
    display: grid;
    gap: 0.55rem;
  }
  .ligne {
    display: grid;
    grid-template-columns: minmax(8rem, 15rem) 1fr auto;
    align-items: center;
    gap: 0.25rem 0.75rem;
  }
  .libelle {
    font-size: var(--t-0);
    color: var(--encre);
  }
  .fin {
    font-size: var(--t-0);
    color: var(--ardoise);
    font-variant-numeric: tabular-nums;
    min-width: 4.5rem;
  }
  .piste {
    display: flex;
    gap: 2px;
    height: 1.6rem;
  }
  .segment {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    min-width: 2px;
    outline-offset: 2px;
  }
  .segment:first-child {
    border-radius: 4px 2px 2px 4px;
  }
  .segment:last-child {
    border-radius: 2px 4px 4px 2px;
  }
  .val {
    font-size: 0.72rem;
    font-weight: 600;
    color: #fff;
    font-variant-numeric: tabular-nums;
    pointer-events: none;
    white-space: nowrap;
    overflow: hidden;
  }
  .clair .val {
    color: var(--encre);
  }
  .bulle {
    display: none;
    position: absolute;
    bottom: calc(100% + 6px);
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
    background: var(--papier);
    color: var(--ardoise);
    border: 1px solid var(--reglure);
    border-radius: 2px;
    padding: 0.25rem 0.5rem;
    font-size: var(--t-0);
    white-space: nowrap;
    box-shadow: 0 2px 6px rgb(0 0 0 / 12%);
  }
  .bulle strong {
    color: var(--encre);
  }
  .segment:hover,
  .segment:focus-visible {
    filter: brightness(1.12);
  }
  .segment:hover .bulle,
  .segment:focus-visible .bulle {
    display: block;
  }
  @media (max-width: 599px) {
    .ligne {
      grid-template-columns: 1fr auto;
    }
    .libelle {
      grid-column: 1 / -1;
    }
  }
</style>
