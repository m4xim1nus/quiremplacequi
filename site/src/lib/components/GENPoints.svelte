<script lang="ts">
  // Nuage de points en lignes (dot plot), en HTML : une ligne par groupe, un point par série
  // (forme ET couleur, jamais la couleur seule), ligne de zéro, une seule échelle. `precision` :
  // valeurs lues sur un graphique, affichées avec leur marge de lecture.
  import { pts } from '$lib/generations';

  interface Serie {
    cle: string;
    libelle: string;
    couleur: string;
    forme: 'rond' | 'carre' | 'creux';
  }
  let {
    lignes,
    series,
    min,
    max,
    unite = 'pt',
    precision = null,
    format
  }: {
    lignes: { libelle: string; valeurs: Record<string, number> }[];
    series: Serie[];
    min: number;
    max: number;
    unite?: string;
    precision?: number | null;
    format?: (x: number) => string;
  } = $props();

  const f = $derived(format ?? ((x: number) => (unite === 'pt' ? pts(x) : `${x} ${unite}`)));
  const pos = (x: number) => (100 * (x - min)) / (max - min);
  const graduations = $derived.by(() => {
    const pas = max - min > 30 ? 10 : 5;
    const g = [];
    for (let x = Math.ceil(min / pas) * pas; x <= max; x += pas) g.push(x);
    return g;
  });
</script>

<ul class="legende" aria-label="Légende">
  {#each series as s (s.cle)}
    <li><span class="point {s.forme}" style:--c={s.couleur}></span>{s.libelle}</li>
  {/each}
  {#if precision}<li class="prec">
      lecture sur graphique : ± {String(precision).replace('.', ',')}&nbsp;{unite}
    </li>{/if}
</ul>
<div class="lignes">
  <div class="ligne axe" aria-hidden="true">
    <div></div>
    <div class="piste">
      {#each graduations as g (g)}
        <span class="grad" style:left="{pos(g)}%">{g}</span>
      {/each}
    </div>
  </div>
  {#each lignes as l (l.libelle)}
    <div class="ligne">
      <div class="libelle">{l.libelle}</div>
      <div class="piste">
        {#if min < 0}<span class="zero" style:left="{pos(0)}%"></span>{/if}
        {#each series as s (s.cle)}
          {#if l.valeurs[s.cle] !== undefined}
            <!-- Focusable pour la bulle au clavier ; les valeurs sont aussi dans le tableau. -->
            <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
            <span
              class="marque"
              style:left="{pos(l.valeurs[s.cle])}%"
              tabindex="0"
              role="img"
              aria-label="{l.libelle}, {s.libelle} : {f(l.valeurs[s.cle])}"
            >
              {#if precision}<span
                  class="marge"
                  style:width="{(200 * precision) / (max - min)}cqw"
                  style:--c={s.couleur}
                ></span>{/if}
              <span class="point {s.forme}" style:--c={s.couleur}></span>
              <span class="bulle" aria-hidden="true"
                ><strong>{precision ? '≈ ' : ''}{f(l.valeurs[s.cle])}</strong>
                {s.libelle}</span
              >
            </span>
          {/if}
        {/each}
      </div>
    </div>
  {/each}
</div>

<style>
  .legende {
    list-style: none;
    padding: 0;
    margin: 0 0 0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1rem;
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .legende .point {
    position: static;
    display: inline-block;
    margin-right: 0.4em;
    vertical-align: -0.05em;
    transform: none;
  }
  .prec {
    color: var(--gris);
  }
  .lignes {
    display: grid;
    gap: 0.15rem;
  }
  .ligne {
    display: grid;
    grid-template-columns: minmax(8rem, 15rem) 1fr;
    align-items: center;
    gap: 0.75rem;
  }
  .libelle {
    font-size: var(--t-0);
    color: var(--encre);
  }
  .piste {
    position: relative;
    height: 1.5rem;
    container-type: inline-size;
    border-bottom: 1px solid var(--reglure);
  }
  .axe .piste {
    height: 1.1rem;
    border-bottom: none;
  }
  .grad {
    position: absolute;
    transform: translateX(-50%);
    font-size: 0.7rem;
    color: var(--gris);
    font-variant-numeric: tabular-nums;
  }
  .zero {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 1px;
    background: var(--gris);
  }
  .marque {
    position: absolute;
    top: 50%;
    width: 1.4rem;
    height: 1.4rem;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
  .marge {
    position: absolute;
    height: 3px;
    border-radius: 2px;
    background: var(--c);
    opacity: 0.3;
  }
  .point {
    width: 0.6rem;
    height: 0.6rem;
    background: var(--c);
    border-radius: 50%;
    box-shadow: 0 0 0 2px var(--papier);
  }
  .point.carre {
    border-radius: 1px;
  }
  .point.creux {
    background: var(--papier);
    border: 2px solid var(--c);
    box-sizing: border-box;
  }
  .bulle {
    display: none;
    position: absolute;
    bottom: calc(100% + 4px);
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
  .marque:hover .bulle,
  .marque:focus-visible .bulle {
    display: block;
  }
  .marque:hover .point,
  .marque:focus-visible .point {
    transform: scale(1.3);
  }
  @media (max-width: 599px) {
    .ligne {
      grid-template-columns: 1fr;
      gap: 0;
    }
    .axe > div:first-child {
      display: none;
    }
  }
</style>
