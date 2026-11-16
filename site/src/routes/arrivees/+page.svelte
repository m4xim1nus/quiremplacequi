<script lang="ts">
  import TLCadre from '$lib/components/TLCadre.svelte';
  import TLLignes from '$lib/components/TLLignes.svelte';
  import TLFacettes from '$lib/components/TLFacettes.svelte';
  import TLBarres from '$lib/components/TLBarres.svelte';
  import Sommaire from '$lib/components/Sommaire.svelte';
  import Detail from '$lib/components/Detail.svelte';
  import { entier, milliers, pct, virgule } from '$lib/format';
  import { DU_MOTIF, LIBELLES_MOTIFS, type Motif } from '$lib/comparaisons';

  let { data } = $props();
  const c = $derived(data.chiffres);
  const irr = $derived(data.irreguliers);
  const ans = $derived(data.annees);
  const pctEntier = (x: number) => `${Math.round(x)} %`;
  const signe = (x: number) => (x > 0 ? `+${milliers(x)}` : milliers(x));
  const part = (k: string) => c.hausse.find((h) => h.cle === k)!.part;
  const minuscule = (s: string) => s.charAt(0).toLowerCase() + s.slice(1);
  // Les deux motifs qui contribuent le plus à la hausse.
  const grands = $derived([...c.hausse].sort((a, b) => b.part - a.part).slice(0, 2));

  // D1 : bascule nombre ↔ pour 10 000 habitants.
  let mesure: 'nombre' | 'relatif' = $state('nombre');
  const val = (n: number, pop: number) => (mesure === 'nombre' ? n : (1e4 * n) / pop);
  const fmtVal = (y: number) =>
    mesure === 'nombre' ? `${milliers(y)}` : `${virgule(y, 1)} pour 10 000`;
  const serieTitres = $derived([
    {
      id: 'total',
      libelle: 'Tous les premiers titres',
      couleur: 'var(--serie-1)',
      segments: [
        ans.map((a) => ({
          x: a.annee,
          y: val(a.total, a.population),
          etiquette: fmtVal(val(a.total, a.population))
        }))
      ]
    },
    {
      id: 'hors',
      libelle: 'Hors Britanniques',
      couleur: 'var(--cat-2)',
      segments: [
        ans.map((a) => ({
          x: a.annee,
          y: val(a.total - a.britanniques, a.population),
          etiquette: fmtVal(val(a.total - a.britanniques, a.population))
        }))
      ]
    }
  ]);
  const infobulleTitres = (x: number) => {
    const a = ans.find((v) => v.annee === x)!;
    return `${entier(a.total)} premiers titres, dont ${entier(a.britanniques)} à des Britanniques${a.brexit ? ` (${entier(a.brexit)} au titre de l’accord de retrait)` : ''} · ${virgule((1e4 * a.total) / a.population, 1)} pour 10 000 habitants`;
  };

  const facettes = $derived(
    data.motifs.map((m) => ({
      titre: LIBELLES_MOTIFS[m],
      points: ans.map((a) => ({ x: a.annee, y: a.motifs[m] }))
    }))
  );
  const yMaxMotifs = $derived(Math.max(...ans.flatMap((a) => Object.values(a.motifs))) * 1.15);
  const etudesDevant = $derived(
    ans.find((a, i) => ans.slice(i).every((b) => b.motifs.etudiants > b.motifs.familial))
  );

  // D2 : les trois sous-motifs familiaux.
  const serieFamille = $derived(
    (
      [
        ['francais', 'Famille de Français', 'var(--serie-1)'],
        ['membre', 'Membre de famille', 'var(--cat-2)'],
        ['liens', 'Liens personnels et familiaux', 'var(--cat-3)']
      ] as const
    ).map(([k, libelle, couleur]) => ({
      id: k,
      libelle,
      couleur,
      segments: [ans.map((a) => ({ x: a.annee, y: a.famille[k] }))]
    }))
  );
  const famDernier = $derived(c.dernier.famille);

  // D4 : entrées (Insee) et premiers titres (ministère).
  const serieDeux = $derived([
    {
      id: 'insee',
      libelle: 'Entrées d’immigrés (Insee)',
      couleur: 'var(--serie-1)',
      segments: [data.flux.map((f) => ({ x: f.annee, y: f.entreesImm }))]
    },
    {
      id: 'titres',
      libelle: 'Premiers titres (Intérieur)',
      couleur: 'var(--cat-2)',
      segments: [ans.map((a) => ({ x: a.annee, y: a.total }))]
    }
  ]);
  const o = $derived(data.origines);
  const nesUE = $derived(o['Espagne, Italie, Portugal'] + o["Autres pays de l'UE27"]);

  // D5 : soldes des immigrés et des non-immigrés.
  const serieSoldes = $derived([
    {
      id: 'imm',
      libelle: 'Immigrés',
      couleur: 'var(--serie-1)',
      segments: [c.soldes.map((s) => ({ x: s.annee, y: s.immigres }))]
    },
    {
      id: 'ni',
      libelle: 'Non-immigrés',
      couleur: 'var(--cat-2)',
      segments: [c.soldes.map((s) => ({ x: s.annee, y: s.nonImmigres }))]
    }
  ]);
  const infobulleSoldes = (x: number) => {
    const s = c.soldes.find((v) => v.annee === x)!;
    return `immigrés ${signe(s.immigres)} · non-immigrés ${signe(s.nonImmigres)} (${milliers(s.entreesNi)} entrées, ${milliers(s.sortiesNi)} sorties)`;
  };

  const SOMMAIRE = $derived([
    {
      ancre: 'titres',
      question: 'Combien de titres de séjour ?',
      chiffre: milliers(c.dernier.total),
      reponse: `premiers titres en ${c.dernier.annee}, ${virgule(c.pour10k, 0)} pour 10 000 habitants${c.pic.annee === c.dernier.annee ? `, le plus haut de la série commencée en ${c.premier.annee} (titres de l’accord de retrait du Brexit à part)` : ''}. La hausse vient d’abord ${grands.map((h) => DU_MOTIF[h.cle as Motif]).join(' et ')}.`
    },
    {
      ancre: 'famille',
      question: 'La famille, premier motif ?',
      chiffre: pctEntier((100 * c.dernier.motifs.familial) / c.dernier.total),
      reponse: `des titres en ${c.dernier.annee}, un nombre stable depuis ${c.premier.annee}${etudesDevant ? ` ; les études passent devant depuis ${etudesDevant.annee}` : ''}.`
    },
    {
      ancre: 'asile',
      question: 'Asile et titres s’additionnent-ils ?',
      chiffre: 'Non.',
      reponse: `ce sont les étapes d’un même parcours : ${milliers(c.premieres)} premières demandes, ${milliers(c.positives)} décisions positives en première instance en ${c.anAsile}.`
    },
    {
      ancre: 'deux-mesures',
      question: 'Pourquoi deux chiffres des arrivées ?',
      chiffre: milliers(c.fluxOrigines.entreesImm),
      reponse: `immigrés entrés en ${data.anneeOrigines} selon l’Insee, ${milliers(c.titresAnOrigines.total)} premiers titres selon le ministère : deux mesures différentes.`
    },
    {
      ancre: 'solde',
      question: 'Qu’y a-t-il dans le solde migratoire ?',
      chiffre: milliers(c.cumulNonImmigres),
      reponse: `de solde pour les non-immigrés de ${c.soldesDebut} à ${c.soldesFin}, face à ${signe(c.cumulImmigres)} pour les immigrés : les premiers partent plus qu’ils ne reviennent.`
    },
    {
      ancre: 'sans-titre',
      question: 'Et les personnes sans titre ?',
      chiffre: milliers(irr.ame_beneficiaires_2024),
      reponse: `bénéficiaires de l’aide médicale de l’État fin 2024 : un indice, pas un compte. Aucune source publique ne compte les personnes en situation irrégulière.`
    }
  ]);
