<script lang="ts">
  // Barres horizontales : groupées (une barre par série, valeur au bout) ou empilées à 100 %
  // (segments séparés par un espace de 2 px, valeur dans le segment quand elle tient). Légende
  // dès deux séries ; infobulle au survol de chaque barre ou segment.
  import { scaleLinear } from 'd3-scale';

  interface Ligne {
    libelle: string;
    valeurs: (number | null)[];
  }
  interface Cle {
    libelle: string;
    couleur: string;
    /** Couleur du texte posé dans un segment (empilé). */
    texte?: string;
  }

  let {
    lignes,
    cles,
    mode = 'groupe',
    max,
    format,
    titre
  }: {
    lignes: Ligne[];
    cles: Cle[];
    mode?: 'groupe' | 'empile';
    max?: number;
    format: (v: number) => string;
    titre: string;
  } = $props();

  let largeur = $state(640);
  // Sur petit écran, le libellé passe au-dessus des barres au lieu d'être tronqué à gauche.
  const etroit = $derived(largeur < 480);
  const gaucheLib = $derived(etroit ? 0 : 190);
  const dessus = $derived(etroit ? 16 : 0);
  const epais = 14;
  const hauteurLigne = $derived(
    (mode === 'groupe' ? cles.length * (epais + 3) + 10 : epais + 12) + dessus
  );
  const hauteur = $derived(lignes.length * hauteurLigne + 4);
  const vmax = $derived(
    max ?? Math.max(...lignes.flatMap((l) => l.valeurs.map((v) => v ?? 0))) * 1.05
  );
  const x = $derived(
    scaleLinear()
      .domain([0, mode === 'empile' ? 100 : vmax])
      .range([0, largeur - gaucheLib - (mode === 'groupe' ? 44 : 4)])
  );

  let survol: { l: number; k: number } | null = $state(null);
  const debut = (l: Ligne, k: number) =>
    l.valeurs.slice(0, k).reduce<number>((s, v) => s + (v ?? 0), 0);
</script>

{#if cles.length > 1}
  <p class="legende">
    {#each cles as c (c.libelle)}
      <span><b class="pastille" style:background={c.couleur}></b>{c.libelle}</span>
    {/each}
  </p>
{/if}
<div class="graphique" bind:clientWidth={largeur}>
  <svg
    width={largeur}
    height={hauteur}
    viewBox="0 0 {largeur} {hauteur}"
    role="img"
    aria-label={titre}
    onpointerleave={() => (survol = null)}
  >
    {#each lignes as l, i (l.libelle)}
      {@const y0 = i * hauteurLigne + 4}
      {#if etroit}
        <text class="libelle" x="0" y={y0 + 6} text-anchor="start">{l.libelle}</text>
      {:else}
        <text class="libelle" x={gaucheLib - 8} y={y0 + (hauteurLigne - 10) / 2} text-anchor="end"
          >{l.libelle}</text
        >
      {/if}
      {#each l.valeurs as v, k (k)}
        {#if v !== null && v > 0}
          {@const bx = mode === 'empile' ? gaucheLib + x(debut(l, k)) : gaucheLib}
          {@const by = (mode === 'empile' ? y0 : y0 + k * (epais + 3)) + dessus}
          {@const bw = Math.max(0, x(v) - (mode === 'empile' ? 2 : 0))}
          <rect
            role="presentation"
            x={bx}
            y={by}
            width={bw}
            height={epais}
            rx="3"
            style:fill={cles[k].couleur}
            opacity={survol && (survol.l !== i || survol.k !== k) ? 0.55 : 1}
            onpointerenter={() => (survol = { l: i, k })}
          />
          {#if mode === 'groupe'}
            <text class="valeur" x={bx + bw + 4} y={by + epais / 2} dominant-baseline="middle"
              >{format(v)}</text
            >
          {:else if bw > 30}
            <text
              class="dedans"
              x={bx + bw / 2}
              y={by + epais / 2}
              text-anchor="middle"
              dominant-baseline="middle"
              style:fill={cles[k].texte ?? 'var(--papier)'}>{format(v)}</text
            >
          {/if}
        {/if}
      {/each}
    {/each}
  </svg>
  {#if survol}
    {@const l = lignes[survol.l]}
    <div
      class="infobulle"
      role="status"
      style:top="{survol.l * hauteurLigne + hauteurLigne + 2}px"
      style:left="{gaucheLib}px"
    >
      <strong>{l.libelle}</strong> · {cles[survol.k].libelle} :
      {format(l.valeurs[survol.k] ?? 0)}
    </div>
  {/if}
</div>

<style>
  .graphique {
    position: relative;
    width: 100%;
  }
  svg {
    display: block;
    overflow: visible;
  }
  .libelle {
    font-size: 11.5px;
    fill: var(--ardoise);
    dominant-baseline: middle;
  }
  .valeur,
  .dedans {
    font-size: 11px;
    font-variant-numeric: tabular-nums;
  }
  .valeur {
    fill: var(--ardoise);
  }
  .legende {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1rem;
    font-size: var(--t-0);
    color: var(--ardoise);
    margin: 0.25rem 0 0.5rem;
  }
  .pastille {
    display: inline-block;
    width: 0.75em;
    height: 0.75em;
    border-radius: 3px;
    margin-right: 0.35em;
    vertical-align: -0.05em;
  }
  .infobulle {
    position: absolute;
    pointer-events: none;
    background: var(--papier);
    border: 1px solid var(--reglure);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-size: var(--t-0);
    z-index: 1;
    white-space: nowrap;
  }
</style>
