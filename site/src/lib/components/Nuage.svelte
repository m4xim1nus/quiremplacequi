<script lang="ts">
  // Nuage de points : axe horizontal logarithmique, axe vertical linéaire depuis zéro, disques
  // d'aire proportionnelle à un poids (population). Un trait en escalier porte une valeur par
  // tranche (médianes). Points mis en évidence en ocre et étiquetés ; infobulle au survol.
  import { scaleLog, scaleLinear, scaleSqrt } from 'd3-scale';

  interface Point {
    id: string;
    libelle: string;
    x: number;
    y: number;
    poids: number;
    accent?: boolean;
  }
  interface Palier {
    de: number;
    a: number;
    y: number;
  }

  let {
    points,
    paliers = [],
    xFormat,
    yFormat,
    xTicks,
    titre,
    infobulle,
    libellePaliers = 'Médiane de la tranche',
    hauteur = 380
  }: {
    points: Point[];
    paliers?: Palier[];
    xFormat: (x: number) => string;
    yFormat: (y: number) => string;
    xTicks: number[];
    titre: string;
    infobulle: (p: Point) => string;
    libellePaliers?: string;
    hauteur?: number;
  } = $props();

  let largeur = $state(640);
  const m = $derived({ haut: 14, droite: 12, bas: 30, gauche: 44 });
  const x = $derived(
    scaleLog()
      .domain([
        Math.min(...points.map((p) => p.x)) * 0.9,
        Math.max(...points.map((p) => p.x)) * 1.1
      ])
      .range([m.gauche, largeur - m.droite])
  );
  const y = $derived(
    scaleLinear()
      .domain([0, Math.max(...points.map((p) => p.y)) * 1.05])
      .nice()
      .range([hauteur - m.bas, m.haut])
  );
  const r = $derived(
    scaleSqrt()
      .domain([0, Math.max(...points.map((p) => p.poids))])
      .range([0, largeur < 480 ? 16 : 26])
  );
  // Les gros disques derrière, les points mis en évidence devant.
  const ordre = $derived(
    [...points].sort((a, b) => Number(!!a.accent) - Number(!!b.accent) || b.poids - a.poids)
  );
  let survol: Point | null = $state(null);
  function bouger(e: PointerEvent) {
    const svg = e.currentTarget as SVGSVGElement;
    const b = svg.getBoundingClientRect();
    const px = ((e.clientX - b.left) / b.width) * largeur;
    const py = ((e.clientY - b.top) / b.height) * hauteur;
    let best: Point | null = null;
    let d = Infinity;
    for (const p of points) {
      const dd = (x(p.x) - px) ** 2 + (y(p.y) - py) ** 2;
      if (dd < d) [d, best] = [dd, p];
    }
    survol = d < 30 ** 2 ? best : null;
  }
</script>

<p class="legende">
  <span><b class="disque"></b>Un pays (aire proportionnelle à sa population)</span>
  {#if paliers.length}<span><b class="palier"></b>{libellePaliers}</span>{/if}
</p>
<div class="graphique" bind:clientWidth={largeur}>
  <svg
    width={largeur}
    height={hauteur}
    viewBox="0 0 {largeur} {hauteur}"
    role="img"
    aria-label={titre}
    onpointermove={bouger}
    onpointerleave={() => (survol = null)}
  >
    {#each y.ticks(5) as t (t)}
      <line class="grille" x1={m.gauche} x2={largeur - m.droite} y1={y(t)} y2={y(t)} />
      <text class="axe" x={m.gauche - 6} y={y(t)} text-anchor="end" dominant-baseline="middle"
        >{yFormat(t)}</text
      >
    {/each}
    {#each xTicks as t (t)}
      <line class="grille" x1={x(t)} x2={x(t)} y1={m.haut} y2={hauteur - m.bas} />
      <text class="axe" x={x(t)} y={hauteur - 10} text-anchor="middle">{xFormat(t)}</text>
    {/each}
    {#each ordre as p (p.id)}
      <circle
        cx={x(p.x)}
        cy={y(p.y)}
        r={Math.max(2.5, r(p.poids))}
        class:accent={p.accent}
        class:survole={survol?.id === p.id}
      />
    {/each}
    {#each paliers as pa, i (i)}
      <line class="palier" x1={x(pa.de)} x2={x(pa.a)} y1={y(pa.y)} y2={y(pa.y)} />
    {/each}
    {#each points.filter((p) => p.accent) as p (p.id)}
      <text class="etiquette" x={x(p.x) + 8} y={y(p.y) - 8}>{p.libelle}</text>
    {/each}
  </svg>
  {#if survol}
    <div
      class="infobulle"
      role="status"
      style:left="{Math.min(x(survol.x), largeur - 220)}px"
      style:top="{y(survol.y) + 14}px"
    >
      {infobulle(survol)}
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
  .grille {
    stroke: var(--reglure);
    stroke-width: 1;
  }
  .axe {
    font-size: 11px;
    fill: var(--ardoise);
    font-variant-numeric: tabular-nums;
  }
  circle {
    fill: var(--serie-1);
    fill-opacity: 0.35;
    stroke: var(--serie-1);
    stroke-width: 1;
  }
  circle.accent {
    fill: var(--repere);
    fill-opacity: 0.9;
    stroke: var(--encre);
  }
  circle.survole {
    stroke: var(--encre);
    stroke-width: 2;
  }
  line.palier {
    stroke: var(--encre);
    stroke-width: 3;
    stroke-linecap: round;
  }
  .etiquette {
    font-size: 12px;
    font-weight: 700;
    fill: var(--encre);
  }
  .legende {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1rem;
    font-size: var(--t-0);
    color: var(--ardoise);
    margin: 0.25rem 0 0.5rem;
  }
  .disque {
    display: inline-block;
    width: 0.8em;
    height: 0.8em;
    border-radius: 50%;
    background: var(--serie-1);
    opacity: 0.6;
    margin-right: 0.35em;
    vertical-align: -0.05em;
  }
  b.palier {
    display: inline-block;
    width: 1.2em;
    height: 3px;
    background: var(--encre);
    margin-right: 0.35em;
    vertical-align: 0.2em;
  }
  .infobulle {
    position: absolute;
    pointer-events: none;
    background: var(--papier);
    border: 1px solid var(--reglure);
    border-radius: 2px;
    padding: 0.2rem 0.5rem;
    font-size: var(--t-0);
    max-width: 220px;
    z-index: 1;
  }
</style>
