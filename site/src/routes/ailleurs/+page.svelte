<script lang="ts">
  import TLCadre from '$lib/components/TLCadre.svelte';
  import TLLignes from '$lib/components/TLLignes.svelte';
  import TLBarres from '$lib/components/TLBarres.svelte';
  import Nuage from '$lib/components/Nuage.svelte';
  import Sommaire from '$lib/components/Sommaire.svelte';
  import Detail from '$lib/components/Detail.svelte';
  import { entier, milliers, millions, pct, virgule } from '$lib/format';
  import { mediane, negatifDepuis, rangTexte } from '$lib/comparaisons';

  let { data } = $props();
  const c = $derived(data.chiffres);
  const points = (x: number) =>
    `${x > 0 ? '+' : ''}${virgule(x)} point${Math.abs(x) >= 2 ? 's' : ''}`;
  const estFrance = (l: string) => l === 'France';

  // C1 : part des personnes nées à l'étranger.
  const lignesPart = $derived(
    [...data.nesEtranger]
      .sort((a, b) => b.part - a.part)
      .map((x) => ({ libelle: x.pays, valeurs: [x.part] }))
  );

  const tete = $derived(
    [...data.nesEtranger]
      .sort((a, b) => b.part - a.part)
      .slice(0, 3)
      .map((x) => x.pays)
  );

  // C2 : soldes naturel et migratoire en ‰, un pays à la fois.
  const negatifs = $derived(
    data.soldes.map((s) => ({
      pays: s.pays,
      depuis: negatifDepuis(s.points.map((p) => ({ annee: p.annee, valeur: p.naturel }))),
      debutSerie:
        negatifDepuis(s.points.map((p) => ({ annee: p.annee, valeur: p.naturel }))) ===
        s.points[0].annee
    }))
  );
  const autresNegatifs = $derived(negatifs.filter((n) => n.pays !== 'France' && n.depuis !== null));
  const franceNegatif = $derived(negatifs.find((n) => n.pays === 'France')!.depuis);
  let paysSoldes = $state('FR');
  const soldesPays = $derived(data.soldes.find((s) => s.geo === paysSoldes)!);
  const serieSoldes = $derived([
    {
      id: 'naturel',
      libelle: 'Solde naturel',
      couleur: 'var(--cat-3)',
      segments: [soldesPays.points.map((p) => ({ x: p.annee, y: p.naturel }))]
    },
    {
      id: 'migratoire',
      libelle: 'Solde migratoire (y c. ajustement)',
      couleur: 'var(--serie-1)',
      segments: [soldesPays.points.map((p) => ({ x: p.annee, y: p.migratoire }))]
    }
  ]);
  const soldesFr = $derived(data.soldes.find((s) => s.geo === 'FR')!.points);
  const dernierSolde = $derived(soldesFr.at(-1)!);

  // C3 : entrées permanentes par catégorie (OCDE), pour 10 000 habitants.
  const CATS = $derived([
    { k: 'travail', libelle: 'Travail', couleur: 'var(--serie-1)' },
    { k: 'famille', libelle: 'Famille', couleur: 'var(--cat-2)' },
    {
      k: 'famille_accompagnante',
      libelle: 'Famille accompagnant un travailleur',
      couleur: 'var(--cat-2b)'
    },
    { k: 'humanitaire', libelle: 'Humanitaire', couleur: 'var(--cat-3)' },
    { k: 'libre_circulation', libelle: 'Libre circulation', couleur: 'var(--cat-4)' },
    { k: 'autres', libelle: 'Autres', couleur: 'var(--cat-5)' }
  ] as const);
  const compare = (x: number, ref: number) =>
    Math.abs(x - ref) < 1 ? 'autant que' : x > ref ? 'plus que' : 'moins que';
  const medFamille = $derived(mediane(data.entrees.map((x) => x.cats.famille)));
  const medTravail = $derived(mediane(data.entrees.map((x) => x.cats.travail)));
  const lignesEntrees = $derived(
    [...data.entrees]
      .sort((a, b) => b.total - a.total)
      .map((x) => ({
        libelle: x.code === 'FRA' ? 'France' : x.pays,
        valeurs: CATS.map((k) => x.cats[k.k])
      }))
  );

  // C4 : asile, bascule nombre ↔ pour 10 000 habitants.
  let mesureAsile: 'relatif' | 'nombre' = $state('relatif');
  const lignesAsile = $derived(
    [...data.asile]
      .sort((a, b) =>
        mesureAsile === 'relatif' ? b.demandes10k - a.demandes10k : b.demandes - a.demandes
      )
      .map((x) => ({
        libelle: x.pays,
        valeurs: [mesureAsile === 'relatif' ? x.demandes10k : x.demandes]
      }))
  );
  const [p0, p1] = $derived(data.periodeAsile);
  const nAns = $derived(p1 - p0 + 1);

  // C7 : la bosse migratoire et l'émigration subsaharienne (ONU).
  const em = $derived(data.emigration);
  const q = $derived(em.quintiles);
  const qMax = $derived(q.reduce((a, b) => (b.mediane > a.mediane ? b : a)));
  const bosse = $derived(qMax !== q[0] && qMax !== q[q.length - 1]);
  const af = $derived(em.afrique);
  const partAbroad = $derived((100 * af.emigres) / (af.population + af.emigres));
  const partMemeRegion = $derived((100 * af.memeRegion) / af.emigres);
  const pctEntier = (x: number) => `${Math.round(x)} %`;
  const dollars = (x: number) =>
    x >= 1000 ? `${virgule(x / 1000, x >= 10000 ? 0 : 1)} k$` : `${Math.round(x)} $`;
  const pointsNuage = $derived(
    em.pays.map((p) => ({
      id: p.code,
      libelle: p.pays,
      x: p.pib,
      y: p.taux,
      poids: p.population,
      accent: p.pays === 'France'
    }))
  );

  const SOMMAIRE = $derived([
    {
      ancre: 'part',
      question: 'Plus d’immigrés que les voisins ?',
      chiffre: pct(c.fr.part),
      reponse: `de la population de la France est née à l’étranger en ${data.anNaiss} : ${rangTexte(c.rangPart)} pays sur ${c.nPart} en Europe${data.ue.part !== null ? `, pour ${pct(data.ue.part)} dans l’Union européenne` : ''}.`
    },
    {
      ancre: 'vitesse',
      question: 'Une hausse plus rapide qu’ailleurs ?',
      chiffre: points(c.progressionFr),
      reponse: `de ${data.anNaissDebut} à ${data.anNaiss} en France${c.progressionUe !== null ? `, ${points(c.progressionUe)} dans l’Union européenne` : ''} : ${rangTexte(c.rangProgression)} hausse sur ${c.nPart}.`
    },
    ...(c.entreesFr
      ? [
          {
            ancre: 'entrees',
            question: 'Combien d’entrées pour 10 000 habitants ?',
            chiffre: virgule(c.entreesFr.total, 0),
            reponse: `entrées à titre permanent par an pour 10 000 habitants en France (${data.periodeEntrees[0]}-${data.periodeEntrees[1]}) : ${rangTexte(c.rangEntrees!)} pays sur ${c.nEntrees} de l’OCDE.`
          }
        ]
      : []),
    {
      ancre: 'asile',
      question: 'La France, première terre d’asile ?',
      chiffre: rangTexte(c.rangAsileRel),
      reponse: `sur ${c.nAsile} pays européens pour les demandes d’asile rapportées à la population (${p0}-${p1}), ${rangTexte(c.rangAsileAbs)} en nombre.`
    },
    {
      ancre: 'bosse',
      question: 'Les plus pauvres émigrent-ils le plus ?',
      chiffre: bosse ? 'Non.' : `${virgule(q[0].mediane)} %`,
      reponse: bosse
        ? `${virgule(q[0].mediane)} % d’émigrés dans les pays les plus pauvres, ${virgule(qMax.mediane)} % dans les pays à revenu intermédiaire, ${virgule(q[q.length - 1].mediane)} % dans les plus riches (médianes, ${em.annee}).`
        : `d’émigrés dans les pays les plus pauvres (médiane, ${em.annee}).`
    },
    {
      ancre: 'afrique',
      question: 'Une « ruée » africaine ?',
      chiffre: pct(partAbroad),
      reponse: `des personnes nées en Afrique subsaharienne vivent hors de leur pays en ${em.annee} ; ${pctEntier(partMemeRegion)} d’entre elles dans un autre pays d’Afrique subsaharienne.`
    }
  ]);
