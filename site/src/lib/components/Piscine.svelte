<script lang="ts">
  // La piscine (docs/PISCINE.md) : cinq teintes (G1, G2 deux parents, G2 un parent, G3, autres),
  // quatre vannes dont l'épaisseur suit le débit de l'année, et deux états de l'eau : décantée
  // (les teintes en couches, non miscibles, pour lire les volumes) ou mélangée. Dessin Canvas 2D ;
  // textes et commandes en HTML par-dessus.
  import { onMount } from 'svelte';
  import { Moteur, SCENE, ETATS } from '$lib/moteur';
  import {
    STATUTS,
    CHAMPS,
    GENERATIONS,
    TEINTES,
    stocks,
    naissancesParTeinte,
    decesParTeinte,
    type DonneesPiscine,
    type AnneePiscine,
    type Teinte
  } from '$lib/piscine';
  import { entier, milliers, pct } from '$lib/format';

  let { donnees }: { donnees: DonneesPiscine } = $props();

  const annees = $derived(donnees.annees);
  const debut = $derived(annees[0].annee);
  const fin = $derived(annees[annees.length - 1].annee);

  let canvas: HTMLCanvasElement;
  let cadre: HTMLDivElement;
  let moteur: Moteur | undefined;
  // Valeurs initiales seulement : le composant ne reçoit jamais d'autres données.
  // svelte-ignore state_referenced_locally
  let annee = $state(donnees.annees[0].annee);
  let lecture = $state(false);
  let vitesse = $state(1);
  let calme = $state(false);
  let decante = $state(true);
  // svelte-ignore state_referenced_locally
  let echelle = $state(donnees.echelle);

  const ligne = $derived(annees.find((a) => a.annee === annee)!);
  const statut = $derived(ligne.statut_flux ? STATUTS[ligne.statut_flux] : null);
  const evenement = $derived(donnees.evenements.find((e) => e.annee === annee));
  const reconstruit = $derived(ligne.statut_flux === 'reconstruit');
  const st = $derived(stocks(ligne));
  const generations = $derived(ligne.g2a !== undefined);

  /** Débits de l'année, par vanne et par teinte (pour l'épaisseur des tuyaux). */
  function debits(l: AnneePiscine) {
    const vide = (): Record<Teinte, number> => ({ 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 });
    const arr = vide();
    const dep = vide();
    const pos = (x: number | null | undefined) => Math.max(0, x ?? 0);
    const neg = (x: number | null | undefined) => Math.max(0, -(x ?? 0));
    if (l.statut_flux === 'reconstruit') {
      arr[4] = pos(l.net_imm);
      arr[0] = pos(l.net_ni);
      dep[4] = neg(l.net_imm);
      dep[0] = neg(l.net_ni);
    } else {
      arr[4] = pos(l.entrees_imm);
      arr[0] = pos(l.entrees_ni);
      dep[4] = pos(l.sorties_imm);
      dep[0] = pos(l.sorties_ni);
    }
    return {
      naissances: naissancesParTeinte(l),
      arrivees: arr,
      deces: decesParTeinte(l),
      departs: dep
    };
  }
  const somme = (r: Record<Teinte, number>) => TEINTES.reduce<number>((s, t) => s + r[t], 0);
  const debitMax = $derived(
    Math.max(
      ...annees.flatMap((l) => {
        const d = debits(l);
        return [somme(d.naissances), somme(d.arrivees), somme(d.deces), somme(d.departs)];
      })
    )
  );

  function couleurs() {
    const s = getComputedStyle(cadre);
    const c = (n: string) => s.getPropertyValue(n).trim();
    return {
      eau: c('--eau'),
      bord: c('--bord'),
      encre: c('--encre'),
      ajust: c('--ajustement'),
      teinte: [c('--t0'), c('--t1'), c('--t2'), c('--t3'), c('--t4')]
    };
  }

  /** Tuyau d'épaisseur proportionnelle au débit, en bandes par teinte. */
  function tuyau(
    ctx: CanvasRenderingContext2D,
    k: ReturnType<typeof couleurs>,
    r: Record<Teinte, number>,
    x: number,
    y0: number,
    y1: number,
    largeurMax: number,
    inconnu = false
  ) {
    const total = somme(r);
    const w = (total / debitMax) * largeurMax;
    if (inconnu) {
      ctx.setLineDash([3, 4]);
      ctx.strokeStyle = k.bord;
      ctx.lineWidth = 1.5;
      ctx.strokeRect(x - 6, y0, 12, y1 - y0);
      ctx.setLineDash([]);
      return;
    }
    if (w < 0.5) return;
    let gauche = x - w / 2;
    for (const t of [4, 3, 2, 1, 0] as Teinte[]) {
      const lw = (r[t] / total) * w;
      if (lw <= 0) continue;
      ctx.fillStyle = k.teinte[t];
      ctx.fillRect(gauche, y0, lw, y1 - y0);
      gauche += lw;
    }
    ctx.strokeStyle = k.bord;
    ctx.lineWidth = 1;
    ctx.strokeRect(x - w / 2, y0, w, y1 - y0);
  }

  function dessiner(ctx: CanvasRenderingContext2D, w: number, h: number, horloge: number) {
    if (!moteur) return;
    const k = couleurs();
    const { x0, x1, haut, bas } = SCENE.bassin;
    const niveau = moteur.niveau();
    const surface = bas - (bas - haut) * niveau;
    const l = moteur.ligne(Math.min(fin, Math.floor(moteur.temps)))!;
    const d = debits(l);
    ctx.clearRect(0, 0, w, h);

    // Eau.
    const agite = calme ? 0 : 1 - moteur.decante;
    const vague = (x: number) => surface * h + Math.sin(horloge * 1.2 + x * 18) * 1.4 * agite;
    ctx.beginPath();
    ctx.moveTo(x0 * w, bas * h);
    for (let x = x0; x <= x1 + 1e-9; x += 0.01) ctx.lineTo(x * w, vague(x));
    ctx.lineTo(x1 * w, bas * h);
    ctx.closePath();
    ctx.fillStyle = k.eau;
    ctx.fill();

    // Couches de l'eau décantée : une bande pâle par teinte.
    const dec = moteur.decante;
    const hauteur = (bas - surface) * h;
    if (dec > 0.01) {
      ctx.globalAlpha = 0.35 * dec;
      for (const t of TEINTES) {
        const [lo, hi] = moteur.bornes[t];
        if (hi - lo <= 0) continue;
        ctx.fillStyle = k.teinte[t];
        ctx.fillRect(x0 * w, bas * h - hi * hauteur, (x1 - x0) * w, (hi - lo) * hauteur);
      }
      ctx.globalAlpha = 1;
    }

    // Tuyaux : épaisseur ∝ débit de l'année, même échelle pour les quatre vannes.
    const lmax = 0.085 * w;
    const yRobinet = SCENE.vannes.naissances.y * h;
    tuyau(ctx, k, d.naissances, SCENE.vannes.naissances.x * w, yRobinet, surface * h, lmax);
    tuyau(ctx, k, d.arrivees, SCENE.vannes.arrivees.x * w, yRobinet, surface * h, lmax);
    tuyau(ctx, k, d.deces, SCENE.vannes.deces.x * w, bas * h, h, lmax);
    tuyau(
      ctx,
      k,
      d.departs,
      SCENE.vannes.departs.x * w,
      bas * h,
      h,
      lmax,
      l.statut_flux === 'partiel'
    );

    // Bassin.
    ctx.strokeStyle = k.bord;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x0 * w, haut * h);
    ctx.lineTo(x0 * w, bas * h);
    ctx.lineTo(x1 * w, bas * h);
    ctx.lineTo(x1 * w, haut * h);
    ctx.stroke();

    // Particules, par lots de couleur.
    const r = Math.max(
      1,
      Math.min(
        3.2,
        0.42 * Math.sqrt(((x1 - x0) * w * (bas - haut) * h * 0.85) / moteur.particules.length)
      )
    );
    for (const teinte of TEINTES) {
      ctx.fillStyle = k.teinte[teinte];
      ctx.beginPath();
      for (const p of moteur.particules) {
        if (p.teinte !== teinte || p.alpha < 1) continue;
        const [x, y] = p.etat === ETATS.eau ? moteur.position(p, niveau) : [p.x, p.y];
        ctx.moveTo(x * w + r, y * h);
        ctx.arc(x * w, y * h, r, 0, Math.PI * 2);
      }
      ctx.fill();
    }
    for (const p of moteur.particules) {
      if (p.alpha >= 1) continue;
      const [x, y] = p.etat === ETATS.sort ? [p.x, p.y] : moteur.position(p, niveau);
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.fillStyle = k.teinte[p.teinte];
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

    // Étiquettes des couches (eau décantée), dans le bassin à droite.
    if (dec > 0.5) {
      ctx.font = `600 ${w < 600 ? 10 : 12}px Lexend, system-ui, sans-serif`;
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.globalAlpha = (dec - 0.5) * 2;
      for (const t of TEINTES) {
        const [lo, hi] = moteur.bornes[t];
        if ((hi - lo) * hauteur < 15) continue;
        const y = bas * h - ((lo + hi) / 2) * hauteur;
        const texte = `${GENERATIONS[t].court} · ${pct(100 * (hi - lo))}`;
        const lx = (x1 - 0.012) * w;
        const tw = ctx.measureText(texte).width;
        ctx.fillStyle = k.eau;
        ctx.beginPath();
        ctx.roundRect(lx - tw - 6, y - 8, tw + 12, 16, 8);
        ctx.fill();
        ctx.fillStyle = k.encre;
        ctx.fillText(texte, lx, y);
      }
      ctx.globalAlpha = 1;
    }
  }

  onMount(() => {
    const reduit = window.matchMedia('(prefers-reduced-motion: reduce)');
    calme = reduit.matches;
    const params = new URLSearchParams(location.search);
    const demande = Number(params.get('annee'));
    if (demande >= debut && demande <= fin) annee = demande;
    // `?lecture` : démarre l'animation ; `?melange` : eau mélangée (démonstrations, liens partagés).
    if (params.has('lecture')) lecture = true;
    if (params.has('melange')) decante = false;
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
        moteur.decante = moteur.decanteCible = decante ? 1 : 0;
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
        moteur.decanteCible = decante ? 1 : 0;
        if (lecture) {
          moteur.avancer(dt * vitesse * (calme ? 0.8 : 0.5), calme);
          annee = Math.min(fin, Math.floor(moteur.temps));
          if (moteur.temps >= fin) lecture = false;
        }
        moteur.animer(dt, maintenant / 1000, calme);
        dessiner(ctx, w, h, maintenant / 1000);
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
    `En ${annee}, ${entier(ligne.population)} habitants (${CHAMPS[ligne.champ]}), dont ${entier(ligne.immigres)} immigrés, soit ${pct(ligne.part_immigres)}` +
      (generations
        ? `, environ ${milliers(st[3] + st[2])} enfants d’immigrés et ${milliers(st[1])} petits-enfants d’immigrés (modèle).`
        : '.')
  );
  const LIGNES: Teinte[] = [4, 3, 2, 1, 0];
</script>

<figure class="piscine">
  <div class="compteur" aria-live="polite">
    <span class="annee">{annee}</span>
    <span>{milliers(ligne.population)} habitants</span>
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
      <span class="val"
        ><span class="long">immigrés</span><span class="court">imm.</span>
        {valeur(reconstruit ? ligne.net_imm : ligne.entrees_imm)}</span
      >
      <span class="val"
        ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
        {valeur(reconstruit ? ligne.net_ni : ligne.entrees_ni)}</span
      >
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
    <button type="button" class="principal" onclick={basculer} aria-pressed={lecture}>
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
    <div class="bascule" role="group" aria-label="État de l’eau">
      <button type="button" aria-pressed={decante} onclick={() => (decante = true)}>Décantée</button
      >
      <button type="button" aria-pressed={!decante} onclick={() => (decante = false)}
        >Mélangée</button
      >
    </div>
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
    <table class="composition">
      <caption class="visually-hidden">Composition de la population en {annee}</caption>
      <tbody>
        {#each LIGNES as t (t)}
          {#if generations || t === 4 || t === 0}
            <tr>
              <th scope="row"
                ><b class="pastille" style:background="var(--t{t})"></b>{generations || t === 4
                  ? GENERATIONS[t].libelle
                  : 'Non-immigrés'}</th
              >
              <td>{milliers(st[t])}</td>
              <td>{pct((100 * st[t]) / ligne.population)}</td>
            </tr>
          {/if}
        {/each}
      </tbody>
    </table>
    <p class="regime">
      {#if statut}<span class="badge {ligne.statut_flux}">{statut.libelle}</span>
        {statut.detail}{/if}
      {#if generations}
        <span class="badge modele">Modèle</span> G2 et G3 : modèle de cohortes calé sur l’état civil
        et l’enquête Insee de 2019-2020 (IP 1910), pas une observation annuelle.
        {#if annee < 1968}Avant 1968, ils dépendent aussi d’une hypothèse sur les enfants d’immigrés
          vivants en 1911 : des ordres de grandeur seulement.{/if}
      {/if}
      {#if evenement}<strong class="evenement"
          >{evenement.code ? `${evenement.code} · ` : ''}{evenement.libelle}.</strong
        >{/if}
    </p>
    <p class="legende">
      <span>Épaisseur des tuyaux : débit de l’année, à la même échelle pour les quatre vannes.</span
      >
      <span><b class="pastille ajust"></b>ajustement (champ ou collecte, jamais une arrivée)</span>
      <span>1 point = {entier(echelle)} personnes</span>
    </p>
    <p class="lecture">Lecture : {lectureTexte}</p>
  </figcaption>
</figure>

<style>
  .piscine {
    margin: 0;
    position: relative;
    --eau: #eef3f8;
    --bord: #5b6f86;
    --ajustement: #8a8f98;
    --t0: #c9d3de;
    --t1: #6da7ec;
    --t2: #3987e5;
    --t3: #1c5cab;
    --t4: #0d366b;
  }
  @media (prefers-color-scheme: dark) {
    .piscine {
      --eau: #1b2a3a;
      --bord: #8ea3bb;
      --ajustement: #9aa3b5;
      --t0: #4a5a6c;
      --t1: #2a78d6;
      --t2: #5598e7;
      --t3: #86b6ef;
      --t4: #cde2fb;
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
    display: flex;
    flex-direction: column;
    font-size: var(--t-0);
    line-height: 1.25;
    color: var(--ardoise);
    pointer-events: none;
    white-space: nowrap;
  }
  .etiquette.naissances {
    transform: translateX(calc(-100% - 3.2rem));
    align-items: flex-end;
    text-align: right;
  }
  .etiquette.arrivees {
    transform: translateX(3.2rem);
    align-items: flex-start;
  }
  .etiquette.bas {
    top: auto;
    bottom: -2.6rem;
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
    z-index: 1;
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
    width: 0.75em;
    height: 0.75em;
    border-radius: 50%;
    margin-right: 0.45em;
    vertical-align: -0.05em;
  }
  .pastille.ajust {
    background: transparent;
    border: 1.5px solid var(--ajustement);
  }
  .commandes {
    display: flex;
    align-items: center;
    gap: 0.75rem 1rem;
    margin-top: 3.4rem;
    flex-wrap: wrap;
  }
  .commandes button {
    font: inherit;
    font-size: var(--t-0);
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    border: 1.5px solid var(--encre);
    background: transparent;
    color: var(--encre);
    cursor: pointer;
  }
  .commandes button.principal,
  .commandes button[aria-pressed='true']:not(.principal) {
    background: var(--encre);
    color: var(--papier);
  }
  .commandes button.principal {
    font-size: var(--t-1);
    font-weight: 600;
    min-width: 6.5rem;
  }
  .bascule {
    display: flex;
    gap: 0.3rem;
  }
  .frise {
    flex: 1 1 14rem;
    display: flex;
    flex-direction: column;
  }
  .frise input {
    width: 100%;
    accent-color: var(--t3);
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
  .composition {
    border-collapse: collapse;
    font-variant-numeric: tabular-nums;
    margin: 0.5rem 0;
  }
  .composition th {
    text-align: left;
    font-weight: 400;
    padding: 0.1rem 1rem 0.1rem 0;
    color: var(--encre);
  }
  .composition td {
    text-align: right;
    padding: 0.1rem 0 0.1rem 1rem;
  }
  .regime {
    min-height: 2.6em;
  }
  .badge {
    display: inline-block;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.05rem 0.45rem;
    border-radius: 0.25rem;
    border: 1px solid currentColor;
  }
  .badge.reconstruit,
  .badge.modele {
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
  .court {
    display: none;
  }
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
  }
  @media (max-width: 599px) {
    .compteur {
      position: static;
      transform: none;
      flex-direction: row;
      align-items: baseline;
      gap: 0.8rem;
      margin-bottom: 0.4rem;
    }
    .scene {
      padding-top: 2.6rem;
    }
    .etiquette.naissances {
      left: 0 !important;
      transform: none;
      align-items: flex-start;
      text-align: left;
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