</script>

<svelte:head>
  <title>Les arrivées · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Qui arrive en France et pour quel motif : titres de séjour, asile, entrées mesurées par l'Insee, et ce que contient le solde migratoire."
  />
</svelte:head>

<article class="page arr">
  <header class="colonne">
    <h1>Les arrivées</h1>
    <p class="chapeau">
      Qui arrive en France, pour quel motif, et comment le compte-t-on ? Deux administrations
      mesurent les arrivées : l’Insee compte les personnes qui s’installent, le ministère de
      l’Intérieur les titres de séjour qu’il délivre. Elles ne mesurent pas la même chose.
    </p>
  </header>

  <Sommaire items={SOMMAIRE} />

  <section id="titres">
    <div class="colonne">
      <h2>Combien de titres de séjour ?</h2>
      <p class="reponse">
        {#if c.pic.annee === c.dernier.annee}<strong
            >Le nombre de premiers titres de séjour est le plus élevé de la série</strong
          >, commencée en {c.premier.annee}, si l’on met à part les titres délivrés après le Brexit
          aux Britanniques déjà installés : {milliers(c.dernier.total)} en {c.dernier
            .annee}{:else}Le ministère a délivré {milliers(c.dernier.total)} premiers titres de séjour
          en {c.dernier.annee}, moins qu’en {c.pic.annee}{/if}, soit {virgule(c.pour10k, 0)} pour 10 000
        habitants, contre {milliers(c.premier.total)} ({virgule(c.pour10kPremier, 0)} pour 10 000) en
        {c.premier.annee}. La hausse vient pour {pctEntier(part('etudiants'))} des études, pour {pctEntier(
          part('economique')
        )} du travail et pour {pctEntier(part('humanitaire'))} de la protection ; la famille y compte
        pour {pctEntier(part('familial'))} et les autres motifs pour {pctEntier(part('divers'))} (calcul
        sur les motifs, hors titres de l’accord de retrait).
      </p>
    </div>
    <TLCadre
      titre="Premiers titres de séjour délivrés, {c.premier.annee}-{c.dernier.annee}"
      lecture="en {c.dernier.annee}, {entier(
        c.dernier.total
      )} premiers titres de séjour ont été délivrés à des ressortissants de pays hors de l’Union européenne, dont {entier(
        c.dernier.britanniques
      )} à des Britanniques. Le pic de 2021 est celui des titres délivrés, au titre de l’accord de retrait du Brexit, aux Britanniques qui vivaient déjà en France ; le creux de 2020 est celui de la crise sanitaire."
      source="Ministère de l’Intérieur (DSED), série publiée le 27 juin 2024 jusqu’en 2014, fichiers annuels définitifs ensuite ; population : Insee, bilan démographique"
      champ="France ; premiers titres délivrés aux ressortissants de pays tiers (hors Union européenne, Espace économique européen et Suisse) ; de 2011 à 2014, la ventilation par motif ne compte pas les Britanniques (moins de 250 titres par an), inclus dans le total ; les titres de l’accord de retrait du Brexit sont dans le total, pas dans les motifs"
      statut="définitif"
      fichiers={['titres.csv', 'titres_totaux.csv']}
    >
      <div class="bascule" role="group" aria-label="Mesure affichée">
        <button type="button" aria-pressed={mesure === 'nombre'} onclick={() => (mesure = 'nombre')}
          >Nombre</button
        >
        <button
          type="button"
          aria-pressed={mesure === 'relatif'}
          onclick={() => (mesure = 'relatif')}>Pour 10 000 habitants</button
        >
      </div>
      <TLLignes
        series={serieTitres}
        reperes={[
          { x: 2020, libelle: 'crise sanitaire', style: 'rupture' },
          { x: 2021, libelle: 'Brexit', style: 'rupture' }
        ]}
        marqueurs
        yFormat={mesure === 'nombre' ? (y) => `${virgule(y / 1000, 0)} k` : (y) => virgule(y, 0)}
        titre="Premiers titres de séjour, {mesure === 'nombre'
          ? 'en nombre'
          : 'pour 10 000 habitants'}"
        infobulle={infobulleTitres}
      />
      {#snippet tableau()}
        <table>
          <thead
            ><tr
              ><th>Année</th><th>Total</th><th>dont Britanniques</th><th>dont accord de retrait</th
              >{#each data.motifs as m (m)}<th>{LIBELLES_MOTIFS[m]}</th>{/each}<th
                >Pour 10 000 hab.</th
              ></tr
            ></thead
          >
          <tbody>
            {#each ans as a (a.annee)}
              <tr
                ><td>{a.annee}</td><td>{entier(a.total)}</td><td>{entier(a.britanniques)}</td><td
                  >{entier(a.brexit)}</td
                >{#each data.motifs as m (m)}<td>{entier(a.motifs[m])}</td>{/each}<td
                  >{virgule((1e4 * a.total) / a.population, 1)}</td
                ></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </TLCadre>
    <TLCadre
      titre="Premiers titres de séjour par motif, {c.premier.annee}-{c.dernier.annee}"
      lecture="en {c.dernier.annee}, {entier(
        c.dernier.motifs.etudiants
      )} titres pour études, {entier(
        c.dernier.motifs.familial
      )} pour motif familial. Même échelle pour les cinq motifs ; le pic de chaque motif est indiqué."
      source="Ministère de l’Intérieur (DSED)"
      champ="France, ressortissants de pays tiers. « Divers » comprend les visiteurs, les étrangers entrés mineurs et, de 2018 à 2022, des Britanniques ; les titres de l’accord de retrait du Brexit en sont retirés"
      statut="définitif"
      fichiers={['titres.csv']}
    >
      <TLFacettes
        {facettes}
        yFormat={(y) => milliers(y)}
        xDomaine={[c.premier.annee, c.dernier.annee]}
        yMax={yMaxMotifs}
        xTicks={[c.premier.annee, c.dernier.annee]}
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          De {c.premier.annee} à {c.dernier.annee}, le nombre de premiers titres passe de {entier(
            c.premier.total
          )} à {entier(c.dernier.total)}. Par motif :
          {#each c.hausse as h, i (h.cle)}{LIBELLES_MOTIFS[h.cle as keyof typeof LIBELLES_MOTIFS]
              .toLowerCase()
              .replace('protection (asile et autres)', 'protection')}
            {signe(h.variation)}{i < c.hausse.length - 1 ? ' ; ' : '.'}
          {/each}
        </p>
        <p>
          Un premier titre n’est pas une arrivée : il peut être délivré des années après l’entrée en
          France. En 2021, {entier(ans.find((a) => a.annee === 2021)?.brexit ?? 0)} titres ont été délivrés
          au titre de l’accord de retrait du Brexit à des Britanniques qui vivaient déjà en France ; ils
          sont comptés dans le total, pas dans les motifs ci-dessus. Avant le Brexit, les Britanniques,
          citoyens européens, n’avaient pas besoin de titre.
        </p>
        <p class="note">
          Les deux sources du ministère se raccordent exactement : de 2015 à 2022, la série publiée
          en juin 2024 plus les titres des Britanniques redonne le total des fichiers annuels
          (contrôle <code>qrq check</code>).
        </p>
      </Detail>
    </div>
  </section>

  <section id="famille">
    <div class="colonne">
      <h2>La famille, premier motif ?</h2>
      <p class="reponse">
        {#if etudesDevant}<strong>Plus depuis {etudesDevant.annee}</strong> : les études passent devant.{/if}
        En {c.dernier.annee}, {milliers(c.dernier.motifs.familial)} titres pour motif familial, soit {pctEntier(
          (100 * c.dernier.motifs.familial) / c.dernier.total
        )} du total, un nombre resté entre {milliers(c.familialMin)} et {milliers(c.familialMax)} depuis
        {c.premier.annee}. Stable en total, mais recomposé : les membres de famille de Français
        passent de {milliers(c.premier.famille.francais)} à {milliers(famDernier.francais)}, les
        membres de famille d’étrangers de {milliers(c.premier.famille.membre)} à {milliers(
          famDernier.membre
        )}.
      </p>
    </div>
    <TLCadre
      titre="Premiers titres pour motif familial, par catégorie, {c.premier.annee}-{c.dernier
        .annee}"
      lecture="en {c.dernier.annee}, {entier(
        famDernier.francais
      )} titres « famille de Français », {entier(famDernier.membre)} « membre de famille », {entier(
        famDernier.liens
      )} « liens personnels et familiaux »."
      source="Ministère de l’Intérieur (DSED)"
      champ="France, ressortissants de pays tiers"
      statut="définitif"
      fichiers={['titres.csv']}
    >
      <p class="legende-lignes">
        {#each serieFamille as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieFamille}
        marqueurs
        yFormat={(y) => `${virgule(y / 1000, 0)} k`}
        titre="Premiers titres pour motif familial, par catégorie"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          « Famille de Français » regroupe les titres délivrés aux membres de la famille d’un
          Français (conjoints, parents d’enfants français…). « Membre de famille » regroupe ceux des
          familles d’étrangers, dont le regroupement familial au sens du droit, la procédure par
          laquelle un étranger installé fait venir son conjoint et ses enfants ; les fichiers
          utilisés ici ne l’isolent pas. « Liens personnels et familiaux » désigne des personnes
          déjà en France, admises au séjour pour l’intensité de leurs attaches.
        </p>
      </Detail>
    </div>
  </section>

  <section id="asile">
    <div class="colonne">
      <h2>Asile et titres s’additionnent-ils ?</h2>
      <p class="reponse">
        <strong>Non</strong> : ce sont les étapes d’un même parcours. En {c.anAsile}, {milliers(
          c.premieres
        )} premières demandes d’asile ont été déposées ; {milliers(c.positives)} décisions de première
        instance sur {milliers(c.decisions)} ont accordé une protection ({pctEntier(
          (100 * c.positives) / c.decisions
        )}) ; {milliers(c.titresProtection)} premiers titres de réfugié ou de protection subsidiaire ont
        été délivrés. Additionner demandes et titres compterait deux fois les mêmes personnes.
      </p>
    </div>
    <TLCadre
      titre="Les étapes de l’asile en France, {c.anAsile}"
      lecture="en {c.anAsile}, {entier(
        c.premieres
      )} personnes ont demandé l’asile pour la première fois. Les décisions et les titres d’une année concernent en partie des demandes plus anciennes : ces barres ne décrivent pas une même cohorte."
      source="Eurostat (migr_asyappctza, migr_asydcfsta) pour les demandes et les décisions ; ministère de l’Intérieur (DSED) pour les titres"
      champ="France ; décisions de première instance (Office français de protection des réfugiés et apatrides), sans les recours"
      statut="définitif"
      fichiers={['eurostat.csv', 'titres.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'Premières demandes', valeurs: [c.premieres] },
          { libelle: 'Décisions (1re instance)', valeurs: [c.decisions] },
          { libelle: 'dont positives', valeurs: [c.positives] },
          { libelle: 'Premiers titres de protection', valeurs: [c.titresProtection] }
        ]}
        cles={[{ libelle: 'Personnes', couleur: 'var(--serie-1)' }]}
        format={(v) => milliers(v)}
        titre="Les étapes de l’asile en France en {c.anAsile}"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Les décisions négatives de première instance peuvent faire l’objet d’un recours devant la
          Cour nationale du droit d’asile, qui accorde à son tour des protections : elles ne sont
          pas dans ces chiffres. Les déboutés ne quittent pas tous la France ; ceux qui restent sans
          titre relèvent des personnes en situation irrégulière, que la statistique publique ne
          mesure qu’en fourchette (U7).
        </p>
      </Detail>
    </div>
  </section>

  <section id="deux-mesures">
    <div class="colonne">
      <h2>Pourquoi deux chiffres des arrivées ?</h2>
      <p class="reponse">
        En {data.anneeOrigines}, l’Insee compte
        <strong>{milliers(c.fluxOrigines.entreesImm)}</strong>
        immigrés entrés en France ; le ministère de l’Intérieur, {milliers(
          c.titresAnOrigines.total
        )}
        premiers titres de séjour. Ce ne sont ni les mêmes personnes ni la même mesure : {milliers(
          o['Europe']
        )} de ces immigrés sont nés en Europe, dont {milliers(nesUE)} nés dans un pays de l’Union européenne,
        et les citoyens européens n’ont pas besoin de titre ; à l’inverse, un premier titre peut être
        délivré des années après l’arrivée.
      </p>
    </div>
    <TLCadre
      titre="Entrées d’immigrés et premiers titres de séjour"
      lecture="en {data.anneeOrigines}, {entier(
        c.fluxOrigines.entreesImm
      )} entrées d’immigrés (Insee) et {entier(
        c.titresAnOrigines.total
      )} premiers titres (ministère de l’Intérieur). Les deux courbes ne s’additionnent pas."
      source="Insee, Insee Première 2107 (entrées estimées par le recensement) ; ministère de l’Intérieur (DSED)"
      champ="France hors Mayotte jusqu’en 2013, France ensuite (Insee) ; France, ressortissants de pays tiers (ministère)"
      statut="définitif"
      fichiers={['flux.csv', 'titres_totaux.csv', 'entrees_origine.csv']}
    >
      <p class="legende-lignes">
        {#each serieDeux as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieDeux}
        reperes={[{ x: 2014, libelle: '+ Mayotte (Insee)', style: 'champ' }]}
        marqueurs
        yFormat={(y) => `${virgule(y / 1000, 0)} k`}
        titre="Entrées d’immigrés selon l’Insee et premiers titres de séjour selon le ministère"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          L’Insee compte toute personne née étrangère à l’étranger qui s’installe en France pour au
          moins un an, quels que soient son âge, sa nationalité et sa situation administrative ; les
          personnes sans titre sont en partie captées par le recensement. Le ministère compte les
          titres délivrés aux ressortissants de pays hors de l’Union européenne : le titre n’est en
          principe obligatoire qu’à partir de 18 ans, et une régularisation produit un premier titre
          pour une personne arrivée plus tôt.
        </p>
        <p>
          Une entrée n’est pas non plus toujours celle d’un immigré : la même année, l’Insee compte
          {milliers(c.fluxOrigines.entreesNi)} entrées de non-immigrés, nés en France ou nés Français
          à l’étranger, qui s’installent ou reviennent.
        </p>
      </Detail>
    </div>
  </section>

  <section id="solde">
    <div class="colonne">
      <h2>Qu’y a-t-il dans le solde migratoire ?</h2>
      <p class="reponse">
        Deux mouvements de sens contraire. De {c.soldesDebut} à {c.soldesFin}, les entrées et les
        sorties d’immigrés ont ajouté <strong>{milliers(c.cumulImmigres)}</strong> personnes ; les
        non-immigrés, qui partent plus qu’ils ne reviennent, en ont retiré {milliers(
          -c.cumulNonImmigres
        )}{c.niToujoursNegatif ? ' : leur solde est négatif chaque année' : ''}.
      </p>
    </div>
    <TLCadre
      titre="Solde migratoire des immigrés et des non-immigrés, {c.soldesDebut}-{c.soldesFin}"
      lecture="en {c.soldesFin}, le solde des immigrés est de {signe(
        c.soldes.at(-1)!.immigres
      )} et celui des non-immigrés de {signe(
        c.soldes.at(-1)!.nonImmigres
      )}. Le solde migratoire de la France est la somme des deux. Les sorties d’immigrés de {c
        .sortiesMin.annee} ({milliers(
        c.sortiesMin.valeur
      )}) sont très en dessous des autres années ({milliers(c.sortiesAutresMin)} à {milliers(
        c.sortiesAutresMax
      )}) : le solde de cette année est sans doute surestimé (U2)."
      source="Insee, Insee Première 2107"
      champ="France hors Mayotte jusqu’en 2013, France ensuite. Non-immigrés : personnes nées en France ou nées françaises à l’étranger"
      statut="sorties estimées par différence (U2)"
      fichiers={['flux.csv']}
    >
      <p class="legende-lignes">
        {#each serieSoldes as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieSoldes}
        reperes={[{ x: 2014, libelle: '+ Mayotte', style: 'champ' }]}
        marqueurs
        yFormat={(y) => `${virgule(y / 1000, 0)} k`}
        titre="Solde migratoire des immigrés et des non-immigrés"
        infobulle={infobulleSoldes}
      />
      {#snippet tableau()}
        <table>
          <thead
            ><tr
              ><th>Année</th><th>Solde des immigrés</th><th>Entrées de non-immigrés</th><th
                >Sorties de non-immigrés</th
              ><th>Solde des non-immigrés</th></tr
            ></thead
          >
          <tbody>
            {#each c.soldes as s (s.annee)}
              <tr
                ><td>{s.annee}</td><td>{signe(s.immigres)}</td><td>{milliers(s.entreesNi)}</td><td
                  >{milliers(s.sortiesNi)}</td
                ><td>{signe(s.nonImmigres)}</td></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          « Il n’y a que des entrées » : le solde migratoire de la France est un solde, celui des
          immigrés moins le départ net des non-immigrés. Les sorties ne sont pas comptées
          directement : aucun registre ne note les départs, et l’Insee les estime par différence, ce
          qui les rend fragiles (U2). Ces soldes sont aussi ceux de la piscine.
        </p>
      </Detail>
    </div>
  </section>

  <section id="sans-titre">
    <div class="colonne">
      <h2>Et les personnes sans titre ?</h2>
      <p class="reponse">
        Aucune source publique ne les compte, et ce site ne leur donne pas de nombre (U7). Deux
        indices seulement. Fin 2024, <strong>{entier(irr.ame_beneficiaires_2024)}</strong> personnes
        bénéficiaient de l’aide médicale de l’État, réservée aux étrangers en situation irrégulière,
        dont {entier(irr.ame_outre_mer_2024)} outre-mer ; toutes les personnes sans titre ne la demandent
        pas. Et parmi les étrangers qui ont reçu en 2018 un premier titre de séjour,
        {irr.elipa_sans_papier_arrivee} % n’avaient aucun papier à leur arrivée en France, {irr.elipa_sans_papier_avant_demarches} %
        juste avant leurs démarches : l’irrégularité est souvent une étape du parcours, pas un état.
      </p>
    </div>
    <TLCadre
      titre="Primo-arrivants de 2018 sans aucun papier, à l’arrivée et avant les démarches"
      lecture="{irr.elipa_sans_papier_arrivee} % des étrangers qui ont reçu en 2018 un premier titre de séjour d’au moins un an n’avaient aucun papier à leur arrivée en France ; juste avant d’entamer leurs démarches, {irr.elipa_sans_papier_avant_demarches} %, surtout parce que des visas de courte durée avaient expiré."
      source="Ministère de l’Intérieur (DSED), enquête Elipa 2, L’essentiel sur Elipa 2 (2024), p. 22-23"
      champ="Primo-arrivants de 2018 détenteurs d’un titre de séjour de plus d’un an, hors titre étudiant, majeurs, résidant dans un des départements du champ de l’enquête"
      statut="enquête, déclaratif"
      fichiers={['irreguliers.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'À l’arrivée en France', valeurs: [irr.elipa_sans_papier_arrivee] },
          {
            libelle: 'Juste avant les démarches',
            valeurs: [irr.elipa_sans_papier_avant_demarches]
          }
        ]}
        cles={[{ libelle: 'Sans aucun papier', couleur: 'var(--serie-1)' }]}
        max={100}
        format={(v) => `${v} %`}
        titre="Part des primo-arrivants de 2018 sans aucun papier"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Elipa 2 montre aussi des séjours longs avant le premier titre : {irr.elipa_presence_2_ans_ou_moins} %
          des primo-arrivants de 2018 étaient en France depuis 2 ans ou moins quand ils l’ont
          obtenu, mais
          {irr.elipa_aes_5_ans} sur 10 des personnes régularisées par une admission exceptionnelle au
          séjour y étaient depuis 5 ans ou plus, et près de {irr.elipa_liens_personnels_avant_2010} titulaires
          sur 10 d’un titre « liens personnels et familiaux » étaient arrivés plus de neuf ans avant (DSED,
          <em>Infos migrations</em> n° 98, 2020).
        </p>
        <p>
          Le nombre de bénéficiaires de l’aide médicale de l’État vient du projet annuel de
          performances 2026 de la mission « Santé » (p. 78) ; il a augmenté de {irr.ame_variation_2024} %
          par rapport à 2023. Ce n’est pas une estimation du nombre de personnes sans titre : il en
          manque celles qui ne demandent pas l’aide, et ces chiffres ne s’additionnent ni aux stocks
          d’immigrés de l’Insee, qui en comptent déjà une partie, ni aux titres de séjour.
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
  .arr {
    --serie-1: #2a78d6;
    --cat-2: #7a5fb8;
    --cat-3: #1f8a7a;
  }
  @media (prefers-color-scheme: dark) {
    .arr {
      --serie-1: #3987e5;
      --cat-2: #a48bdb;
      --cat-3: #3fb3a1;
    }
  }
  section {
    margin-top: 2.5rem;
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
  .note {
    color: var(--gris);
    font-size: var(--t-0);
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
