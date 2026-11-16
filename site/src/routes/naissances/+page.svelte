<script lang="ts">
  import TLCadre from '$lib/components/TLCadre.svelte';
  import TLLignes from '$lib/components/TLLignes.svelte';
  import TLBarres from '$lib/components/TLBarres.svelte';
  import Sommaire from '$lib/components/Sommaire.svelte';
  import Detail from '$lib/components/Detail.svelte';
  import { entier, milliers, millions, pct, virgule } from '$lib/format';

  let { data } = $props();
  const c = $derived(data.chiffres);
  const ans = $derived(data.annees);
  const v2 = (x: number) => virgule(x, 2);
  const minuscule = (s: string) => s.charAt(0).toLowerCase() + s.slice(1);
  /** « enfant » au singulier en dessous de 2 (règle de l'Insee : « 1,56 enfant par femme »). */
  const enfants = (x: number) => (x < 2 ? 'enfant' : 'enfants');

  // 1. Naissances selon le pays de naissance des parents : trois catégories qui font le total.
  let mesure: 'nombre' | 'part' = $state('nombre');
  const RUPTURE = 2011;
  const avantRupture = $derived(ans.find((a) => a.annee === RUPTURE - 1)!);
  const apresRupture = $derived(ans.find((a) => a.annee === RUPTURE)!);
  const segments = (f: (a: (typeof ans)[number]) => number) => {
    const pts = ans.map((a) => ({
      x: a.annee,
      y: mesure === 'nombre' ? f(a) : (100 * f(a)) / a.ensemble
    }));
    return [pts.filter((p) => p.x < RUPTURE), pts.filter((p) => p.x >= RUPTURE)];
  };
  const serieParents = $derived([
    {
      id: 'france',
      libelle: 'Deux parents nés en France',
      couleur: 'var(--cat-5)',
      segments: segments((a) => a.deuxNesFrance)
    },
    {
      id: 'un',
      libelle: 'Un parent né à l’étranger',
      couleur: 'var(--cat-2)',
      segments: segments((a) => a.unParent)
    },
    {
      id: 'deux',
      libelle: 'Deux parents nés à l’étranger',
      couleur: 'var(--serie-1)',
      segments: segments((a) => a.deuxParents)
    }
  ]);
  const infobulleParents = (x: number) => {
    const a = ans.find((v) => v.annee === x)!;
    const p = (n: number) => pct((100 * n) / a.ensemble);
    return `${entier(a.ensemble)} naissances : deux parents nés en France ${p(a.deuxNesFrance)}, un parent né à l’étranger ${p(a.unParent)}, deux parents nés à l’étranger ${p(a.deuxParents)} · mère née à l’étranger ${p(a.mereEtranger)}`;
  };
  // Part de deux parents nés à l'étranger si leur nombre n'avait pas changé depuis 2014.
  const partSansHausse = $derived(
    (100 * c.base.deuxParents) / (c.dernier.ensemble - c.variation.deuxParents)
  );
  const partDeuxBase = $derived((100 * c.base.deuxParents) / c.base.ensemble);

  // 2. ICF ajusté selon le lieu de naissance.
  const serieIcf = $derived(
    (
      [
        ['nees_a_l_etranger', 'Nées à l’étranger', 'var(--serie-1)'],
        ['ensemble', 'Ensemble des femmes', 'var(--encre)'],
        ['nees_en_france', 'Nées en France', 'var(--cat-2)']
      ] as const
    ).map(([g, libelle, couleur]) => ({
      id: g,
      libelle,
      couleur,
      segments: [data.icf[g].map((p) => ({ x: p.annee, y: p.icf, etiquette: v2(p.icf) }))]
    }))
  );
  const etrMin = $derived(Math.min(...data.icf.nees_a_l_etranger.map((p) => p.icf)));
  const etrMax = $derived(Math.max(...data.icf.nees_a_l_etranger.map((p) => p.icf)));

  // 3. ICF national depuis 1901 et seuil de remplacement (métropole, seule série aussi longue).
  const metro = $derived(data.nationale.filter((x) => x.champ === 'metropole'));
  const serieNationale = $derived([
    {
      id: 'icf',
      libelle: 'Indicateur conjoncturel',
      couleur: 'var(--serie-1)',
      segments: [metro.map((x) => ({ x: x.annee, y: x.icf, etiquette: v2(x.icf) }))]
    },
    {
      id: 'seuil',
      libelle: 'Seuil de remplacement',
      couleur: 'var(--repere)',
      segments: [metro.map((x) => ({ x: x.annee, y: x.seuil, etiquette: v2(x.seuil) }))]
    }
  ]);

  // 4. Calendrier des naissances autour de l'arrivée.
  const serieArrivee = $derived([
    {
      id: 'france',
      libelle: 'En France',
      couleur: 'var(--serie-1)',
      segments: [data.arrivee.map((x) => ({ x: x.duree, y: x.enFrance }))]
    },
    {
      id: 'etranger',
      libelle: 'À l’étranger',
      couleur: 'var(--cat-2)',
      segments: [data.arrivee.map((x) => ({ x: x.duree, y: x.aLEtranger }))]
    }
  ]);
  const duree = (x: number) =>
    x === 0 ? 'arrivée' : `${x > 0 ? '+' : '−'}${Math.abs(x)} an${Math.abs(x) > 1 ? 's' : ''}`;

  // 5. Descendance finale par génération (TeO).
  const tranche = (debut: number) => `${debut}-${String(debut + 4).slice(2)}`;
  const periode = (debut: number) => `${debut} à ${debut + 4}`;
  const serieGenerations = $derived([
    {
      id: 'imm',
      libelle: 'Immigrées',
      couleur: 'var(--serie-1)',
      segments: [c.genImmigrees.map((g) => ({ x: g.debut, y: g.valeur, etiquette: v2(g.valeur) }))]
    },
    {
      id: 'non',
      libelle: 'Non-immigrées',
      couleur: 'var(--cat-2)',
      segments: [
        c.genNonImmigrees.map((g) => ({ x: g.debut, y: g.valeur, etiquette: v2(g.valeur) }))
      ]
    }
  ]);
  const genPremiere = $derived(c.genImmigrees[0]);
  const genDerniere = $derived(c.genImmigrees.at(-1)!);
  const genNonPremiere = $derived(c.genNonImmigrees[0]);
  const genNonDerniere = $derived(c.genNonImmigrees.at(-1)!);
  const diplome = (cat: string, groupe: string) =>
    data.df.find((x) => x.dimension === 'diplome' && x.categorie === cat && x.groupe === groupe)!
      .valeur;
  const ecartDes = $derived(c.lien.descendantes - c.lien.ni);
  const procheDes = $derived(Math.abs(ecartDes) < 0.1);
  const commeNi = $derived(
    !procheDes
      ? ', contre'
      : ecartDes > 0
        ? ', à peine plus que'
        : ecartDes < 0
          ? ', à peine moins que'
          : ', autant que'
  );

  // 6. ONU 2000.
  const o = $derived(c.onu);
  const parAn = (s: Record<string, number>) => s.migrants_par_an * 1000;
  // Solde observé (métropole) rapporté au scénario IV : même ordre de grandeur à ± 15 %.
  const comparaisonIV = $derived.by(() => {
    const r = c.onu.soldeMoyen / parAn(c.onu.IV);
    const iv = `${milliers(parAn(c.onu.IV))} par an en moyenne`;
    if (r > 1.15) return `plus que le scénario IV (${iv})`;
    if (r < 0.85) return `moins que le scénario IV (${iv})`;
    return `du même ordre que le scénario IV (${iv})`;
  });
  const citation = (cle: string) => data.onu.citations.find((x) => x.cle === cle)!;

  const SOMMAIRE = $derived([
    {
      ancre: 'parents',
      question: 'De quels parents naissent les enfants ?',
      chiffre: pct(c.partsDernier.mere),
      reponse: `des enfants nés en ${c.dernier.annee} avaient une mère née à l’étranger, ${pct(c.partsDernier.auMoinsUn)} au moins un parent né à l’étranger, ${pct(c.partsDernier.deux)} deux parents nés à l’étranger.`
    },
    {
      ancre: 'fecondite',
      question: 'Les femmes nées à l’étranger ont-elles plus d’enfants ?',
      chiffre: v2(c.icf.etranger),
      reponse: `${enfants(c.icf.etranger)} par femme en ${c.icf.annee}, contre ${v2(c.icf.france)} pour les femmes nées en France.`
    },
    {
      ancre: 'poids',
      question: 'Que changent-elles à la fécondité de la France ?',
      chiffre: `+${v2(c.contributionAjustee)} à +${v2(c.contribution)}`,
      reponse: `enfant par femme selon le calcul (${v2(c.icf.france)} sans elles en ${c.icf.annee}), soit ${virgule(c.contributionAjusteeRel, 0)} à ${virgule(c.contributionRel, 0)} % de plus.`
    },
    {
      ancre: 'arrivee',
      question: 'Pourquoi deux chiffres pour les femmes nées à l’étranger ?',
      chiffre: `${v2(c.textes.icf_etranger_brut_2017_2021)} ou ${v2(c.textes.icf_etranger_ajuste_2017_2021)}`,
      reponse: `enfants par femme (2017-2021) : beaucoup ont leurs enfants juste après la migration, ce qui gonfle le calcul classique.`
    },
    {
      ancre: 'generations',
      question: 'Et les descendantes d’immigrés ?',
      chiffre: v2(c.lien.descendantes),
      reponse: `enfant en moyenne pour les femmes nées en France d’au moins un parent immigré, de 1960 à 1974 ; ${v2(c.lien.ni)} pour les femmes sans ascendance migratoire, ${v2(c.lien.immigrees)} pour les immigrées des mêmes générations.`
    },
    {
      ancre: 'seuil',
      question: 'Les naissances suffisent-elles à renouveler les générations ?',
      chiffre: v2(c.frDer.icf),
      reponse: `${enfants(c.frDer.icf)} par femme en ${c.frDer.annee}, sous le seuil de remplacement (${v2(c.seuilDer)})${c.sousSeuilDepuis ? ` depuis ${c.sousSeuilDepuis} en métropole` : ''}.`
    },
    {
      ancre: 'onu',
      question: 'Que disait l’ONU des « migrations de remplacement » ?',
      chiffre: millions(parAn(o.V)),
      reponse: `de migrants par an pour garder en France le rapport de 1995 entre actifs et âgés : selon l’ONU, ce maintien « semble inaccessible » par la seule immigration.`
    }
  ]);
