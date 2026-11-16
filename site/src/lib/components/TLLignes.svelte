<script lang="ts">
  // Courbes (une ou plusieurs séries) sur un axe horizontal numérique, une seule échelle verticale.
  // Les segments d'une série ne sont pas reliés entre eux (rupture de série). Repères verticaux
  // (changement de champ, rupture), infobulle au survol, marqueurs aux points observés.
  import { scaleLinear } from 'd3-scale';
  import { line, area } from 'd3-shape';

  interface Point {
    x: number;
    y: number;
    etiquette?: string;
  }
  interface Serie {
    id: string;
    libelle: string;
    couleur: string;
    segments: Point[][];
  }
  interface Repere {
    x: number;
    libelle: string;
    style: 'rupture' | 'champ';
  }

  let {
    series,
    reperes = [],
    yFormat,
    xFormat = (x: number) => String(x),
    xTicks,
    yMax,
    hauteur = 300,
    marqueurs = false,
    aire = false,
    titre,
    infobulle
  }: {
    series: Serie[];
    reperes?: Repere[];
    yFormat: (y: number) => string;
    xFormat?: (x: number) => string;
    xTicks?: number[];
    yMax?: number;
    hauteur?: number;
    marqueurs?: boolean;
    aire?: boolean;
    titre: string;
    infobulle?: (x: number) => string;
  } = $props();

  let largeur = $state(640);
  const m = $derived({ haut: 16, droite: largeur < 480 ? 12 : 72, bas: 28, gauche: 52 });
  const tous = $derived(series.flatMap((s) => s.segments.flat()));
  const xs = $derived(tous.map((p) => p.x));
  const x = $derived(
    scaleLinear()
      .domain([Math.min(...xs), Math.max(...xs)])
      .range([m.gauche, largeur - m.droite])
  );
  const y = $derived(
    scaleLinear()
      .domain([
        Math.min(0, ...tous.map((p) => p.y * 1.08)),
        yMax ?? Math.max(0, ...tous.map((p) => p.y)) * 1.08
      ])
      .nice()
      .range([hauteur - m.bas, m.haut])
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
  const graduationsX = $derived(xTicks ?? x.ticks(largeur < 480 ? 4 : 8));
  const graduationsY = $derived(y.ticks(5));

  // Étiquettes de fin de série écartées verticalement (12 px au moins) pour ne pas se chevaucher.
  const etiquettesFin = $derived.by(() => {
    const e = series.map((s) => {
      const der = s.segments.at(-1)!.at(-1)!;
      return { id: s.id, libelle: s.libelle, x: x(der.x), y: y(der.y) };
    });
    e.sort((a, b) => a.y - b.y);
    for (let i = 1; i < e.length; i++) if (e[i].y - e[i - 1].y < 12) e[i].y = e[i - 1].y + 12;
    return e;
  });

  // Repères : leurs libellés descendent d'un cran quand ils sont trop proches du précédent.
  const reperesPlaces = $derived.by(() => {
    const r = [...reperes].sort((a, b) => a.x - b.x);
    let precedent = -Infinity;
    let cran = 0;
    return r.map((d) => {
      const px = x(d.x);
      cran = px - precedent < 80 ? cran + 1 : 0;
      precedent = px;
      return { ...d, px, dy: cran * 12 };
    });
  });

  let survol: number | null = $state(null);
  const xsUniques = $derived([...new Set(xs)].sort((a, b) => a - b));
  function bouger(e: PointerEvent) {
    const svg = e.currentTarget as SVGSVGElement;
    const r = svg.getBoundingClientRect();
    const px = ((e.clientX - r.left) / r.width) * largeur;
    const v = x.invert(px);
    survol = xsUniques.reduce((a, b) => (Math.abs(b - v) < Math.abs(a - v) ? b : a));
  }
  const pointsSurvol = $derived(
    survol === null
      ? []
      : series
          .map((s) => ({ s, p: s.segments.flat().find((p) => p.x === survol) }))
          .filter((d) => d.p)
  );
</script>

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
    {#each graduationsY as t (t)}
      <line class="grille" x1={m.gauche} x2={largeur - m.droite} y1={y(t)} y2={y(t)} />
      <text class="axe" x={m.gauche - 6} y={y(t)} text-anchor="end" dominant-baseline="middle"
        >{yFormat(t)}</text
      >
    {/each}
    {#each graduationsX as t (t)}
      <text class="axe" x={x(t)} y={hauteur - 8} text-anchor="middle">{xFormat(t)}</text>
    {/each}
    {#each reperesPlaces as r (r.x + r.libelle)}
      <line class="repere {r.style}" x1={r.px} x2={r.px} y1={m.haut} y2={hauteur - m.bas} />
      <text
        class="repere-texte"
        x={r.px + 4 > largeur - 60 ? r.px - 4 : r.px + 4}
        text-anchor={r.px + 4 > largeur - 60 ? 'end' : 'start'}
        y={m.haut + 8 + r.dy}>{r.libelle}</text
      >
    {/each}
    {#each series as s (s.id)}
      {#each s.segments as seg, i (i)}
        {#if aire}
          <path d={lavis(seg)} style:fill={s.couleur} opacity="0.1" />
        {/if}
        <path d={trait(seg)} fill="none" style:stroke={s.couleur} stroke-width="2" class="trait" />
        {#if marqueurs}
          {#each seg as p (p.x)}
            <circle cx={x(p.x)} cy={y(p.y)} r="3" style:fill={s.couleur} class="marqueur" />
          {/each}
        {/if}
      {/each}
    {/each}
    {#if series.length > 1 && largeur >= 480}
      {#each etiquettesFin as e (e.id)}
        <text class="etiquette" x={e.x + 8} y={e.y} dominant-baseline="middle">{e.libelle}</text>
      {/each}
    {/if}
    {#if survol !== null}
      <line class="curseur" x1={x(survol)} x2={x(survol)} y1={m.haut} y2={hauteur - m.bas} />
      {#each pointsSurvol as d (d.s.id)}
        <circle cx={x(d.p!.x)} cy={y(d.p!.y)} r="5" style:fill={d.s.couleur} class="marqueur" />
      {/each}
    {/if}
  </svg>
  {#if survol !== null}
    <div
      class="infobulle"
      style:left="{Math.min(x(survol), largeur - 170)}px"
      style:top="{m.haut}px"
      role="status"
    >
      <strong>{xFormat(survol)}</strong>
      {#if infobulle}
        <span>{infobulle(survol)}</span>
      {:else}
        {#each pointsSurvol as d (d.s.id)}
          <span
            ><b class="pastille" style:background={d.s.couleur}></b>{series.length > 1
              ? `${d.s.libelle} : `
              : ''}{d.p!.etiquette ?? yFormat(d.p!.y)}</span
          >
        {/each}
      {/if}
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
    touch-action: pan-y;
  }
  .grille {
    stroke: var(--reglure);
    stroke-width: 1;
  }
  .axe,
  .repere-texte,
  .etiquette {
    font-size: 11px;
    fill: var(--gris);
    font-variant-numeric: tabular-nums;
  }
  .etiquette {
    fill: var(--ardoise);
    font-weight: 600;
  }
  .trait {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
  .marqueur {
    stroke: var(--papier);
    stroke-width: 2;
  }
  .repere {
    stroke: var(--ardoise);
    stroke-width: 1;
  }
  .repere.champ {
    stroke-dasharray: 2 3;
    stroke: var(--gris);
  }
  .curseur {
    stroke: var(--gris);
    stroke-width: 1;
  }
  .infobulle {
    position: absolute;
    pointer-events: none;
    background: var(--papier);
    border: 1px solid var(--reglure);
    border-radius: 2px;
    padding: 0.35rem 0.55rem;
    font-size: var(--t-0);
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
    min-width: 9rem;
    max-width: 14rem;
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.08);
    transform: translateX(8px);
  }
  .pastille {
    display: inline-block;
    width: 0.7em;
    height: 0.7em;
    border-radius: 50%;
    margin-right: 0.35em;
  }
</style>
