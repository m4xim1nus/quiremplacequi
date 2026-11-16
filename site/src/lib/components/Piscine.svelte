<script lang="ts">
  // La piscine (docs/PISCINE.md) : cinq teintes (G1, G2 deux parents, G2 un parent, G3, autres).
  // De haut en bas : deux robinets versent par des rubans d'épaisseur proportionnelle au débit de
  // l'année ; l'eau est décantée (une colonne par teinte, de largeur proportionnelle à l'effectif)
  // ou mélangée ; chaque colonne se vide par le fond vers deux bondes. Dessin Canvas 2D ; textes
  // et commandes en HTML par-dessus.
  import { onMount } from 'svelte';
  import {
    Moteur,
    SCENE,
    geometrie,
    surRuban,
    type Particule,
    type Ruban,
    type Vannes
  } from '$lib/moteur';
  import PiscineFrise from './PiscineFrise.svelte';
  import {
    STATUTS,
    CHAMPS,
    GENERATIONS,
    TEINTES,
    stocks,
    debits,
    somme,
    cumuls,
    partNesAvant,
    fourchette,
    type DonneesPiscine,
    type Teinte
  } from '$lib/piscine';
  import { entier, milliers, millions, pct } from '$lib/format';

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
  let suivre = $state(false);
  // svelte-ignore state_referenced_locally
  let origine = $state(donnees.annees[0].annee);
  const nesAvant = $derived(
    donnees.nes_avant ? partNesAvant(donnees.nes_avant, origine, annee) : null
  );
  // svelte-ignore state_referenced_locally
  let echelle = $state(donnees.echelle);
  let hauteur = $state(0);
  let etroit = $state(false);

  const ligne = $derived(annees.find((a) => a.annee === annee)!);
  const statut = $derived(ligne.statut_flux ? STATUTS[ligne.statut_flux] : null);
  const evenement = $derived(donnees.evenements.find((e) => e.annee === annee));
  const reconstruit = $derived(ligne.statut_flux === 'reconstruit');
  const st = $derived(stocks(ligne));
  const generations = $derived(ligne.g2a !== undefined);
  const cumul = $derived(cumuls(annees, origine, annee));

  function couleurs() {
    const s = getComputedStyle(cadre);
    const c = (n: string) => s.getPropertyValue(n).trim();
    return {
      eau: c('--eau'),
      bord: c('--bord'),
      encre: c('--encre'),
      papier: c('--papier'),
      ajust: c('--ajustement'),
      teinte: [c('--t0'), c('--t1'), c('--t2'), c('--t3'), c('--t4')]
    };
  }

  /** Un ruban : une bande courbe, de largeur constante, entre une vanne et une colonne. */
  function ruban(ctx: CanvasRenderingContext2D, r: Ruban, w: number, h: number) {
    const ym = ((r.ya + r.yb) / 2) * h;
    const g = (x: number) => (x - r.largeur / 2) * w;
    const d = (x: number) => (x + r.largeur / 2) * w;
    ctx.beginPath();
    ctx.moveTo(g(r.xa), r.ya * h);
    ctx.bezierCurveTo(g(r.xa), ym, g(r.xb), ym, g(r.xb), r.yb * h);
    ctx.lineTo(d(r.xb), r.yb * h);
    ctx.bezierCurveTo(d(r.xb), ym, d(r.xa), ym, d(r.xa), r.ya * h);
    ctx.closePath();
  }

  /** Tuyau droit d'un robinet ou d'une bonde, en bandes par teinte. */
  function tuyau(
    ctx: CanvasRenderingContext2D,
    k: ReturnType<typeof couleurs>,
    rubans: Ruban[],
    vanne: keyof Vannes,
    w: number,
    h: number,
    pointille: boolean
  ) {
    const { x, y0, y1 } = moteur!.vannes[vanne];
    const rs = rubans.filter((r) => r.vanne === vanne);
    const total = rs.reduce((s, r) => s + r.largeur, 0);
    if (total * w < 0.5) {
      ctx.setLineDash([3, 4]);
      ctx.strokeStyle = k.bord;
      ctx.lineWidth = 1.2;
      ctx.strokeRect(x * w - 5, y0 * h, 10, (y1 - y0) * h);
      ctx.setLineDash([]);
      return;
    }
    for (const r of rs) {
      const xr = vanne === 'naissances' || vanne === 'arrivees' ? r.xa : r.xb;
      ctx.fillStyle = k.teinte[r.teinte];
      ctx.fillRect((xr - r.largeur / 2) * w, y0 * h, r.largeur * w, (y1 - y0) * h);
    }
    ctx.strokeStyle = k.bord;
    ctx.lineWidth = 1;
    if (pointille) ctx.setLineDash([3, 3]);
    ctx.strokeRect((x - total / 2) * w, y0 * h, total * w, (y1 - y0) * h);
    ctx.setLineDash([]);
  }

  function dessiner(ctx: CanvasRenderingContext2D, w: number, h: number, horloge: number) {
    if (!moteur) return;
    const k = couleurs();
    const { x0, x1, haut, bas } = SCENE.bassin;
    const niveau = moteur.niveau();
    const surface = moteur.surface(niveau);
    const l = moteur.ligne(Math.min(fin, Math.floor(moteur.temps)))!;
    const net = l.statut_flux === 'reconstruit';
    const partiel = l.statut_flux === 'partiel';
    const rubans = moteur.rubans;
    ctx.clearRect(0, 0, w, h);

    // Rubans : pâles, avec un contour ; pointillés quand le débit n'est pas un flux brut mesuré
    // (solde net avant 2006, sorties pas encore publiées).
    for (const r of rubans) {
      const douteux =
        (net && (r.vanne === 'arrivees' || r.vanne === 'departs')) ||
        (partiel && r.vanne === 'departs');
      ruban(ctx, r, w, h);
      ctx.globalAlpha = douteux ? 0.3 : 0.6;
      ctx.fillStyle = k.teinte[r.teinte];
      ctx.fill();
      ctx.globalAlpha = douteux ? 0.9 : 0.35;
      if (douteux) ctx.setLineDash([3, 3]);
      ctx.strokeStyle = k.bord;
      ctx.lineWidth = 0.8;
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    }
    tuyau(ctx, k, rubans, 'naissances', w, h, false);
    tuyau(ctx, k, rubans, 'arrivees', w, h, net);
    tuyau(ctx, k, rubans, 'deces', w, h, false);
    tuyau(ctx, k, rubans, 'departs', w, h, net || partiel);

    // Eau.
    const agite = calme ? 0 : 1;
    const vague = (x: number) => surface * h + Math.sin(horloge * 1.2 + x * 18) * 1.2 * agite;
    ctx.beginPath();
    ctx.moveTo(x0 * w, bas * h);
    for (let x = x0; x <= x1 + 1e-9; x += 0.01) ctx.lineTo(x * w, vague(x));
    ctx.lineTo(x1 * w, bas * h);
    ctx.closePath();
    ctx.fillStyle = k.eau;
    ctx.fill();

    // Colonnes de l'eau décantée : un fond pâle par teinte, séparées par un trait fin.
    const dec = moteur.decante;
    const larg = (x1 - x0) * w;
    if (dec > 0.01) {
      for (const t of TEINTES) {
        const [lo, hi] = moteur.bornes[t];
        if (hi - lo <= 0) continue;
        ctx.globalAlpha = 0.3 * dec;
        ctx.fillStyle = k.teinte[t];
        ctx.fillRect(x0 * w + lo * larg, surface * h, (hi - lo) * larg, (bas - surface) * h);
        ctx.globalAlpha = dec;
        if (lo > 0) {
          ctx.strokeStyle = k.papier;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(x0 * w + lo * larg, surface * h + 2);
          ctx.lineTo(x0 * w + lo * larg, bas * h);
          ctx.stroke();
        }
      }
      ctx.globalAlpha = 1;
    }

    // Bassin, ouvert au fond sous chaque bouche de sortie.
    ctx.strokeStyle = k.bord;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x0 * w, haut * h);
    ctx.lineTo(x0 * w, bas * h);
    ctx.lineTo(x1 * w, bas * h);
    ctx.lineTo(x1 * w, haut * h);
    ctx.stroke();

    // Particules, par lots de couleur.
    const n = moteur.particules.length;
    const rayon = Math.max(
      1,
      Math.min(2.8, 0.42 * Math.sqrt(((x1 - x0) * w * (bas - haut) * h * 0.8) / n))
    );
    // Suivre l'eau d'une année : l'eau de départ en encre, les entrées depuis dans leur teinte, pâles.
    const pale = suivre ? 0.35 : 1;
    const lot = (couleur: string, alpha: number, garder: (p: Particule) => boolean) => {
      ctx.fillStyle = couleur;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      for (const p of moteur!.particules) {
        if (p.alpha < 1 || !garder(p)) continue;
        const [x, y] = moteur!.position(p, niveau);
        ctx.moveTo(x * w + rayon, y * h);
        ctx.arc(x * w, y * h, rayon, 0, Math.PI * 2);
      }
      ctx.fill();
    };
    for (const teinte of TEINTES)
      lot(k.teinte[teinte], pale, (p) => p.teinte === teinte && !(suivre && p.origine));
    if (suivre) lot(k.encre, 0.8, (p) => p.origine);
    ctx.globalAlpha = 1;
    for (const p of moteur.particules) {
      if (p.alpha >= 1) continue;
      const [x, y] = moteur.position(p, niveau);
      ctx.globalAlpha = Math.max(0, p.alpha) * (suivre && !p.origine ? pale : 1);
      ctx.fillStyle = suivre && p.origine ? k.encre : k.teinte[p.teinte];
      ctx.beginPath();
      ctx.arc(x * w, y * h, rayon, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
      if (p.marque) {
        ctx.strokeStyle = k.ajust;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.arc(x * w, y * h, rayon + 2.5, 0, Math.PI * 2);
        ctx.stroke();
      }
    }

    // Étiquettes des colonnes (eau décantée) : couchées dans les colonnes étroites.
    if (dec > 0.5) {
      const taille = w < 600 ? 10 : 12;
      ctx.font = `600 ${taille}px Lexend, system-ui, sans-serif`;
      ctx.textBaseline = 'middle';
      ctx.globalAlpha = (dec - 0.5) * 2;
      for (const t of TEINTES) {
        const [lo, hi] = moteur.bornes[t];
        const cw = (hi - lo) * larg;
        if (cw < taille + 4) continue;
        const texte = `${GENERATIONS[t].court} · ${pct(100 * (hi - lo))}`;
        const tw = ctx.measureText(texte).width;
        const cx = x0 * w + ((lo + hi) / 2) * larg;
        const fond = bas * h - 8;
        ctx.save();
        if (cw > tw + 16) {
          ctx.translate(cx, fond - 8);
          ctx.textAlign = 'center';
        } else if ((bas - surface) * h > tw + 24) {
          ctx.translate(cx, fond);
          ctx.rotate(-Math.PI / 2);
          ctx.textAlign = 'left';
        } else {
          ctx.restore();
          continue;
        }
        const bx = ctx.textAlign === 'center' ? -tw / 2 - 6 : -6;
        ctx.fillStyle = k.eau;
        ctx.beginPath();
        ctx.roundRect(bx, -8, tw + 12, 16, 8);
        ctx.fill();
        ctx.fillStyle = k.encre;
        ctx.fillText(texte, 0, 0);
        ctx.restore();
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
      // Toute la scène (robinets, bassin, bondes) tient dans l'écran.
      const ideal = w * (w < 600 ? 1.3 : 0.6);
      h = Math.round(Math.max(340, Math.min(ideal, window.innerHeight * 0.7)));
      hauteur = h;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const e = w < 600 ? donnees.echelle * 2 : donnees.echelle;
      if (!moteur || e !== echelle || etroit !== w < 600) {
        echelle = e;
        etroit = w < 600;
        moteur = new Moteur(annees, e, etroit, donnees.nes_avant);
        moteur.decante = moteur.decanteCible = decante ? 1 : 0;
        moteur.aller(annee);
        origine = annee;
      }
    };
    taille();
    const obs = new ResizeObserver(taille);
    obs.observe(cadre);
    window.addEventListener('resize', taille);

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
      window.removeEventListener('resize', taille);
    };
  });

  function aller(a: number) {
    annee = a;
    origine = a;
    moteur?.aller(a);
  }

  function basculer() {
    if (!lecture && annee >= fin) aller(debut);
    lecture = !lecture;
  }

  const valeur = (x: number | null | undefined) => (x == null ? '—' : milliers(x));
  const d = $derived(debits(ligne));
  const lectureTexte = $derived(
    `En ${annee}, ${entier(ligne.population)} habitants (${CHAMPS[ligne.champ]}), dont ${entier(ligne.immigres)} immigrés, soit ${pct(ligne.part_immigres)}` +
      (generations
        ? `, environ ${milliers(st[3] + st[2])} enfants d’immigrés et ${milliers(st[1])} petits-enfants d’immigrés (modèle).`
        : '.') +
      ` Dans l’année : ${milliers(somme(d.naissances))} naissances, ${milliers(somme(d.deces))} décès.`
  );
  const LIGNES: Teinte[] = [4, 3, 2, 1, 0];

  // Survol : une colonne (effectif, part) ou un ruban (débit de l'année).
  const NOMS_VANNES = {
    naissances: 'Naissances',
    arrivees: 'Arrivées',
    deces: 'Décès',
    departs: 'Départs'
  } as const;
  let bulle = $state<{
    x: number;
    y: number;
    gauche?: boolean;
    titre: string;
    texte: string;
    note?: string;
  } | null>(null);
  function survoler(e: PointerEvent) {
    if (!moteur) return;
    const r = cadre.getBoundingClientRect();
    const px = e.clientX - r.left;
    const py = e.clientY - r.top;
    const u = px / r.width;
    const v = py / r.height;
    const w = r.width;
    const h = r.height;
    // Rubans : distance à la ligne médiane, échantillonnée.
    for (const rb of moteur.rubans) {
      for (let i = 0; i <= 24; i++) {
        const [x, y] = surRuban(rb, i / 24);
        if (Math.abs(y * h - py) < 6 && Math.abs(x * w - px) < (rb.largeur * w) / 2 + 3) {
          const net = reconstruit && (rb.vanne === 'arrivees' || rb.vanne === 'departs');
          bulle = {
            x: px,
            gauche: px > w * 0.6,
            y: py,
            titre: `${NOMS_VANNES[rb.vanne]}${net ? ' (solde net)' : ''} · ${GENERATIONS[rb.teinte].court}`,
            texte: `${milliers(d[rb.vanne][rb.teinte])} en ${annee}`
          };
          return;
        }
      }
    }
    const { x0, x1, bas } = SCENE.bassin;
    if (u >= x0 && u <= x1 && v <= bas && v >= moteur.surface()) {
      const f = (u - x0) / (x1 - x0);
      const t = decante
        ? TEINTES.find((t) => f >= moteur!.bornes[t][0] && f < moteur!.bornes[t][1])
        : undefined;
      bulle =
        t === undefined
          ? {
              x: px,
              gauche: px > w * 0.6,
              y: py,
              titre: `${milliers(ligne.population)} habitants`,
              texte: `au 1er janvier ${annee}`
            }
          : {
              x: px,
              gauche: px > w * 0.6,
              y: py,
              titre: GENERATIONS[t].libelle,
              texte: `${milliers(st[t])} au 1er janvier ${annee}, soit ${pct((100 * st[t]) / ligne.population)}${t > 0 && t < 4 ? ' (modèle)' : ''}`,
              note: (() => {
                const f = fourchette(ligne, t);
                return f
                  ? `De ${pct(f[0])} à ${pct(f[1])} selon l’hypothèse de départ du modèle (U20).`
                  : undefined;
              })()
            };
      return;
    }
    bulle = null;
  }

  const pos = (v: keyof Vannes) => geometrie(etroit)[v].x * 100;
