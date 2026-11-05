<script lang="ts">
  // F2 : le curseur de définition. Chaque cran ajoute un groupe à « ceux que l'on compte » ; le
  // chiffre et la barre se recalculent. La barre montre aussi ce qui reste hors du compte.
  import type { Palier } from '$lib/generations';
  import { pc } from '$lib/generations';

  let {
    paliers,
    couleurs,
    champ
  }: { paliers: Palier[]; couleurs: Record<string, string>; champ: string } = $props();

  let cran = $state(0);
  const courant = $derived(paliers[cran]);
  const rapport = $derived(courant.cumul / paliers[0].cumul);
</script>

<div class="curseur">
  <div class="chiffre" aria-live="polite">
    <span class="grand">{pc(courant.cumul)}</span>
    <span class="sous"
      >de la population ({champ}){#if cran > 0}, soit {rapport.toFixed(1).replace('.', ',')} fois le nombre
        d’immigrés{/if}</span
    >
  </div>

  <div
    class="barre"
    role="img"
    aria-label="{pc(courant.cumul)} comptés, {pc(100 - courant.cumul)} hors du compte"
  >
    {#each paliers as p, i (p.cle)}
      <span
        class="seg"
        class:hors={i > cran}
        class:deduit={p.deduit}
        style:width="{p.ajout}%"
        style:background={couleurs[p.cle]}
        title="{p.libelle} : {pc(p.ajout)}{p.deduit ? ' (déduit)' : ''}"
      ></span>
    {/each}
    <span class="seg reste" style:width="{100 - paliers[paliers.length - 1].cumul}%"></span>
  </div>

  <fieldset>
    <legend>Qui compte-t-on ?</legend>
    {#each paliers as p, i (p.cle)}
      <label class:actif={i <= cran}>
        <input type="radio" name="cran" value={i} bind:group={cran} />
        <span class="cle" style:background={couleurs[p.cle]} class:deduit={p.deduit}></span>
        <span class="lib">{i === 0 ? '' : '+ '}{p.libelle}</span>
        <span class="aj">{i === 0 ? '' : '+'}{pc(p.ajout)}{p.deduit ? ' (déduit)' : ''}</span>
        <span class="cu">= {pc(p.cumul)}</span>
      </label>
    {/each}
  </fieldset>
</div>

<style>
  .curseur {
    margin: 1rem 0;
  }
  .chiffre {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.25rem 0.75rem;
  }
  .grand {
    font-size: var(--t-5);
    font-weight: 700;
    color: var(--encre);
    font-variant-numeric: tabular-nums;
    min-width: 5ch;
  }
  .sous {
    color: var(--ardoise);
    font-size: var(--t-0);
  }
  .barre {
    display: flex;
    gap: 2px;
    height: 1.6rem;
    margin: 0.75rem 0 1rem;
  }
  .seg {
    border-radius: 2px;
    transition: opacity 0.3s;
  }
  .seg:first-child {
    border-radius: 4px 2px 2px 4px;
  }
  .seg.hors {
    opacity: 0.18;
  }
  .seg.deduit,
  .cle.deduit {
    background-image: repeating-linear-gradient(
      45deg,
      transparent 0 3px,
      rgb(255 255 255 / 45%) 3px 5px
    ) !important;
  }
  .seg.reste {
    background: var(--reglure);
    border-radius: 2px 4px 4px 2px;
  }
  fieldset {
    border: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 0.2rem;
  }
  legend {
    font-weight: 600;
    font-size: var(--t-0);
    margin-bottom: 0.35rem;
  }
  label {
    display: grid;
    grid-template-columns: auto auto 1fr auto auto;
    align-items: center;
    gap: 0.5rem;
    font-size: var(--t-0);
    color: var(--gris);
    cursor: pointer;
    padding: 0.15rem 0.3rem;
    border-radius: 4px;
  }
  label.actif {
    color: var(--encre);
  }
  label:has(input:focus-visible) {
    outline: 2px solid var(--lien);
  }
  input {
    margin: 0;
    accent-color: var(--encre);
  }
  .cle {
    width: 0.8em;
    height: 0.8em;
    border-radius: 2px;
  }
  .aj,
  .cu {
    font-variant-numeric: tabular-nums;
    text-align: right;
  }
  .cu {
    min-width: 4.5rem;
    font-weight: 600;
  }
  @media (max-width: 599px) {
    label {
      grid-template-columns: auto auto 1fr auto;
    }
    .aj {
      display: none;
    }
  }
</style>
