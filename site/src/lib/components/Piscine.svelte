<script lang="ts">
  // La piscine v0 (docs/PISCINE.md §8) : deux teintes, quatre vannes, 1968-2025. Le dessin est en
  // Canvas 2D (des milliers de particules) ; les textes et les commandes sont en HTML par-dessus.
  import { onMount } from 'svelte';
  import { Moteur, SCENE, ETATS } from '$lib/moteur';
  import { STATUTS, CHAMPS, type DonneesPiscine } from '$lib/piscine';
  import { entier, milliers, pct } from '$lib/format';

  let { donnees }: { donnees: DonneesPiscine } = $props();

  const annees = $derived(donnees.annees);
  const debut = $derived(annees[0].annee);
  const fin = $derived(annees[annees.length - 1].annee);

  let canvas: HTMLCanvasElement;
  let cadre: HTMLDivElement;
  let moteur: Moteur | undefined;
  // Valeur initiale seulement : le composant ne reçoit jamais d'autres données.
  // svelte-ignore state_referenced_locally
  let annee = $state(donnees.annees[0].annee);
  let lecture = $state(false);
  let vitesse = $state(1);
  let calme = $state(false);
  // svelte-ignore state_referenced_locally
  let echelle = $state(donnees.echelle);

  const ligne = $derived(annees.find((a) => a.annee === annee)!);
  const statut = $derived(ligne.statut_flux ? STATUTS[ligne.statut_flux] : null);
  const evenement = $derived(donnees.evenements.find((e) => e.annee === annee));
  const reconstruit = $derived(ligne.statut_flux === 'reconstruit');

  function couleurs() {
    const s = getComputedStyle(cadre);
    const c = (n: string) => s.getPropertyValue(n).trim();
    return {
      eau: c('--eau'),
      eauFond: c('--eau-fond'),
      bord: c('--bord'),
      ni: c('--teinte-ni'),
      imm: c('--teinte-imm'),
      ajust: c('--ajustement'),
      encre: c('--encre')
    };
  }

  function dessiner(ctx: CanvasRenderingContext2D, w: number, h: number, horloge: number) {
    if (!moteur) return;
    const k = couleurs();
    const { x0, x1, haut, bas } = SCENE.bassin;
    const niveau = moteur.niveau();
    const surface = bas - (bas - haut) * niveau;
    ctx.clearRect(0, 0, w, h);

    // Bassin et eau.
    ctx.fillStyle = k.eauFond;
    ctx.fillRect(x0 * w, haut * h, (x1 - x0) * w, (bas - haut) * h);
    const vague = (x: number) => surface * h + Math.sin(horloge * 1.2 + x * 18) * 1.4;
    ctx.beginPath();
    ctx.moveTo(x0 * w, bas * h);
    for (let x = x0; x <= x1 + 1e-9; x += 0.01) ctx.lineTo(x * w, vague(x));
    ctx.lineTo(x1 * w, bas * h);
    ctx.closePath();
    ctx.fillStyle = k.eau;
    ctx.fill();
    ctx.strokeStyle = k.bord;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x0 * w, haut * h);
    ctx.lineTo(x0 * w, bas * h);
    ctx.lineTo(x1 * w, bas * h);
    ctx.lineTo(x1 * w, haut * h);
    ctx.stroke();

    // Vannes : deux robinets en haut, deux bondes en bas.
    ctx.lineWidth = 6;
    ctx.lineCap = 'round';
    for (const [nom, o] of Object.entries(SCENE.vannes)) {
      ctx.beginPath();
      if (nom === 'naissances' || nom === 'arrivees') {
        const sens = nom === 'naissances' ? -1 : 1;
        ctx.moveTo((o.x + sens * 0.07) * w, (o.y - 0.03) * h);
        ctx.lineTo(o.x * w, (o.y - 0.03) * h);
        ctx.lineTo(o.x * w, (o.y + 0.02) * h);
      } else {
        ctx.moveTo((o.x + (nom === 'deces' ? 0.03 : -0.03)) * w, bas * h);
        ctx.lineTo(o.x * w, (o.y + 0.005) * h);
      }
      ctx.setLineDash(nom === 'departs' && reconstruit ? [4, 6] : []);
      ctx.strokeStyle = k.bord;
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // Particules, par lots de couleur.
    const r = Math.max(
      1,
      Math.min(
        3.2,
        0.42 * Math.sqrt(((x1 - x0) * w * (bas - haut) * h * 0.85) / moteur.particules.length)
      )
    );
    for (const teinte of [0, 1] as const) {
      ctx.fillStyle = teinte ? k.imm : k.ni;
      ctx.beginPath();
      for (const p of moteur.particules) {
        if (p.teinte !== teinte || p.alpha < 1) continue;
        const [x, y] = p.etat === ETATS.eau ? moteur.position(p, niveau) : [p.x, p.y];
        ctx.moveTo(x * w + r, y * h);
        ctx.arc(x * w, y * h, r, 0, Math.PI * 2);
      }
      ctx.fill();
    }
    // Particules en fondu (entrées par ajustement, sorties), une à une.
    for (const p of moteur.particules) {
      if (p.alpha >= 1) continue;
      const [x, y] = p.etat === ETATS.sort ? [p.x, p.y] : moteur.position(p, niveau);
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.fillStyle = p.teinte ? k.imm : k.ni;
      ctx.beginPath();
      ctx.arc(x * w, y * h, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
      if (p.marque) {
        ctx.strokeStyle = k.ajust;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.arc(x * w, y * h, r + 2.5, 0, Math.PI * 2);
        ctx.stroke();
      }
    }
  }

  onMount(() => {
    const reduit = window.matchMedia('(prefers-reduced-motion: reduce)');
    calme = reduit.matches;
    const demande = Number(new URLSearchParams(location.search).get('annee'));
    if (demande >= debut && demande <= fin) annee = demande;
    // `?lecture` : démarre l'animation (démonstrations, liens partagés).
    if (new URLSearchParams(location.search).has('lecture')) lecture = true;
    const ctx = canvas.getContext('2d')!;
    let w = 0;
    let h = 0;
    const taille = () => {
      const dpr = window.devicePixelRatio || 1;
      w = cadre.clientWidth;
      h = Math.round(w * (w < 600 ? 0.95 : 0.6));
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const e = w < 600 ? donnees.echelle * 2 : donnees.echelle;
      if (!moteur || e !== echelle) {
        echelle = e;
        moteur = new Moteur(annees, e);
        moteur.aller(annee);
      }
    };
    taille();
    const obs = new ResizeObserver(taille);
    obs.observe(cadre);

    let avant = performance.now();
    let image = 0;
    const boucle = (maintenant: number) => {
      const dt = Math.min(0.1, (maintenant - avant) / 1000);
      avant = maintenant;
      if (moteur) {
        if (lecture) {
          moteur.avancer(dt * vitesse * (calme ? 0.8 : 0.5), calme);
          annee = Math.min(fin, Math.floor(moteur.temps));
          if (moteur.temps >= fin) lecture = false;
        }
        moteur.animer(dt, maintenant / 1000, calme);
        dessiner(ctx, w, h, calme ? 0 : maintenant / 1000);
      }
      image = requestAnimationFrame(boucle);
    };
    image = requestAnimationFrame(boucle);
    return () => {
      cancelAnimationFrame(image);
      obs.disconnect();
    };
  });

  function aller(a: number) {
    annee = a;
    moteur?.aller(a);
  }

  function basculer() {
    if (!lecture && annee >= fin) aller(debut);
    lecture = !lecture;
  }

  const valeur = (x: number | null | undefined) => (x == null ? '—' : milliers(x));
  const lectureTexte = $derived(
    `En ${annee}, ${entier(ligne.population)} habitants (${CHAMPS[ligne.champ]}), dont ${entier(ligne.immigres)} immigrés, soit ${pct(ligne.part_immigres)}.`
  );
</script>

<figure class="piscine">
  <div class="compteur" aria-live="polite">
    <span class="annee">{annee}</span>
    <span>{milliers(ligne.population)} habitants</span>
    <span
      ><b class="pastille imm"></b>{milliers(ligne.immigres)} immigrés · {pct(
        ligne.part_immigres
      )}</span
    >
    <span><b class="pastille ni"></b>{milliers(ligne.non_immigres)} non-immigrés</span>
  </div>
  <div class="scene" bind:this={cadre}>
    <div role="img" aria-label={lectureTexte}>
      <canvas bind:this={canvas} aria-hidden="true"></canvas>
    </div>

    <div class="etiquette naissances" style:left="{SCENE.vannes.naissances.x * 100}%">
      <span class="nom">Naissances</span>
      <span class="val">{valeur(ligne.naissances)}</span>
    </div>
    <div class="etiquette arrivees" style:left="{SCENE.vannes.arrivees.x * 100}%">
      <span class="nom">{reconstruit ? 'Solde net (reconstruit)' : 'Arrivées'}</span>
      {#if reconstruit}
        <span class="val"
          ><span class="long">immigrés</span><span class="court">imm.</span>
          {valeur(ligne.net_imm)}</span
        >
        <span class="val"
          ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
          {valeur(ligne.net_ni)}</span
        >
      {:else}
        <span class="val"
          ><span class="long">immigrés</span><span class="court">imm.</span>
          {valeur(ligne.entrees_imm)}</span
        >
        <span class="val"
          ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
          {valeur(ligne.entrees_ni)}</span
        >
      {/if}
    </div>
    <div class="etiquette bas deces">
      <span class="nom">Décès</span>
      <span class="val"
        ><span class="long">immigrés</span><span class="court">imm.</span>
        {valeur(ligne.deces_imm)}{ligne.statut_flux !== 'mesure' && ligne.deces_imm != null
          ? ' (est.)'
          : ''}</span
      >
      <span class="val"
        ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
        {valeur(ligne.deces_ni)}</span
      >
    </div>
    <div class="etiquette bas departs" class:flou={ligne.statut_flux !== 'mesure'}>
      <span class="nom">Départs</span>
      {#if reconstruit}
        <span class="val">compris dans le solde net</span>
      {:else if ligne.statut_flux === 'partiel'}
        <span class="val">pas encore mesurés</span>
      {:else}
        <span class="val"
          ><span class="long">immigrés</span><span class="court">imm.</span>
          {valeur(ligne.sorties_imm)}</span
        >
        <span class="val"
          ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
          {valeur(ligne.sorties_ni)}</span
        >
      {/if}
    </div>
  </div>

  <div class="commandes">
    <button type="button" onclick={basculer} aria-pressed={lecture}>
      {lecture ? 'Pause' : annee >= fin ? 'Revoir' : 'Lecture'}
    </button>
    <label class="frise">
      <span class="visually-hidden">Année</span>
      <input
        type="range"
        min={debut}
        max={fin}
        step="1"
        value={annee}
        oninput={(e) => {
          lecture = false;
          aller(Number((e.target as HTMLInputElement).value));
        }}
        list="reperes"
      />
      <datalist id="reperes">
        {#each donnees.evenements as e (e.annee)}<option value={e.annee}></option>{/each}
      </datalist>
      <span class="bornes"><span>{debut}</span><span>2006</span><span>{fin}</span></span>
    </label>
    <label class="vitesse">
      Vitesse
      <select bind:value={vitesse}>
        <option value={0.5}>lente</option>
        <option value={1}>normale</option>
        <option value={2}>rapide</option>
      </select>
    </label>
  </div>

  <figcaption>
    <p class="regime">
      {#if statut}<span class="badge {ligne.statut_flux}">{statut.libelle}</span>
        {statut.detail}{/if}
      {#if evenement}<strong class="evenement"
          >{evenement.code ? `${evenement.code} · ` : ''}{evenement.libelle}.</strong
        >{/if}
    </p>
    <p class="legende">
      <span><b class="pastille imm"></b>immigrés (nés étrangers à l’étranger)</span>
      <span><b class="pastille ni"></b>non-immigrés</span>
      <span
        ><b class="pastille ajust"></b>ajustement (changement de champ ou de collecte, jamais une
        arrivée)</span
      >
      <span>1 point = {entier(echelle)} personnes</span>
    </p>
    <p class="lecture">Lecture : {lectureTexte}</p>
  </figcaption>
</figure>

<style>
  .piscine {
    margin: 0;
    --eau: #a9c8e0;
    --eau-fond: #eef4f9;
    --bord: #5b6f86;
    --teinte-ni: #e9f2f9;
    --teinte-imm: #1d3f66;
    --ajustement: #8a8f98;
  }
  @media (prefers-color-scheme: dark) {
    .piscine {
      --eau: #23415c;
      --eau-fond: #141c27;
      --bord: #8ea3bb;
      --teinte-ni: #b9d3e8;
      --teinte-imm: #f2c46d;
      --ajustement: #9aa3b5;
    }
  }
  .scene {
    position: relative;
    width: 100%;
  }
  canvas {
    display: block;
    width: 100%;
  }
  .etiquette {
    position: absolute;
    top: 0;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: var(--t-0);
    line-height: 1.25;
    color: var(--ardoise);
    pointer-events: none;
    text-align: center;
    white-space: nowrap;
  }
  .etiquette.naissances {
    transform: translateX(-70%);
  }
  .etiquette.arrivees {
    transform: translateX(-30%);
  }
  .etiquette.bas {
    top: auto;
    bottom: -2.6rem;
    transform: none;
  }
  .deces {
    left: 0;
    align-items: flex-start;
  }
  .departs {
    right: 0;
    align-items: flex-end;
  }
  .flou {
    opacity: 0.6;
    font-style: italic;
  }
  .nom {
    font-weight: 600;
    color: var(--encre);
  }
  .val {
    font-variant-numeric: tabular-nums;
  }
  .compteur {
    position: absolute;
    left: 50%;
    top: 0;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: var(--t-0);
    color: var(--ardoise);
    font-variant-numeric: tabular-nums;
    pointer-events: none;
  }
  .compteur .annee {
    font-size: var(--t-4);
    font-weight: 700;
    color: var(--encre);
    line-height: 1;
  }
  .pastille {
    display: inline-block;
    width: 0.7em;
    height: 0.7em;
    border-radius: 50%;
    margin-right: 0.35em;
    vertical-align: -0.05em;
    border: 1px solid var(--bord);
  }
  .pastille.imm {
    background: var(--teinte-imm);
  }
  .pastille.ni {
    background: var(--teinte-ni);
  }
  .pastille.ajust {
    background: transparent;
    border: 1.5px solid var(--ajustement);
  }
  .commandes {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 3.4rem;
    flex-wrap: wrap;
  }
  .commandes button {
    font: inherit;
    font-weight: 600;
    padding: 0.4rem 1.1rem;
    border-radius: 999px;
    border: 1.5px solid var(--encre);
    background: var(--encre);
    color: var(--papier);
    cursor: pointer;
    min-width: 6.5rem;
  }
  .frise {
    flex: 1 1 16rem;
    display: flex;
    flex-direction: column;
  }
  .frise input {
    width: 100%;
    accent-color: var(--teinte-imm);
  }
  .bornes {
    display: flex;
    justify-content: space-between;
    font-size: var(--t-0);
    color: var(--gris);
  }
  .vitesse {
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .vitesse select {
    font: inherit;
  }
  figcaption {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin-top: 0.75rem;
  }
  figcaption p {
    margin: 0.4rem 0;
  }
  .regime {
    min-height: 2.6em;
  }
  .badge {
    display: inline-block;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.05rem 0.45rem;
    border-radius: 0.25rem;
    border: 1px solid currentColor;
  }
  .badge.reconstruit {
    border-style: dashed;
  }
  .evenement {
    display: block;
    color: var(--encre);
    font-weight: 600;
  }
  .legende {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.2rem;
  }
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
  }
  .piscine {
    position: relative;
  }
  .court {
    display: none;
  }
  @media (max-width: 599px) {
    .compteur {
      position: static;
      transform: none;
      flex-direction: row;
      flex-wrap: wrap;
      align-items: baseline;
      gap: 0.1rem 0.8rem;
      margin-bottom: 0.4rem;
    }
    .scene {
      padding-top: 2.6rem;
    }
    .etiquette.arrivees {
      left: auto !important;
      right: 0;
      transform: none;
      align-items: flex-end;
    }
    .long {
      display: none;
    }
    .court {
      display: inline;
    }
  }
</style>