</script>

<figure class="piscine">
  <div class="compteur" aria-live="polite">
    <span class="annee">{annee}</span>
    <span>{milliers(ligne.population)} habitants</span>
    {#if suivre && nesAvant != null && annee > origine}
      <span class="restant"
        >nés avant {origine} : <strong>{pct(100 * nesAvant)}</strong> des habitants</span
      >
    {/if}
    {#if evenement}<span class="repere-court">{evenement.libelle.split(' :')[0]}</span>{/if}
  </div>
  <div
    class="scene"
    role="presentation"
    bind:this={cadre}
    style:--h="{hauteur}px"
    onpointermove={survoler}
    onpointerleave={() => (bulle = null)}
  >
    {#if bulle}
      <div
        class="bulle"
        class:gauche={bulle.gauche}
        style:left="{bulle.x}px"
        style:top="{bulle.y}px"
        aria-hidden="true"
      >
        <strong>{bulle.titre}</strong>
        <span>{bulle.texte}</span>
        {#if bulle.note}<span class="note">{bulle.note}</span>{/if}
      </div>
    {/if}
    <div role="img" aria-label={lectureTexte}>
      <canvas bind:this={canvas} aria-hidden="true"></canvas>
    </div>

    <div class="etiquette haut gauche" style:left="{pos('naissances')}%">
      <span class="nom">Naissances</span>
      <span class="val">{valeur(ligne.naissances)}</span>
    </div>
    <div class="etiquette haut droite" style:left="{pos('arrivees')}%">
      <span class="nom">{reconstruit ? 'Solde migratoire' : 'Arrivées'}</span>
      {#if reconstruit}<span class="val note">net, reconstruit</span>{/if}
      <span class="val"
        ><span class="long">immigrés</span><span class="court">imm.</span>
        {valeur(reconstruit ? ligne.net_imm : ligne.entrees_imm)}</span
      >
      <span class="val"
        ><span class="long">non-immigrés</span><span class="court">non-imm.</span>
        {valeur(reconstruit ? ligne.net_ni : ligne.entrees_ni)}{reconstruit
          ? ' (par diff.)'
          : ''}</span
      >
    </div>
    <div class="etiquette bas gauche" style:left="{pos('deces')}%">
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
    <div
      class="etiquette bas droite"
      class:flou={ligne.statut_flux !== 'mesure'}
      style:left="{pos('departs')}%"
    >
      <span class="nom">Départs</span>
      {#if reconstruit}
        <span class="val">compris dans le solde</span>
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
    <div class="frise">
      <PiscineFrise
        {annees}
        evenements={donnees.evenements}
        {annee}
        onchoisir={(a) => {
          lecture = false;
          aller(a);
        }}
      />
      <label>
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
      </label>
      <datalist id="reperes">
        {#each donnees.evenements as e (e.annee)}<option value={e.annee}></option>{/each}
      </datalist>
      <span class="bornes"><span>{debut}</span><span>{fin}</span></span>
    </div>
    <div class="reglages">
      {#if donnees.nes_avant}
        <button
          type="button"
          class="suivre"
          aria-pressed={suivre}
          onclick={() => (suivre = !suivre)}
          title="Les habitants présents en {origine} restent en couleur ; ceux arrivés ou nés depuis pâlissent."
          >Suivre l’eau de {origine}</button
        >
      {/if}
      <div class="bascule" role="group" aria-label="État de l’eau">
        <button type="button" aria-pressed={decante} onclick={() => (decante = true)}
          >Décantée</button
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
  </div>

  <figcaption>
    <p class="cumul">
      {#if annee > origine}
        De {origine} à {annee}, <strong>{millions(cumul.naissances)}</strong> de naissances et
        <strong>{millions(cumul.deces)}</strong> de décès sont passés par les vannes, pour un solde
        migratoire de <strong>{millions(cumul.migration, true)}</strong>.
      {:else}
        Lancez la lecture : les compteurs cumulent les naissances, les décès et le solde migratoire
        depuis {origine}.
      {/if}
    </p>
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
        >{#if evenement.source}
          <span class="source-evenement">Source : {evenement.source}.</span>{/if}{/if}
    </p>
    <p class="legende">
      <span
        >Largeur des colonnes : effectif. Épaisseur des rubans : débit de l’année, à la même échelle
        pour les quatre vannes.</span
      >
      <span><b class="pastille pointille"></b>pointillés : solde net ou flux pas encore mesuré</span
      >
      <span><b class="pastille ajust"></b>ajustement (champ ou collecte, jamais une arrivée)</span>
      <span>1 point = {entier(echelle)} personnes</span>
      {#if suivre}
        <span
          ><b class="pastille" style:background="var(--encre)"></b>les habitants de {origine} encore là.
          Leur nombre suit la part des habitants nés avant {origine} (pyramides des âges, Insee), qui
          compte aussi les immigrés nés avant {origine} et arrivés depuis.</span
        >
      {/if}
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
  }
  @media (prefers-color-scheme: dark) {
    .piscine {
      --eau: #1b2a3a;
      --bord: #8ea3bb;
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
    display: flex;
    flex-direction: column;
    font-size: var(--t-0);
    line-height: 1.25;
    color: var(--ardoise);
    pointer-events: none;
    white-space: nowrap;
  }
  .etiquette.haut {
    top: 0;
  }
  .etiquette.bas {
    bottom: 0;
  }
  .etiquette.gauche {
    transform: translateX(calc(-100% - 3rem));
    align-items: flex-end;
    text-align: right;
  }
  .etiquette.droite {
    transform: translateX(3rem);
    align-items: flex-start;
  }
  .bulle {
    position: absolute;
    z-index: 2;
    transform: translate(12px, -50%);
    display: flex;
    flex-direction: column;
    width: max-content;
    max-width: 16rem;
    padding: 0.35rem 0.6rem;
    border-radius: 0.4rem;
    background: var(--papier);
    border: 1px solid var(--bord);
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.15);
    font-size: var(--t-0);
    color: var(--ardoise);
    pointer-events: none;
  }
  .bulle.gauche {
    transform: translate(calc(-100% - 12px), -50%);
  }
  .bulle strong {
    color: var(--encre);
  }
  .bulle .note {
    margin-top: 0.2rem;
    font-style: italic;
  }
  .flou {
    opacity: 0.65;
    font-style: italic;
  }
  .nom {
    font-weight: 600;
    color: var(--encre);
  }
  .val {
    font-variant-numeric: tabular-nums;
  }
  .note {
    font-style: italic;
  }
  .compteur {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.2rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: var(--t-0);
    color: var(--ardoise);
    font-variant-numeric: tabular-nums;
  }
  .compteur .annee {
    font-size: var(--t-4);
    font-weight: 700;
    color: var(--encre);
    line-height: 1;
  }
  .restant strong {
    color: var(--encre);
  }
  .repere-court {
    font-weight: 600;
    color: var(--encre);
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
  .pastille.pointille {
    background: transparent;
    border-radius: 2px;
    border: 1.5px dashed var(--bord);
  }
  .commandes {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: start;
    gap: 0.5rem 1rem;
    margin-top: 0.75rem;
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
    margin-top: 1.4rem;
  }
  .reglages {
    grid-column: 2;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem 1rem;
  }
  .bascule {
    display: flex;
    gap: 0.3rem;
  }
  .frise {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }
  .frise input {
    width: 100%;
    margin: 0;
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
  .cumul {
    font-size: var(--t-1);
    color: var(--encre);
    min-height: 3em;
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
  .source-evenement {
    font-size: 0.85em;
    color: var(--ardoise);
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
    .etiquette.gauche {
      left: 0 !important;
      transform: none;
      align-items: flex-start;
      text-align: left;
    }
    .etiquette.droite {
      left: auto !important;
      right: 0;
      transform: none;
      align-items: flex-end;
      text-align: right;
    }
    .long {
      display: none;
    }
    .court {
      display: inline;
    }
    .commandes {
      grid-template-columns: 1fr;
    }
    .commandes button.principal {
      margin-top: 0;
      justify-self: start;
    }
    .reglages {
      grid-column: 1;
    }
  }
</style>