</script>

<svelte:head>
  <title>Les naissances · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Naissances selon le pays de naissance des parents, fécondité des femmes nées à l'étranger, convergence des générations, seuil de remplacement, et ce que disait le rapport de l'ONU sur les « migrations de remplacement »."
  />
</svelte:head>

<article class="page nai">
  <header class="colonne">
    <h1>Les naissances</h1>
    <p class="chapeau">
      De quels parents naissent les enfants, combien en ont les femmes venues d’ailleurs, et les
      femmes nées en France d’un parent immigré ? Et d’où vient l’expression « migrations de
      remplacement » ?
    </p>
    <p class="mode-emploi">
      <strong>Trois mesures à ne pas mêler.</strong> Les <em>naissances</em> d’une année comptent
      les enfants nés cette année-là. L’<em>indicateur conjoncturel de fécondité</em> d’une année
      donne le nombre d’enfants qu’aurait une femme qui connaîtrait, toute sa vie, la fécondité de
      chaque âge observée cette année-là. La <em>descendance finale</em> d’une génération donne le nombre
      d’enfants que les femmes nées une année donnée ont réellement eus.
    </p>
  </header>

  <Sommaire items={SOMMAIRE} />

  <section id="parents">
    <div class="colonne">
      <h2>De quels parents naissent les enfants ?</h2>
      <p class="reponse">
        En {c.dernier.annee}, {milliers(c.dernier.ensemble)} enfants sont nés en France.
        <strong>{pct(c.partsDernier.mere)}</strong> avaient une mère née à l’étranger, {pct(
          c.partsDernier.auMoinsUn
        )} au moins un parent né à l’étranger, {pct(c.partsDernier.deux)} deux parents nés à l’étranger
        : trois chiffres pour trois questions différentes.
        {#if c.base.annee < c.dernier.annee && c.variation.ensemble < 0}
          Depuis {c.base.annee}, à méthode et champ constants, les naissances ont baissé de {milliers(
            -c.variation.ensemble
          )}, et celles de deux parents nés en France de {milliers(
            -c.variation.deuxNesFrance
          )}{#if c.variation.deuxParents > 0}, tandis que celles de deux parents nés à l’étranger
            ont augmenté de {milliers(c.variation.deuxParents)}{/if}.
        {/if}
      </p>
    </div>
    <TLCadre
      titre="Naissances selon le pays de naissance des parents, {c.premier.annee}-{c.dernier.annee}"
      lecture="en {c.dernier.annee}, {entier(
        c.dernier.deuxNesFrance
      )} enfants sont nés de deux parents nés en France, {entier(
        c.dernier.unParent
      )} d’un parent né en France et d’un parent né à l’étranger, {entier(
        c.dernier.deuxParents
      )} de deux parents nés à l’étranger. Les trois courbes font le total des naissances. La série est coupée en {RUPTURE} (changement de méthode de l’Insee)."
      source="Insee, statistiques de l’état civil (tableur 2381382, figure 2)"
      champ="France hors Mayotte jusqu’en 2013, France ensuite ; parents nés en France y compris dans les collectivités d’outre-mer ; « né à l’étranger » comprend les Français nés à l’étranger (U26)"
      statut="{c.dernier.annee} provisoire"
      fichiers={['naissances_parents.csv', 'naissances_detail.csv']}
    >
      <div class="bascule" role="group" aria-label="Mesure affichée">
        <button type="button" aria-pressed={mesure === 'nombre'} onclick={() => (mesure = 'nombre')}
          >Nombre</button
        >
        <button type="button" aria-pressed={mesure === 'part'} onclick={() => (mesure = 'part')}
          >Part des naissances</button
        >
      </div>
      <p class="legende-lignes">
        {#each serieParents as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieParents}
        reperes={[
          { x: RUPTURE, libelle: 'méthode', style: 'rupture' },
          { x: 2014, libelle: '+ Mayotte', style: 'champ' }
        ]}
        marqueurs
        yFormat={mesure === 'nombre' ? (y) => `${virgule(y / 1000, 0)} k` : (y) => `${y} %`}
        titre="Naissances selon le pays de naissance des parents, {mesure === 'nombre'
          ? 'en nombre'
          : 'en part des naissances'}"
        infobulle={infobulleParents}
      />
      {#snippet tableau()}
        <table>
          <thead
            ><tr
              ><th>Année</th><th>Naissances</th><th>Deux parents nés en France</th><th
                >Un parent né à l’étranger</th
              ><th>Deux parents nés à l’étranger</th><th>Mère née à l’étranger</th></tr
            ></thead
          >
          <tbody>
            {#each ans as a (a.annee)}
              <tr
                ><td>{a.annee}{a.provisoire ? ' (p)' : ''}</td><td>{entier(a.ensemble)}</td><td
                  >{entier(a.deuxNesFrance)}</td
                ><td>{entier(a.unParent)}</td><td>{entier(a.deuxParents)}</td><td
                  >{entier(a.mereEtranger)}</td
                ></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </TLCadre>
    <TLCadre
      titre="Trois façons de compter les naissances « d’origine étrangère », {c.dernier.annee}"
      lecture="en {c.dernier.annee}, {pct(
        c.partsDernier.mere
      )} des enfants nés en France avaient une mère née à l’étranger. Les trois catégories s’emboîtent : un enfant de deux parents nés à l’étranger compte dans les trois barres."
      source="Insee, statistiques de l’état civil"
      champ="France ; pays de naissance des parents, pas leur nationalité (U26)"
      statut="provisoire"
      fichiers={['naissances_parents.csv', 'naissances_detail.csv']}
    >
      <TLBarres
        lignes={[
          {
            libelle: 'Au moins un parent né à l’étranger',
            valeurs: [c.partsDernier.auMoinsUn]
          },
          { libelle: 'Mère née à l’étranger', valeurs: [c.partsDernier.mere] },
          { libelle: 'Deux parents nés à l’étranger', valeurs: [c.partsDernier.deux] }
        ]}
        cles={[{ libelle: 'Part des naissances', couleur: 'var(--serie-1)' }]}
        format={(v) => pct(v)}
        titre="Part des naissances de {c.dernier.annee} selon trois définitions"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        {#if c.variation.deuxParents > 0 && c.base.annee < c.dernier.annee}
          <p>
            La part des naissances de deux parents nés à l’étranger passe de {pct(partDeuxBase)} en {c
              .base.annee} à {pct(c.partsDernier.deux)} en {c.dernier.annee}. Si leur nombre était
            resté celui de {c.base.annee}, la seule baisse des autres naissances l’aurait portée à {pct(
              partSansHausse
            )} : une part monte aussi quand le reste baisse.
          </p>
        {/if}
        <p>
          Les comparaisons partent de {c.base.annee} : en 2011, un changement de méthode de l’Insee déplace
          des naissances de la catégorie « un parent né à l’étranger » vers « deux parents nés à l’étranger
          » (de {RUPTURE - 1} à {RUPTURE}, les premières baissent de {milliers(
            avantRupture.unParent - apresRupture.unParent
          )}, la part des secondes passe de {pct(
            (100 * avantRupture.deuxParents) / avantRupture.ensemble
          )} à {pct((100 * apresRupture.deuxParents) / apresRupture.ensemble)}), et Mayotte entre
          dans le champ en 2014.
        </p>
        <p>
          « Né à l’étranger » n’est pas « immigré ». L’état civil connaît le pays de naissance des
          parents, pas leur nationalité de naissance : un Français né à l’étranger y est « né à
          l’étranger » (U26). La piscine, elle, estime les naissances selon que les parents sont
          immigrés ou non, avec un modèle : <a href="/piscine">voir la piscine</a>.
        </p>
        <p>
          « Mère née à l’étranger », « au moins un parent », « deux parents » : les trois chiffres
          sont justes, mais ils ne répondent pas à la même question. Un enfant d’un couple mixte
          compte dans l’une et pas dans l’autre ; un chiffre cité sans sa définition ne dit pas
          laquelle.
        </p>
      </Detail>
    </div>
  </section>

  <section id="fecondite">
    <div class="colonne">
      <h2>Les femmes nées à l’étranger ont-elles plus d’enfants ?</h2>
      <p class="reponse">
        {#if c.icf.etranger > c.icf.france}<strong>Oui</strong> :{/if}
        {v2(c.icf.etranger)}
        {enfants(c.icf.etranger)} par femme en {c.icf.annee}, contre {v2(c.icf.france)} pour les femmes
        nées en France (indicateur conjoncturel ajusté par l’Insee pour les femmes nées à l’étranger).
        {#if c.icf.france < c.icf.franceDebut}
          Depuis {c.icf.debut}, l’écart s’est creusé surtout parce que la fécondité des femmes nées
          en France a baissé, de {v2(c.icf.franceDebut)} à {v2(c.icf.france)} ; celle des femmes nées
          à l’étranger est restée entre {v2(etrMin)} et {v2(etrMax)}.
        {/if}
      </p>
    </div>
    <TLCadre
      titre="Indicateur conjoncturel de fécondité selon le lieu de naissance, {c.icf.debut}-{c.icf
        .annee}"
      lecture="en {c.icf.annee}, l’indicateur est de {v2(
        c.icf.etranger
      )} enfants par femme pour les femmes nées à l’étranger, {v2(
        c.icf.france
      )} pour les femmes nées en France et {v2(
        c.icf.ensemble
      )} pour l’ensemble. L’axe part de zéro. Mayotte entre dans le champ en 2014."
      source="Insee, Insee Première 1939 (2023), figure 6 ; état civil, estimations de population, enquête TeO2 pour l’ajustement"
      champ="France hors Mayotte jusqu’en 2013, France ensuite ; femmes nées à l’étranger, Françaises de naissance comprises (U26)"
      statut="nées à l’étranger : indicateur ajusté, estimé (U25) ; ensemble et nées en France : calcul classique"
      fichiers={['fecondite_icf.csv']}
    >
      <p class="legende-lignes">
        {#each serieIcf as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieIcf}
        marqueurs
        yFormat={(y) => virgule(y, 1)}
        titre="Indicateur conjoncturel de fécondité selon le lieu de naissance"
      />
    </TLCadre>
    <TLCadre
      titre="Indicateur conjoncturel des femmes nées à l’étranger selon leur pays de naissance, {c
        .icf.annee}"
      lecture="en {c.icf.annee}, l’indicateur va de {v2(
        data.regions.at(-1)!.icf
      )} ({data.regions.at(-1)!.libelle}) à {v2(data.regions[0].icf)} ({data.regions[0]
        .libelle}) enfants par femme ; il est de {v2(
        c.icf.france
      )} pour les femmes nées en France. Ce sont des estimations, qui varient d’une année à l’autre pour les groupes où les arrivées sont récentes."
      source="Insee, Insee Première 1939 (2023), figure 6"
      champ="France ; femmes nées à l’étranger, par pays de naissance"
      statut="indicateur ajusté, estimé (U25)"
      fichiers={['fecondite_icf.csv']}
    >
      <TLBarres
        lignes={[
          ...data.regions.map((r) => ({ libelle: r.libelle, valeurs: [r.icf] })),
          { libelle: 'Femmes nées en France', valeurs: [c.icf.france] }
        ]}
        cles={[{ libelle: 'Enfants par femme', couleur: 'var(--serie-1)' }]}
        format={(v) => v2(v)}
        accent={(l) => l === 'Femmes nées en France'}
        titre="Indicateur conjoncturel de fécondité selon le pays de naissance en {c.icf.annee}"
      />
    </TLCadre>
  </section>

  <section id="poids">
    <div class="colonne">
      <h2>Que changent-elles à la fécondité de la France ?</h2>
      <p class="reponse">
        En {c.icf.annee}, l’indicateur de la France est de {v2(c.icf.ensemble)} enfant par femme avec
        les femmes nées à l’étranger ({v2(c.textes.icf_ensemble_ajuste)} avec l’ajustement de l’Insee)
        et de {v2(c.icf.france)} sans elles :
        <strong>+{v2(c.contributionAjustee)} à +{v2(c.contribution)}</strong>
        enfant par femme selon le calcul, soit une hausse de {virgule(c.contributionAjusteeRel, 0)} à
        {virgule(c.contributionRel, 0)} % de l’indicateur, pas de {v2(c.contribution)} %. Un
        indicateur national est une moyenne : les femmes nées à l’étranger y pèsent pour leur part
        (leurs enfants font {pct(c.partsIcf.mere)} des naissances de
        {c.icf.annee}), et c’est cette part qui limite leur effet.
      </p>
    </div>
    <TLCadre
      titre="Indicateur conjoncturel de fécondité de la France avec et sans les femmes nées à l’étranger, {c
        .icf.annee}"
      lecture="en {c.icf.annee}, l’indicateur de l’ensemble des femmes est de {v2(
        c.icf.ensemble
      )} par le calcul classique, {v2(
        c.textes.icf_ensemble_ajuste
      )} avec l’ajustement ; celui des femmes nées en France, c’est-à-dire de la France sans les femmes nées à l’étranger, de {v2(
        c.icf.france
      )}."
      source="Insee, Insee Première 1939 (2023), figure 6 et encadré"
      champ="France"
      statut="nées à l’étranger et ensemble ajusté : estimations (U25)"
      fichiers={['fecondite_icf.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'Femmes nées à l’étranger', valeurs: [c.icf.etranger] },
          { libelle: 'Ensemble, calcul classique', valeurs: [c.icf.ensemble] },
          { libelle: 'Ensemble, avec l’ajustement', valeurs: [c.textes.icf_ensemble_ajuste] },
          { libelle: 'Femmes nées en France', valeurs: [c.icf.france] }
        ]}
        cles={[{ libelle: 'Enfants par femme', couleur: 'var(--serie-1)' }]}
        format={(v) => v2(v)}
        accent={(l) => l.startsWith('Ensemble')}
        titre="Indicateur conjoncturel de fécondité en {c.icf
          .annee}, avec et sans les femmes nées à l’étranger"
      />
    </TLCadre>
  </section>

  <section id="arrivee">
    <div class="colonne">
      <h2>Pourquoi deux chiffres pour les femmes nées à l’étranger ?</h2>
      <p class="reponse">
        Parce que beaucoup ont leurs enfants juste après la migration. Le calcul classique, qui ne
        regarde que les années passées en France, leur donne
        <strong>{v2(c.textes.icf_etranger_brut_2017_2021)}</strong>
        enfants par femme en moyenne de 2017 à 2021 ; l’ajustement de l’Insee, qui tient compte de leur
        fécondité plus faible avant l’arrivée, {v2(c.textes.icf_etranger_ajuste_2017_2021)}. Les
        immigrées nées de 1960 à 1974 ont eu {pct(c.calendrier.cinqAns)} de tous leurs enfants en France
        l’année de leur arrivée et les quatre années suivantes.
      </p>
    </div>
    <TLCadre
      titre="Naissances des immigrées selon les années écoulées depuis leur arrivée en France"
      lecture="un an après leur première entrée en France, les immigrées nées de 1960 à 1974 ont eu en France {pct(
        c.calendrier.annee1
      )} de tous leurs enfants. Les naissances à l’étranger en font {pct(
        c.calendrier.etranger
      )}, dont {virgule(
        c.calendrier.etrangerAvant,
        1
      )} points avant l’arrivée. Le calcul classique ne voit que la partie en France, au moment où elle est la plus haute."
      source="Ined-Insee, enquête Trajectoires et Origines 2 (2019-2020), dans Insee Première 1939, figure 5"
      champ="Femmes immigrées nées de 1960 à 1974, logements ordinaires, France métropolitaine ; en % de toutes leurs naissances"
      statut="enquête"
      fichiers={['fecondite_arrivee.csv']}
    >
      <p class="legende-lignes">
        {#each serieArrivee as s (s.id)}
          <span
            ><b class="pastille" style:background={s.couleur}></b>Naissances {minuscule(
              s.libelle
            )}</span
          >
        {/each}
      </p>
      <TLLignes
        series={serieArrivee}
        reperes={[{ x: 0, libelle: 'arrivée en France', style: 'champ' }]}
        xFormat={duree}
        yFormat={(y) => `${virgule(y, 0)} %`}
        titre="Naissances des immigrées selon les années écoulées depuis leur arrivée"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Selon l’Insee, les femmes nées à l’étranger « ont tendance à repousser leurs maternités
          après la migration » : ces naissances retardées puis rattrapées font monter l’indicateur
          du moment, et c’est ce que corrige l’ajustement (U25). La migration est aussi souvent
          associée à une mise en couple (Laurent Toulemon, Ined, <em>Population et Sociétés</em>
          n° 400, 2004, cité par l’Insee). L’âge à l’arrivée compte : les immigrées arrivées avant 15
          ans ont eu {v2(c.lien.avant15)} enfants en moyenne, celles arrivées à 15 ans ou plus {v2(
            c.lien.apres15
          )}.
        </p>
        <p>
          Pour l’ensemble des femmes, l’ajustement change peu : {v2(c.textes.icf_ensemble_ajuste)} au
          lieu de {v2(c.textes.icf_ensemble_brut)}, selon l’Insee, qui ne préconise donc pas de
          l’appliquer à l’indicateur national.
        </p>
      </Detail>
    </div>
  </section>

  <section id="generations">
    <div class="colonne">
      <h2>Et les descendantes d’immigrés ?</h2>
      <p class="reponse">
        {#if procheDes}Leur fécondité rejoint celle des autres femmes.{/if} Les immigrées nées de 1960
        à 1974 ont eu {v2(c.lien.immigrees)} enfants en moyenne ; les femmes des mêmes générations nées
        en France d’au moins un parent immigré,
        <strong>{v2(c.lien.descendantes)}</strong>{commeNi} les femmes sans ascendance migratoire ({v2(
          c.lien.ni
        )}). Au fil des générations, la descendance baisse pour toutes : pour les immigrées, de {v2(
          genPremiere.valeur
        )} enfants (nées de {periode(genPremiere.debut)}) à {v2(genDerniere.valeur)} (nées de {periode(
          genDerniere.debut
        )}) ; de {v2(genNonPremiere.valeur)} à {v2(genNonDerniere.valeur)} pour les non-immigrées (les
        générations les plus jeunes n’avaient pas tout à fait fini d’avoir des enfants).
      </p>
    </div>
    <TLCadre
      titre="Descendance finale des femmes selon le lien à la migration, générations 1960-1974"
      lecture="les femmes immigrées nées de 1960 à 1974 ont eu en moyenne {v2(
        c.lien.immigrees
      )} enfants, les filles de deux parents immigrés {v2(
        c.lien.deuxParents
      )}, celles d’un seul parent immigré {v2(
        c.lien.unParent
      )}, les femmes sans ascendance migratoire directe {v2(c.lien.ni)}."
      source="Ined-Insee, enquête Trajectoires et Origines 2 (2019-2020), dans Insee Première 1939, figure 1"
      champ="Femmes nées de 1960 à 1974, logements ordinaires, France métropolitaine ; tous les enfants, nés en France ou à l’étranger"
      statut="enquête"
      fichiers={['fecondite_descendance.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'Immigrées', valeurs: [c.lien.immigrees] },
          { libelle: 'Filles de deux parents immigrés', valeurs: [c.lien.deuxParents] },
          { libelle: 'Filles d’un parent immigré', valeurs: [c.lien.unParent] },
          { libelle: 'Sans ascendance migratoire', valeurs: [c.lien.ni] }
        ]}
        cles={[{ libelle: 'Enfants par femme', couleur: 'var(--serie-1)' }]}
        format={(v) => v2(v)}
        titre="Descendance finale selon le lien à la migration, femmes nées de 1960 à 1974"
      />
    </TLCadre>
    <TLCadre
      titre="Descendance finale des immigrées et des non-immigrées, par génération"
      lecture="les immigrées nées de {periode(genPremiere.debut)} ont eu {v2(
        genPremiere.valeur
      )} enfants en moyenne, celles nées de {periode(genDerniere.debut)}, {v2(
        genDerniere.valeur
      )}. Les femmes nées à partir de 1970 n’avaient pas tout à fait fini d’avoir des enfants au moment de l’enquête."
      source="Ined-Insee, enquêtes Trajectoires et Origines 1 (2008-2009, générations 1950-1959) et 2 (2019-2020), dans Insee Première 1939, figure 2a"
      champ="Femmes nées de 1950 à 1974, logements ordinaires, France métropolitaine"
      statut="enquête"
      fichiers={['fecondite_descendance.csv']}
    >
      <p class="legende-lignes">
        {#each serieGenerations as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieGenerations}
        marqueurs
        xFormat={tranche}
        xTicks={c.genImmigrees.map((g) => g.debut)}
        yFormat={(y) => virgule(y, 1)}
        titre="Descendance finale des immigrées et des non-immigrées, par génération"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          L’écart dépend du diplôme : parmi les femmes nées de 1960 à 1974 qui ont un diplôme
          supérieur au baccalauréat, les immigrées ont eu {v2(
            diplome('superieur_au_bac', 'immigrees')
          )}
          {enfants(diplome('superieur_au_bac', 'immigrees'))}, les femmes sans ascendance migratoire {v2(
            diplome('superieur_au_bac', 'ni_immigrees_ni_descendantes')
          )} ; sans diplôme ou avec un diplôme inférieur au baccalauréat, {v2(
            diplome('sans_diplome_ou_inferieur_au_bac', 'immigrees')
          )} contre {v2(
            diplome('sans_diplome_ou_inferieur_au_bac', 'ni_immigrees_ni_descendantes')
          )}.
        </p>
        <p>
          Ces chiffres décrivent des femmes nées il y a plus de cinquante ans : la descendance
          finale ne se connaît qu’à la fin de la vie féconde. La fécondité des immigrées arrivées
          depuis ne se lit encore que dans l’indicateur du moment (plus haut). Les filles d’immigrés
          sont ici celles des générations 1960-1974, pas les filles des immigrées de ces
          générations.
        </p>
      </Detail>
    </div>
  </section>

  <section id="seuil">
    <div class="colonne">
      <h2>Les naissances suffisent-elles à renouveler les générations ?</h2>
      <p class="reponse">
        {#if c.frDer.icf < c.seuilDer}<strong>Non</strong>{#if c.sousSeuilDepuis}, et ce n’est pas
            nouveau{/if} :{/if}
        en {c.frDer.annee}, l’indicateur conjoncturel de la France est de {v2(c.frDer.icf)}
        {enfants(c.frDer.icf)} par femme{c.frDer.provisoire ? ' (provisoire)' : ''}, pour un seuil
        de remplacement de {v2(c.seuilDer)}{#if c.sousSeuilDepuis}{' ;'} en métropole, il est sous ce
          seuil chaque année depuis {c.sousSeuilDepuis}{/if}.
        {#if c.seuilDer > 2}Le seuil n’est pas de deux enfants : il en faut un peu plus, parce qu’il
          naît plus de garçons que de filles et que toutes les filles n’atteignent pas l’âge d’avoir
          des enfants.{/if} En {c.seuilPremier.annee}, avec la mortalité de l’époque, il était de {v2(
          c.seuilPremier.seuil
        )}.
      </p>
    </div>
    <TLCadre
      titre="Indicateur conjoncturel de fécondité et seuil de remplacement, France métropolitaine, {metro[0]
        .annee}-{metro.at(-1)!.annee}"
      lecture="en {metro.at(-1)!.annee}, l’indicateur est de {v2(
        metro.at(-1)!.icf
      )} enfant par femme en métropole et le seuil de remplacement de {v2(
        metro.at(-1)!.seuil
      )}. Le seuil baisse avec la mortalité : il faut moins de naissances pour remplacer une génération quand presque toutes les filles atteignent l’âge adulte."
      source="Insee, bilan démographique 2025, tableaux rétrospectifs (indicateur conjoncturel, taux de reproduction)"
      champ="France métropolitaine (la série de la France entière commence en 1994) ; seuil = indicateur conjoncturel ÷ taux net de reproduction × 100"
      statut={metro.at(-1)!.provisoire ? 'dernières années provisoires' : 'définitif'}
      fichiers={['fecondite_nationale.csv']}
    >
      <p class="legende-lignes">
        {#each serieNationale as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieNationale}
        yFormat={(y) => virgule(y, 1)}
        titre="Indicateur conjoncturel de fécondité et seuil de remplacement, France métropolitaine"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Le seuil de remplacement est calculé ici pour chaque année à partir de deux indicateurs de
          l’Insee : c’est le nombre d’enfants par femme pour lequel 100 femmes auraient 100 filles
          qui atteignent leur âge, avec la mortalité de l’année. « Deux enfants » en est l’ordre de
          grandeur ; « 2,1 » l’arrondi habituel.
        </p>
        <p>
          Un indicateur du moment n’est pas une descendance. Les femmes nées en {c.genDer
            .generation}
          (métropole) ont eu {v2(c.genDer.descendance)}
          {enfants(c.genDer.descendance)} en moyenne ; l’indicateur conjoncturel de {c.icfA30
            .annee}, l’année de leurs 30 ans, était de {v2(
            c.icfA30.icf
          )}.{#if c.icfA30.icf < c.genDer.descendance}
            L’indicateur d’une année baisse quand les femmes ont leurs enfants plus tard, même si
            elles finissent par en avoir autant.{/if} L’indicateur le plus haut de la série métropolitaine
          est celui de {c.icfMax.annee} ({v2(c.icfMax.icf)}).
        </p>
      </Detail>
    </div>
  </section>

  <section id="onu">
    <div class="colonne">
      <h2>Que disait l’ONU des « migrations de remplacement » ?</h2>
      <p class="reponse">
        En 2000, la Division de la population de l’ONU a calculé combien de migrants il faudrait à
        huit pays, dont la France, pour compenser d’ici 2050 le déclin et le vieillissement de leur
        population. Pour la France, garder la population à son maximum demandait {milliers(
          parAn(o.III)
        )} migrants par an en moyenne ; garder le rapport de 1995 entre les 15-64 ans et les 65 ans ou
        plus, <strong>{millions(parAn(o.V))}</strong> par an. Sa conclusion : ce maintien « {citation(
          'vieillissement'
        ).texte.match(/semble inaccessible/)![0]} » par la seule immigration.
      </p>
    </div>
    <TLCadre
      titre="Les cinq scénarios de l’ONU pour la France, 1995-2050"
      lecture="pour garder en 2050 le rapport de 1995 entre les 15-64 ans et les 65 ans ou plus (scénario V), il aurait fallu {millions(
        parAn(o.V)
      )} de migrants par an ; la France aurait compté {millions(
        o.V.population_2050 * 1000
      )} d’habitants en 2050, dont {virgule(
        o.V.part_post1995_2050,
        0
      )} % de migrants arrivés après 1995 et de leurs descendants. Ce sont des calculs, pas des prévisions ni des recommandations."
      source="ONU, Division de la population, Replacement Migration (ESA/P/WP.160, 2000), tableaux 1, IV.4, IV.5, IV.7, IV.10 et IV.11 ; révision 1998 des projections de l’ONU"
      champ="France métropolitaine (58,0 millions d’habitants en 1995 selon le rapport) ; solde migratoire moyen de 2000 à 2050 ; population au 1er juillet 2050"
      statut="projection de 2000"
      fichiers={['onu2000.csv']}
    >
      <div class="defile">
        <table class="scenarios">
          <thead>
            <tr>
              <th scope="col">Scénario</th>
              <th scope="col">Solde migratoire par an</th>
              <th scope="col">Population en 2050</th>
              <th scope="col">Migrants arrivés après 1995 et descendants, en 2050</th>
              <th scope="col">15-64 ans pour un 65 ans ou plus, en 2050</th>
            </tr>
          </thead>
          <tbody>
            {#each data.onu.scenarios as s (s.code)}
              <tr>
                <th scope="row"><span class="code-sc">{s.code}</span> {s.libelle}</th>
                <td>{milliers(s.valeurs.migrants_par_an * 1000)}</td>
                <td>{millions(s.valeurs.population_2050 * 1000)}</td>
                <td>{virgule(s.valeurs.part_post1995_2050, 1)} %</td>
                <td>{v2(s.valeurs.rapport_soutien_2050)}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      <p class="note">
        En 1995, la France comptait {millions(o.I.population_1995 * 1000)} d’habitants et {v2(
          o.I.rapport_soutien_1995
        )} personnes de 15 à 64 ans pour une de 65 ans ou plus.
      </p>
    </TLCadre>
    <div class="colonne">
      <Detail titre="Ce que dit le rapport, et ce qu’il ne dit pas">
        <p>
          Le rapport les définit ainsi : « {citation('definition').texte} » (résumé en français, p. {citation(
            'definition'
          ).page}). « Remplacement » y désigne une compensation de nombres. Pour la France : « {citation(
            'france'
          ).texte} » (p. {citation('france').page}). Pour le vieillissement, il conclut au contraire
          que le maintien du rapport entre actifs et personnes âgées par la seule immigration « {citation(
            'vieillissement'
          ).texte.split('ayant recours à une migration de remplacement ')[1]} » (p. {citation(
            'vieillissement'
          ).page}). Et : « {citation('age_actif').texte} » ; pour la France, sans migration, à {virgule(
            data.onu.scenarios.find((s) => s.code === 'II')!.valeurs.age_limite_actif,
            0
          )} ans.
        </p>
        <p>
          On lit parfois que le titre du rapport prouverait un projet de substitution de population.
          Le rapport calcule des scénarios sans en recommander aucun. Il écrit que, {'«'}{' '}{minuscule(
            citation('court_terme').texte
          )}{' '}{'»'} (p. {citation('court_terme').page}).
        </p>
        <p>
          Depuis, en France métropolitaine (le champ du rapport), le solde migratoire a été de {milliers(
            o.soldeMoyen
          )} personnes par an en moyenne de {o.soldeDe} à {o.soldeA} (Insee{o.provisoires.length
            ? ` ; ${o.provisoires.slice(0, -1).join(', ')}${o.provisoires.length > 1 ? ' et ' : ''}${o.provisoires.at(-1)} provisoires`
            : ''}){#if o.provisoires.length}, {milliers(o.soldeMoyenDefinitif)} de {o.soldeDe} à {o.derDefinitif}{/if}
          :
          {comparaisonIV}, très loin du scénario V. Ce n’est qu’un ordre de grandeur : les moyennes
          du rapport portent sur 2000-2050, alors que dans les scénarios III et IV les migrations ne
          commencent qu’au moment où la population, ou les 15-64 ans, auraient commencé à baisser.
          Le rapport entre les 15-64 ans et les 65 ans ou plus est passé de {v2(o.soutien1995)} au 1er
          janvier 1995 à {v2(o.soutienDer)} au 1er janvier {o.anSoutien} (Insee, France entière) : le
          vieillissement a continué, comme le rapport l’annonçait. La variante moyenne de 1998 supposait
          {milliers(o.I.migrants_1995_2050 * 1000)} migrants de 1995 à 2020 ; l’Insee a mesuré en métropole
          un solde migratoire de {milliers(o.cumul1995_2020)}{#if o.depasseSaufV}, et la métropole a
            déjà {millions(o.popDer)} d’habitants en {o.anPop}, plus que la population projetée pour
            2050 dans tous les scénarios sauf le cinquième{/if}. Une projection n’est pas une
          prévision.
        </p>
      </Detail>
    </div>
  </section>

  <section class="colonne">
    <Detail
      encadre
      niveau={2}
      titre="Ce qu’on ne sait pas, et comment c’est montré"
      resume="Les limites des séries de cette page ({data.incertitudes
        .map((u) => u.code)
        .join(', ')}) et la façon dont chacune apparaît."
    >
      <dl class="incertitudes">
        {#each data.incertitudes as u (u.code)}
          <dt><span class="code">{u.code}</span> {u.titre}</dt>
          <dd>{u.detail} <em>Ici : {minuscule(u.traitement)}.</em></dd>
        {/each}
      </dl>
    </Detail>
  </section>
</article>

<style>
  .nai {
    --serie-1: #2a78d6;
    --cat-2: #7a5fb8;
    --cat-5: #acb3bc;
  }
  @media (prefers-color-scheme: dark) {
    .nai {
      --serie-1: #3987e5;
      --cat-2: #a48bdb;
      --cat-5: #5a636c;
    }
  }
  section {
    margin-top: 2.5rem;
  }
  .mode-emploi {
    color: var(--ardoise);
  }
  .bascule {
    display: flex;
    gap: 0.3rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
  }
  .bascule button {
    font: inherit;
    font-size: var(--t-0);
    padding: 0.3rem 0.85rem;
    border-radius: 2px;
    border: 1.5px solid var(--encre);
    background: transparent;
    color: var(--encre);
    cursor: pointer;
  }
  .bascule button[aria-pressed='true'] {
    background: var(--encre);
    color: var(--papier);
  }
  .legende-lignes {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1rem;
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .pastille {
    display: inline-block;
    width: 0.75em;
    height: 0.75em;
    border-radius: 50%;
    margin-right: 0.35em;
    vertical-align: -0.05em;
  }
  .defile {
    overflow-x: auto;
  }
  .scenarios {
    border-collapse: collapse;
    font-size: var(--t-0);
    font-variant-numeric: tabular-nums;
    width: 100%;
  }
  .scenarios th,
  .scenarios td {
    padding: 0.35rem 0.6rem;
    border-bottom: 1px solid var(--reglure);
    text-align: right;
    vertical-align: top;
  }
  .scenarios thead th {
    font-weight: 600;
    color: var(--ardoise);
  }
  .scenarios thead th:first-child,
  .scenarios th[scope='row'] {
    text-align: left;
    font-weight: 400;
    min-width: 12rem;
  }
  .code-sc {
    font-weight: 700;
    margin-right: 0.3em;
  }
  .note {
    color: var(--gris);
    font-size: var(--t-0);
  }
  .incertitudes dt {
    font-weight: 600;
    margin-top: 0.75rem;
  }
  .incertitudes dd {
    margin: 0.15rem 0 0;
    color: var(--ardoise);
  }
  .code {
    font-size: var(--t-0);
    color: var(--gris);
  }
</style>
