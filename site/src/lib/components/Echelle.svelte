<script lang="ts">
  // L'échelle limnimétrique de l'accueil (docs/CONCEPTION.md §2) : la part des immigrés lue comme un
  // niveau d'eau, sur une règle émaillée graduée en « E ». Les plaques marquent des niveaux passés,
  // comme les repères de crue. Les points sont choisis par règle au prérendu (+page.server.ts).
  import { virgule } from '$lib/format';

  interface Point {
    annee: number;
    part: number;
  }
  let { niveau, reperes, legende }: { niveau: Point; reperes: Point[]; legende: string } = $props();

  const H0 = 500;
  const H1 = 20;
  const X = 70;
  const W = 60;
  const MAX = $derived(2 * Math.ceil((niveau.part + 1.5) / 2));
  const y = (p: number) => H0 - (p / MAX) * (H0 - H1);
  const u = $derived((H0 - H1) / MAX);
  const points = $derived(Array.from({ length: MAX }, (_, n) => n));

  // Plaques : de bas en haut, au moins 38 unités d'écart ; un trait relie chaque plaque à son niveau.
  const plaques = $derived.by(() => {
    const tries = [...reperes].sort((a, b) => a.part - b.part);
    let precedent = Infinity;
    return tries.map((r) => {
      const yNiveau = y(r.part);
      const yPlaque = Math.min(yNiveau, precedent - 38);
      precedent = yPlaque;
      return { ...r, yNiveau, yPlaque, actuel: r.annee === niveau.annee };
    });
  });
  const desc = $derived(
    `Échelle graduée de 0 à ${MAX} %. Niveau de ${niveau.annee} : ${virgule(niveau.part, 1)} %. ` +
      reperes
        .filter((r) => r.annee !== niveau.annee)
        .map((r) => `${virgule(r.part, 1)} % en ${r.annee}`)
        .join(', ') +
      '.'
  );
</script>

<figure class="echelle">
  <svg viewBox="0 0 250 520" role="img" aria-labelledby="echelle-titre echelle-desc">
    <title id="echelle-titre">Part des immigrés dans la population</title>
    <desc id="echelle-desc">{desc}</desc>
    <rect class="email" x={X} y={H1} width={W} height={H0 - H1} />
    <rect class="eau" x={X} y={y(niveau.part)} width={W} height={H0 - y(niveau.part)} />
    {#each points as n (n)}
      {@const gauche = n % 2 === 0}
      {@const xs = gauche ? X + 4 : X + W / 2}
      {@const w = W / 2 - 4}
      {#each [0, 1, 2] as k (k)}
        <rect class="grad" x={xs} y={y(n + 0.1 * (2 * k + 1))} width={w} height={u * 0.1} />
      {/each}
      <rect
        class="grad"
        x={gauche ? xs : xs + w - u * 0.1}
        y={y(n + 0.5)}
        width={u * 0.1}
        height={u * 0.5}
      />
      {#if n % 2 === 0}
        <text class="num" x={X - 10} y={y(n) + 6} text-anchor="end">{n === 0 ? '0' : `${n} %`}</text
        >
      {/if}
    {/each}
    <text class="num" x={X - 10} y={y(MAX) + 6} text-anchor="end">{MAX} %</text>
    <line class="ligne-eau" x1={X - 6} x2={X + W + 6} y1={y(niveau.part)} y2={y(niveau.part)} />
    {#each plaques as p (p.annee)}
      <polyline
        class="crue"
        points="{X + W},{p.yNiveau} {X + W + 10},{p.yNiveau} {X + W + 10},{p.yPlaque} {X +
          W +
          16},{p.yPlaque}"
      />
      <rect
        class="plaque"
        class:actuel={p.actuel}
        x={X + W + 16}
        y={p.yPlaque - 15}
        width="84"
        height="34"
        rx="2"
      />
      <text class="plaque-an" x={X + W + 24} y={p.yPlaque}>{p.annee}</text>
      <text class="plaque-val" x={X + W + 24} y={p.yPlaque + 14}>{virgule(p.part, 1)} %</text>
    {/each}
  </svg>
  <figcaption>{legende}</figcaption>
</figure>

<style>
  .echelle {
    margin: 0;
    width: 16rem;
    max-width: 100%;
  }
  svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }
  .email {
    fill: var(--plaque);
    stroke: var(--reglure);
  }
  .grad {
    fill: var(--encre);
  }
  .num {
    fill: var(--encre);
    font-family: var(--titre);
    font-weight: 600;
    font-size: 17px;
    font-variant-numeric: tabular-nums;
  }
  .eau {
    fill: var(--t4);
    opacity: 0.16;
  }
  .ligne-eau {
    stroke: var(--t4);
    stroke-width: 3;
  }
  .crue {
    fill: none;
    stroke: var(--repere);
    stroke-width: 2;
  }
  .plaque {
    fill: var(--plaque);
    stroke: var(--repere);
    stroke-width: 1.5;
  }
  .plaque.actuel {
    stroke: var(--t4);
    stroke-width: 2;
  }
  .plaque-an {
    fill: var(--encre);
    font-family: var(--titre);
    font-weight: 700;
    font-size: 15px;
  }
  .plaque-val {
    fill: var(--ardoise);
    font-family: var(--titre);
    font-weight: 500;
    font-size: 14px;
    font-variant-numeric: tabular-nums;
  }
  figcaption {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin-top: 0.6rem;
    line-height: 1.45;
  }
  @media (prefers-reduced-motion: no-preference) {
    .eau,
    .ligne-eau {
      animation: monter 1.4s cubic-bezier(0.2, 0.7, 0.2, 1) both;
      transform-box: view-box;
      transform-origin: 0 500px;
    }
    @keyframes monter {
      from {
        transform: scaleY(0);
      }
    }
  }
</style>
