<script lang="ts">
  // Frise de la piscine : sous le curseur des années, l'aire empilée des parts d'immigrés,
  // d'enfants et de petits-enfants d'immigrés (le reste de l'eau est implicite), le régime des
  // données (reconstruit, mesuré, partiel) et les années repères. Cliquer ou glisser choisit une
  // année ; le curseur natif reste la commande accessible au clavier.
  import { scaleLinear } from 'd3-scale';
  import { area } from 'd3-shape';
  import { stocks, STATUTS, type AnneePiscine, type Evenement, type Teinte } from '$lib/piscine';
  import { pct } from '$lib/format';

  let {
    annees,
    evenements,
    annee,
    onchoisir
  }: {
    annees: AnneePiscine[];
    evenements: Evenement[];
    annee: number;
    onchoisir: (a: number) => void;
  } = $props();

  let largeur = $state(600);
  const H = 58;
  const BANDE = 7;
  const POUCE = 8; // rayon du curseur natif : aligne l'axe du graphique sur le curseur
  const debut = $derived(annees[0].annee);
  const fin = $derived(annees[annees.length - 1].annee);
  const x = $derived(
    scaleLinear()
      .domain([debut, fin])
      .range([POUCE, largeur - POUCE])
  );

  // Du bas vers le haut : G1, G2 deux parents, G2 un parent, G3.
  const PILE: Teinte[] = [4, 3, 2, 1];
  const parts = $derived(
    annees.map((l) => {
      const s = stocks(l);
      let cumul = 0;
      const bornes = PILE.map((t) => {
        const b = cumul;
        cumul += s[t] / l.population;
        return [b, cumul] as [number, number];
      });
      return { annee: l.annee, bornes, total: cumul };
    })
  );
  const maxi = $derived(Math.ceil((Math.max(...parts.map((p) => p.total)) * 100) / 10) / 10);
  const y = $derived(scaleLinear().domain([0, maxi]).range([H, 4]));
  const aires = $derived(
    PILE.map((t, i) =>
      area<(typeof parts)[number]>()
        .x((p) => x(p.annee))
        .y0((p) => y(p.bornes[i][0]))
        .y1((p) => y(p.bornes[i][1]))(parts)
    )
  );

  // Régimes des flux, en segments contigus.
  const regimes = $derived.by(() => {
    const out: { statut: string; de: number; a: number }[] = [];
    for (const l of annees) {
      const s = l.statut_flux ?? 'reconstruit';
      const d = out[out.length - 1];
      if (d && d.statut === s) d.a = l.annee;
      else out.push({ statut: s, de: l.annee, a: l.annee });
    }
    return out;
  });

  const courant = $derived(parts.find((p) => p.annee === annee));

  let glisse = false;
  function choisir(e: PointerEvent) {
    const r = (e.currentTarget as SVGElement).getBoundingClientRect();
    const a = Math.round(x.invert(e.clientX - r.left));
    onchoisir(Math.max(debut, Math.min(fin, a)));
  }
</script>

<div class="frise" bind:clientWidth={largeur}>
  <svg
    width={largeur}
    height={H + BANDE + 16}
    aria-hidden="true"
    onpointerdown={(e) => {
      glisse = true;
      (e.currentTarget as SVGElement).setPointerCapture(e.pointerId);
      choisir(e);
    }}
    onpointermove={(e) => glisse && choisir(e)}
    onpointerup={() => (glisse = false)}
  >
    <line class="axe" x1={x(debut)} x2={x(fin)} y1={H} y2={H} />
    <line class="axe" x1={x(debut)} x2={x(fin)} y1={y(maxi)} y2={y(maxi)} stroke-dasharray="2 3" />
    <text class="graduation" x={x(debut) + 2} y={y(maxi) + 9}>{pct(maxi * 100)}</text>
    {#each aires as d, i (i)}
      <path {d} fill="var(--t{PILE[i]})" />
    {/each}
    {#each evenements as e (e.annee)}
      <line class="repere" x1={x(e.annee)} x2={x(e.annee)} y1={4} y2={H} />
    {/each}
    {#each regimes as r (r.de)}
      <rect
        class="regime {r.statut}"
        x={x(r.de)}
        y={H + 3}
        width={Math.max(1, x(r.a + 1 > fin ? fin : r.a + 1) - x(r.de) - 1)}
        height={BANDE - 2}
      />
      {#if x(r.a) - x(r.de) > 60}
        <text class="graduation" x={x(r.de) + 2} y={H + BANDE + 12}
          >{STATUTS[r.statut as keyof typeof STATUTS].libelle.toLowerCase()}</text
        >
      {/if}
    {/each}
    <line class="curseur" x1={x(annee)} x2={x(annee)} y1={0} y2={H + BANDE + 1} />
  </svg>
  {#if courant}
    <p class="visually-hidden">
      En {annee}, immigrés, enfants et petits-enfants d’immigrés : {pct(courant.total * 100)} de la population.
    </p>
  {/if}
</div>

<style>
  .frise {
    width: 100%;
  }
  svg {
    display: block;
    cursor: pointer;
    touch-action: none;
  }
  .axe {
    stroke: var(--reglure);
  }
  .repere {
    stroke: var(--papier);
    stroke-width: 1;
    opacity: 0.7;
  }
  .curseur {
    stroke: var(--encre);
    stroke-width: 1.5;
  }
  .graduation {
    font-size: 10px;
    fill: var(--gris);
  }
  .regime {
    fill: var(--bord);
  }
  .regime.reconstruit {
    fill: none;
    stroke: var(--bord);
    stroke-dasharray: 2 2;
  }
  .regime.partiel {
    opacity: 0.45;
  }
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
  }
</style>
