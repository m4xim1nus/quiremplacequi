<script lang="ts">
  // Petits multiples : une courbe par facette, même axe horizontal et même échelle verticale pour
  // toutes (comparaison honnête des hauteurs). Le pic de chaque facette est étiqueté ; infobulle
  // au survol.
  import { scaleLinear } from 'd3-scale';
  import { line, area } from 'd3-shape';

  interface Point {
    x: number;
    y: number;
  }
  interface Facette {
    titre: string;
    points: Point[];
  }

  let {
    facettes,
    yFormat,
    xDomaine,
    yMax,
    couleur = 'var(--serie-1)',
    xTicks
  }: {
    facettes: Facette[];
    yFormat: (y: number) => string;
    xDomaine: [number, number];
    yMax: number;
    couleur?: string;
    xTicks: number[];
  } = $props();

  let largeurGrille = $state(640);
  const colonnes = $derived(largeurGrille < 480 ? 2 : largeurGrille < 760 ? 3 : 4);
  const w = $derived(Math.floor((largeurGrille - (colonnes - 1) * 16) / colonnes));
  const h = 120;
  const m = { haut: 18, droite: 8, bas: 18, gauche: 8 };
  const x = $derived(
    scaleLinear()
      .domain(xDomaine)
      .range([m.gauche, w - m.droite])
  );
  const y = $derived(
    scaleLinear()
      .domain([0, yMax])
      .range([h - m.bas, m.haut])
  );
  const trait = $derived(
    line<Point>()
      .x((p) => x(p.x))
      .y((p) => y(p.y))
  );
  const lavis = $derived(
    area<Point>()
      .x((p) => x(p.x))
      .y0(y(0))
      .y1((p) => y(p.y))
  );

  let survol: { f: number; p: Point } | null = $state(null);
  function bouger(e: PointerEvent, f: number) {
    const r = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
    const v = x.invert(((e.clientX - r.left) / r.width) * w);
    const pts = facettes[f].points;
    const p = pts.reduce((a, b) => (Math.abs(b.x - v) < Math.abs(a.x - v) ? b : a), pts[0]);
    survol = { f, p };
  }
  const pic = (pts: Point[]) => pts.reduce((a, b) => (b.y > a.y ? b : a), pts[0]);
</script>

<div class="grille" bind:clientWidth={largeurGrille} style:--colonnes={colonnes}>
  {#each facettes as f, i (f.titre)}
    {@const sommet = pic(f.points)}
    <figure class="facette">
      <figcaption>{f.titre}</figcaption>
      <svg
        width={w}
        height={h}
        viewBox="0 0 {w} {h}"
        role="img"
        aria-label="{f.titre} : maximum {yFormat(sommet.y)} en {sommet.x}"
        onpointermove={(e) => bouger(e, i)}
        onpointerleave={() => (survol = null)}
      >
        <line class="base" x1={m.gauche} x2={w - m.droite} y1={y(0)} y2={y(0)} />
        {#each xTicks as t (t)}
          <text class="axe" x={x(t)} y={h - 4} text-anchor="middle">{t}</text>
        {/each}
        <path d={lavis(f.points)} style:fill={couleur} opacity="0.1" />
        <path
          d={trait(f.points)}
          fill="none"
          style:stroke={couleur}
          stroke-width="2"
          class="trait"
        />
        <circle cx={x(sommet.x)} cy={y(sommet.y)} r="4" style:fill={couleur} class="marqueur" />
        <text
          class="valeur"
          x={Math.min(Math.max(x(sommet.x), 24), w - 24)}
          y={y(sommet.y) - 8}
          text-anchor="middle">{yFormat(sommet.y)} ({sommet.x})</text
        >
        {#if survol && survol.f === i}
          <line class="curseur" x1={x(survol.p.x)} x2={x(survol.p.x)} y1={m.haut} y2={y(0)} />
          <circle
            cx={x(survol.p.x)}
            cy={y(survol.p.y)}
            r="5"
            style:fill={couleur}
            class="marqueur"
          />
        {/if}
      </svg>
      {#if survol && survol.f === i}
        <div class="infobulle" role="status">
          {survol.p.x} : <strong>{yFormat(survol.p.y)}</strong>
        </div>
      {/if}
    </figure>
  {/each}
</div>

<style>
  .grille {
    display: grid;
    grid-template-columns: repeat(var(--colonnes), minmax(0, 1fr));
    gap: 0.75rem 16px;
  }
  .facette {
    margin: 0;
    position: relative;
    min-width: 0;
  }
  figcaption {
    font-size: var(--t-0);
    font-weight: 600;
    color: var(--encre);
  }
  svg {
    display: block;
    overflow: visible;
    touch-action: pan-y;
  }
  .base {
    stroke: var(--reglure);
  }
  .axe {
    font-size: 10px;
    fill: var(--gris);
  }
  .valeur {
    font-size: 10.5px;
    fill: var(--ardoise);
    font-variant-numeric: tabular-nums;
  }
  .trait {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
  .marqueur {
    stroke: var(--papier);
    stroke-width: 2;
  }
  .curseur {
    stroke: var(--gris);
  }
  .infobulle {
    position: absolute;
    top: 1.2rem;
    right: 0;
    pointer-events: none;
    background: var(--papier);
    border: 1px solid var(--reglure);
    border-radius: 2px;
    padding: 0.15rem 0.45rem;
    font-size: var(--t-0);
    font-variant-numeric: tabular-nums;
  }
</style>