</script>

<svelte:head>
  <title>Ailleurs · Qui remplace qui ?</title>
  <meta
    name="description"
    content="La France comparée aux autres pays européens et de l'OCDE : part des personnes nées à l'étranger, soldes naturel et migratoire, entrées et demandes d'asile rapportées à la population."
  />
</svelte:head>

<article class="page ail">
  <header class="colonne">
    <h1>La France parmi les autres</h1>
    <p class="chapeau">
      Un chiffre seul ne dit pas grand-chose : il faut le rapporter à la population et le comparer.
      Où se situe la France parmi les pays d’Europe et de l’OCDE, pour la part des personnes nées à
      l’étranger, pour les entrées et pour l’asile ?
    </p>
  </header>

  <Sommaire items={SOMMAIRE} />

  <section id="part">
    <div class="colonne">
      <h2>Plus d’immigrés que les voisins ?</h2>
      <p class="reponse">
        En {data.anNaiss}, <strong>{pct(c.fr.part)}</strong> des habitants de la France sont nés à
        l’étranger : la France est au {rangTexte(c.rangPart)} rang sur {c.nPart} pays européens{data
          .ue.part !== null
          ? `, ${c.fr.part > data.ue.part ? 'au-dessus de' : 'au-dessous de'} la part de l’Union européenne (${pct(data.ue.part)})`
          : ''}. Avec la définition française de l’immigré, qui exclut les Français nés à
        l’étranger, la part est de {pct(data.insee.part)}.
      </p>
    </div>
    <TLCadre
      titre="Part de la population née à l’étranger, {data.anNaiss}"
      lecture="en {data.anNaiss}, {pct(
        c.fr.part
      )} des habitants de la France sont nés dans un autre pays. La France est marquée en ocre."
      source="Eurostat, migr_pop3ctb (population au 1er janvier selon le pays de naissance)"
      champ="pays de l’Union européenne et de l’Association européenne de libre-échange ; « né à l’étranger » : né dans un autre pays, quelle que soit la nationalité (définition internationale, U12)"
      statut="provisoire pour la plupart des pays"
      fichiers={['eurostat.csv']}
    >
      <TLBarres
        lignes={lignesPart}
        cles={[{ libelle: 'Nés à l’étranger', couleur: 'var(--serie-1)' }]}
        format={(v) => pct(v)}
        titre="Part de la population née à l’étranger, pays européens, {data.anNaiss}"
        accent={estFrance}
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Deux définitions coexistent (U12). La statistique internationale compte les personnes nées
          à l’étranger : en France, {pct(c.fr.part)} selon Eurostat. L’Insee compte les immigrés, nés
          étrangers à l’étranger :
          {pct(data.insee.part)} en {data.insee.annee}{data.insee.statut === 'provisoire'
            ? ' (provisoire)'
            : ''}. L’écart correspond aux personnes nées françaises à l’étranger, que la statistique
          internationale compte et que l’Insee ne compte pas parmi les immigrés. Les parts les plus
          élevées : {tete.join(', ')}.
        </p>
      </Detail>
    </div>
  </section>

  <section id="vitesse">
    <div class="colonne">
      <h2>Une hausse plus rapide qu’ailleurs ?</h2>
      <p class="reponse">
        De {data.anNaissDebut} à {data.anNaiss}, la part des personnes nées à l’étranger a gagné
        <strong>{points(c.progressionFr)}</strong>
        en France{c.progressionUe !== null
          ? `, contre ${points(c.progressionUe)} dans l’Union européenne`
          : ''} : la France est au {rangTexte(c.rangProgression)} rang sur {c.nPart}.
      </p>
    </div>
    <TLCadre
      titre="Solde naturel et solde migratoire, pour 1 000 habitants"
      lecture="en {dernierSolde.annee}, en France, le solde naturel est de {virgule(
        dernierSolde.naturel
      )} ‰ et le solde migratoire de {virgule(
        dernierSolde.migratoire
      )} ‰. Quand le solde naturel passe sous zéro, il y a plus de décès que de naissances."
      source="Eurostat, demo_gind"
      champ="territoire de chaque pays à chaque date ; solde migratoire y compris l’ajustement statistique (U22)"
      statut="dernières années provisoires"
      fichiers={['eurostat.csv']}
    >
      <div class="bascule" role="group" aria-label="Pays affiché">
        {#each data.soldes as s (s.geo)}
          <button
            type="button"
            aria-pressed={paysSoldes === s.geo}
            onclick={() => (paysSoldes = s.geo)}>{s.pays}</button
          >
        {/each}
      </div>
      <p class="legende-lignes">
        {#each serieSoldes as s (s.id)}
          <span><b class="pastille" style:background={s.couleur}></b>{s.libelle}</span>
        {/each}
      </p>
      <TLLignes
        series={serieSoldes}
        yFormat={(y) => `${virgule(y, 0)} ‰`}
        titre="{soldesPays.pays} : solde naturel et solde migratoire pour 1 000 habitants"
        infobulle={(x) => {
          const p = soldesPays.points.find((v) => v.annee === x)!;
          return `${soldesPays.pays}, ${x} : naturel ${virgule(p.naturel)} ‰, migratoire ${virgule(p.migratoire)} ‰${p.provisoire ? ' · provisoire' : ''}`;
        }}
      />
    </TLCadre>
    <div class="colonne">
      {#if autresNegatifs.length}
        <p>
          Au dixième de ‰ près, le solde naturel est négatif chaque année : {autresNegatifs
            .map(
              (n) =>
                `${n.pays} depuis ${n.depuis}${n.debutSerie ? ' au moins (début de la série)' : ''}`
            )
            .join(', ')}{franceNegatif === null
            ? ' ; en France, il est resté positif'
            : franceNegatif === dernierSolde.annee
              ? ` ; en France, il passe sous zéro en ${franceNegatif}${dernierSolde.provisoire ? ' (provisoire)' : ''}`
              : ` ; en France, depuis ${franceNegatif}`}.
        </p>
      {/if}
      <Detail>
        <p>
          Le solde migratoire d’Eurostat est calculé par différence (croissance de la population
          moins solde naturel) : il absorbe les corrections de recensement, si bien qu’une année
          isolée peut tomber bas pour des raisons statistiques (U22). On lit ici des tendances.
        </p>
      </Detail>
    </div>
  </section>

  {#if c.entreesFr}
    <section id="entrees">
      <div class="colonne">
        <h2>Combien d’entrées pour 10 000 habitants ?</h2>
        <p class="reponse">
          De {data.periodeEntrees[0]} à {data.periodeEntrees[1]}, la France a accueilli en moyenne
          <strong>{virgule(c.entreesFr.total, 0)}</strong> migrants à titre permanent par an pour
          10 000 habitants : {rangTexte(c.rangEntrees!)} sur les {c.nEntrees} pays de l’OCDE qui publient
          les dix années ({rangTexte(c.rangEntreesHorsLC!)} sans la libre circulation européenne, que
          les pays hors d’Europe n’ont pas). Pour 10 000 habitants, la famille y compte pour {virgule(
            c.entreesFr.cats.famille,
            0
          )} entrées par an ({compare(c.entreesFr.cats.famille, medFamille)} dans le pays médian, {virgule(
            medFamille,
            0
          )}), le travail pour {virgule(c.entreesFr.cats.travail, 0)} ({compare(
            c.entreesFr.cats.travail,
            medTravail
          )} dans le pays médian, {virgule(medTravail, 0)}).
        </p>
      </div>
      <TLCadre
        titre="Entrées à titre permanent par catégorie, pour 10 000 habitants, moyenne {data
          .periodeEntrees[0]}-{data.periodeEntrees[1]}"
        lecture="de {data.periodeEntrees[0]} à {data
          .periodeEntrees[1]}, la France a accueilli chaque année {virgule(
          c.entreesFr.total,
          1
        )} migrants permanents pour 10 000 habitants, dont {virgule(
          c.entreesFr.cats.libre_circulation,
          1
        )} au titre de la libre circulation européenne."
        source="OCDE, base de données sur les migrations internationales (entrées standardisées) et population historique"
        champ="pays de l’OCDE qui publient les dix années ; migrations à caractère permanent, sans les étudiants ni les travailleurs temporaires (U23)"
        statut="dernière année parfois provisoire"
        fichiers={['ocde.csv']}
      >
        <TLBarres
          lignes={lignesEntrees}
          cles={CATS.map((k) => ({ libelle: k.libelle, couleur: k.couleur }))}
          mode="cumul"
          format={(v) => virgule(v, 0)}
          titre="Entrées à titre permanent par catégorie pour 10 000 habitants, pays de l’OCDE"
        />
      </TLCadre>
      <div class="colonne">
        <Detail>
          <p>
            L’OCDE range les entrées de chaque pays dans des catégories communes pour pouvoir les
            comparer. Ces chiffres ne sont pas les titres de séjour du ministère : les étudiants,
            nombreux parmi les premiers titres délivrés en France, n’y figurent pas (U23). Une
            catégorie qu’un pays ne publie pas (libre circulation hors d’Europe, par exemple) compte
            pour zéro.
          </p>
        </Detail>
      </div>
    </section>
  {/if}

  <section id="asile">
    <div class="colonne">
      <h2>La France, première terre d’asile ?</h2>
      <p class="reponse">
        En nombre, la France est au <strong>{rangTexte(c.rangAsileAbs)}</strong> rang des pays
        européens pour les premières demandes d’asile de {p0} à {p1}. Rapportée à sa population,
        elle passe au <strong>{rangTexte(c.rangAsileRel)}</strong> rang sur {c.nAsile}, avec {virgule(
          c.asileFr.demandes10k,
          0
        )} demandes par an pour 10 000 habitants{c.premierAsileRel
          ? `, contre ${virgule(c.premierAsileRel.valeur, 0)} pour le premier pays (${c.premierAsileRel.libelle})`
          : ''}.
      </p>
    </div>
    <TLCadre
      titre="Premières demandes d’asile, {p0}-{p1}"
      lecture={mesureAsile === 'relatif'
        ? `de ${p0} à ${p1}, la France a reçu en moyenne ${virgule(c.asileFr.demandes10k, 1)} premières demandes d’asile par an pour 10 000 habitants.`
        : `de ${p0} à ${p1}, la France a reçu ${entier(c.asileFr.demandes)} premières demandes d’asile.`}
      source="Eurostat, migr_asyappctza et demo_gind"
      champ="pays de l’Union européenne et de l’Association européenne de libre-échange qui publient chaque année de la période ; premières demandes (sans les réexamens)"
      statut="définitif"
      fichiers={['eurostat.csv']}
    >
      <div class="bascule" role="group" aria-label="Mesure affichée">
        <button
          type="button"
          aria-pressed={mesureAsile === 'relatif'}
          onclick={() => (mesureAsile = 'relatif')}>Pour 10 000 habitants, par an</button
        >
        <button
          type="button"
          aria-pressed={mesureAsile === 'nombre'}
          onclick={() => (mesureAsile = 'nombre')}>Nombre, cumul {p0}-{p1}</button
        >
      </div>
      <TLBarres
        lignes={lignesAsile}
        cles={[{ libelle: 'Premières demandes', couleur: 'var(--serie-1)' }]}
        format={(v) => (mesureAsile === 'relatif' ? virgule(v, 0) : milliers(v))}
        titre="Premières demandes d’asile, {mesureAsile === 'relatif'
          ? 'par an pour 10 000 habitants'
          : `en nombre, cumul ${p0}-${p1}`}"
        accent={estFrance}
      />
    </TLCadre>
    <TLCadre
      titre="« Prendre sa part » : la France dans l’Union européenne, {p0}-{p1}"
      lecture="de {p0} à {p1}, la France a reçu {pct(
        c.part.demandes
      )} des premières demandes d’asile de l’Union européenne et accordé {pct(
        c.part.positives
      )} des protections en première instance, pour {pct(c.part.population)} de sa population{c.part
        .pib !== null
        ? ` et ${pct(c.part.pib)} de son produit intérieur brut`
        : ''}."
      source="Eurostat (migr_asyappctza, migr_asydcfsta, demo_gind, nama_10_gdp)"
      champ="Union européenne à 27 ; population moyenne et PIB cumulé sur la période"
      statut="dernières années provisoires pour le PIB"
      fichiers={['eurostat.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'Population', valeurs: [c.part.population] },
          ...(c.part.pib !== null
            ? [{ libelle: 'Produit intérieur brut', valeurs: [c.part.pib] }]
            : []),
          { libelle: 'Premières demandes d’asile', valeurs: [c.part.demandes] },
          { libelle: 'Protections accordées (1re instance)', valeurs: [c.part.positives] }
        ]}
        cles={[{ libelle: 'Part de la France dans l’UE', couleur: 'var(--serie-1)' }]}
        format={(v) => pct(v)}
        titre="Part de la France dans l’Union européenne : population, PIB, demandes d’asile, protections"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Une demande n’est pas une protection : de {p0} à {p1}, la France a accordé en première
          instance {entier(c.asileFr.positives)} protections, soit {virgule(
            c.asileFr.positives10k,
            1
          )} par an pour 10 000 habitants ({rangTexte(c.rangPositivesRel)} rang sur {c.nAsile}). Les
          recours, qui accordent d’autres protections, ne sont pas comptés ici. Les Ukrainiens
          arrivés depuis 2022 relèvent pour la plupart d’un régime de protection temporaire,
          distinct de l’asile et compté à part ; seuls ceux qui ont demandé l’asile figurent dans
          ces {nAns} années de demandes.
        </p>
      </Detail>
    </div>
  </section>

  <section id="bosse">
    <div class="colonne">
      <h2>Les plus pauvres émigrent-ils le plus ?</h2>
      <p class="reponse">
        {#if bosse}<strong>Non</strong> : en {em.annee}, la part d’émigrés est de {virgule(
            q[0].mediane
          )} % dans le cinquième des pays les plus pauvres, monte à {virgule(qMax.mediane)} % dans les
          pays dont le PIB par habitant va de {dollars(qMax.de)} à {dollars(qMax.a)}, puis retombe à {virgule(
            q[q.length - 1].mediane
          )} % dans les plus riches (médianes). C’est la « bosse migratoire » : pour partir, il faut des
          ressources.{:else}En {em.annee}, la part d’émigrés est de {virgule(q[0].mediane)} % dans le
          cinquième des pays les plus pauvres et de {virgule(q[q.length - 1].mediane)} % dans les plus
          riches (médianes).{/if}
      </p>
    </div>
    <TLCadre
      titre="Part d’émigrés selon le PIB par habitant, {em.annee}"
      lecture="chaque disque est un pays ; plus il est haut, plus la part de ses natifs vivant à l’étranger est forte. Les traits épais donnent la médiane de chaque cinquième des pays, classés par PIB par habitant (échelle logarithmique). La France est en ocre."
      source="ONU DESA, International Migrant Stock 2024 et World Population Prospects 2024 ; ONU, Division de statistique (PIB par habitant)"
      champ="{em.pays
        .length} pays d’au moins un million d’habitants ; part d’émigrés = émigrés / (population résidente + émigrés) ; PIB par habitant en dollars courants (U24)"
      statut="estimations de l’ONU"
      fichiers={['onu_pays.csv']}
    >
      <Nuage
        points={pointsNuage}
        paliers={q.map((t) => ({ de: t.de, a: t.a, y: t.mediane }))}
        libellePaliers="Médiane de chaque cinquième des pays"
        xFormat={dollars}
        yFormat={(y) => `${virgule(y, 0)} %`}
        xTicks={[300, 1000, 3000, 10000, 30000, 100000]}
        titre="Part d’émigrés selon le PIB par habitant, {em.pays.length} pays, {em.annee}"
        infobulle={(p) => {
          const d = em.pays.find((x) => x.code === p.id)!;
          return `${d.pays} : ${virgule(d.taux)} % d’émigrés (${milliers(d.emigres)}), PIB ${dollars(d.pib)} par habitant`;
        }}
      />
      {#snippet tableau()}
        <table>
          <thead
            ><tr><th>Cinquième</th><th>PIB par habitant</th><th>Pays</th><th>Médiane</th></tr
            ></thead
          >
          <tbody>
            {#each q as t, i (i)}
              <tr
                ><td>{i + 1}</td><td>{dollars(t.de)} à {dollars(t.a)}</td><td>{t.n}</td><td
                  >{virgule(t.mediane)} %</td
                ></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Émigrer coûte : le voyage, les papiers, les réseaux. Les pays les plus pauvres ont moins
          de ressources pour partir ; les plus riches, moins de raisons. Une hausse du revenu d’un
          pays pauvre peut donc s’accompagner d’abord de plus de départs ; une photographie à une
          date ne le prouve pas à elle seule. Les écarts entre pays tiennent aussi aux guerres, à la
          taille et à la géographie : une médiane par tranche les lisse.
        </p>
      </Detail>
    </div>
  </section>

  <section id="afrique">
    <div class="colonne">
      <h2>Une « ruée » africaine ?</h2>
      <p class="reponse">
        En {em.annee}, <strong>{pct(partAbroad)}</strong> des personnes nées en Afrique
        subsaharienne vivent hors de leur pays de naissance, soit {millions(af.emigres)}. {partMemeRegion >
        50
          ? 'La plupart restent dans la région'
          : 'Une partie reste dans la région'} : {pctEntier(partMemeRegion)} vivent dans un autre pays
        d’Afrique subsaharienne,
        {pctEntier((100 * af.europeAmerique) / af.emigres)} en Europe ou en Amérique du Nord, dont {milliers(
          af.france
        )} en France.
      </p>
    </div>
    <TLCadre
      titre="Où vivent les émigrés d’Afrique subsaharienne, {em.annee}"
      lecture="en {em.annee}, {entier(
        af.emigres
      )} personnes nées en Afrique subsaharienne vivent dans un autre pays, dont {entier(
        af.memeRegion
      )} dans un autre pays de la région et {entier(af.france)} en France."
      source="ONU DESA, International Migrant Stock 2024 (tableaux 1 et 2) ; World Population Prospects 2024"
      champ="personnes nées en Afrique subsaharienne et vivant dans un autre pays que leur pays de naissance, au 1er juillet ; grandes régions des objectifs de développement durable (U24)"
      statut="estimations de l’ONU"
      fichiers={['onu_regions.csv']}
    >
      <TLBarres
        lignes={[
          { libelle: 'Autre pays d’Afrique subsaharienne', valeurs: [af.memeRegion] },
          { libelle: 'Europe et Amérique du Nord', valeurs: [af.europeAmerique] },
          { libelle: 'dont France', valeurs: [af.france] },
          { libelle: 'Afrique du Nord et Asie de l’Ouest', valeurs: [af.nordOuest] },
          {
            libelle: 'Ailleurs',
            valeurs: [af.emigres - af.memeRegion - af.europeAmerique - af.nordOuest]
          }
        ]}
        cles={[{ libelle: 'Émigrés', couleur: 'var(--serie-1)' }]}
        format={(v) => millions(v)}
        titre="Où vivent les émigrés d’Afrique subsaharienne en {em.annee}"
        accent={(l) => l === 'dont France'}
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Les projections démographiques ne disent pas combien partiront : ce sont des scénarios,
          pas des prévisions, et la bosse migratoire rappelle que le départ dépend des ressources
          autant que du nombre. Ce que l’on mesure aujourd’hui : une émigration faible rapportée à
          la population, et surtout régionale.
        </p>
      </Detail>
    </div>
  </section>

  <section class="colonne">
    <Detail
      encadre
      niveau={2}
      titre="Ce qu’on ne sait pas, et comment c’est montré"
      resume="Les limites des comparaisons de cette page ({data.incertitudes
        .map((u) => u.code)
        .join(', ')}) et la façon dont chacune apparaît."
    >
      <dl class="incertitudes">
        {#each data.incertitudes as u (u.code)}
          <dt><span class="code">{u.code}</span> {u.titre}</dt>
          <dd>
            {u.detail}
            <em>Ici : {u.traitement.charAt(0).toLowerCase() + u.traitement.slice(1)}.</em>
          </dd>
        {/each}
      </dl>
    </Detail>
  </section>
</article>

<style>
  .ail {
    --serie-1: #2a78d6;
    --cat-2: #7a5fb8;
    --cat-2b: #b9a6e3;
    --cat-3: #1f8a7a;
    --cat-4: #86b6ef;
    --cat-5: #acb3bc;
  }
  @media (prefers-color-scheme: dark) {
    .ail {
      --serie-1: #3987e5;
      --cat-2: #a48bdb;
      --cat-2b: #6d5a9e;
      --cat-3: #3fb3a1;
      --cat-4: #1c5cab;
      --cat-5: #5a636c;
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
