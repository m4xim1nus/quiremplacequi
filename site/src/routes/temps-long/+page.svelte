<script lang="ts">
  import TLCadre from '$lib/components/TLCadre.svelte';
  import TLLignes from '$lib/components/TLLignes.svelte';
  import TLFacettes from '$lib/components/TLFacettes.svelte';
  import TLBarres from '$lib/components/TLBarres.svelte';
  import Sommaire from '$lib/components/Sommaire.svelte';
  import Detail from '$lib/components/Detail.svelte';
  import { entier, milliers, pct } from '$lib/format';
  import { pts } from '$lib/generations';
  import { segments, changementsDeChamp, CHAMPS_LIBELLES } from '$lib/temps-long';

  let { data } = $props();
  const c = $derived(data.chiffres);

  const virgule = (x: number, n = 1) =>
    x.toLocaleString('fr-FR', { minimumFractionDigits: n, maximumFractionDigits: n });
  const points = (x: number) =>
    `${x > 0 ? '+' : ''}${virgule(x)} point${Math.abs(x) >= 2 ? 's' : ''}`;
  const pctEntier = (x: number) => `${Math.round(x)} %`;

  // B1 : bascule absolu ↔ part.
  let mesure: 'effectif' | 'part' = $state('part');
  const champs = $derived(changementsDeChamp(data.serie));
  const reperesB1 = $derived([
    ...champs.map((ch) => ({
      x: ch.annee,
      libelle: ch.champ === 'france' ? '+ Mayotte' : '+ outre-mer',
      style: 'champ' as const
    })),
    { x: 2024, libelle: 'rupture', style: 'rupture' as const }
  ]);
  const serieB1 = $derived([
    {
      id: 'immigres',
      libelle: 'Immigrés',
      couleur: 'var(--serie-1)',
      segments: segments(data.serie).map((seg) =>
        seg.map((p) => ({
          x: p.annee,
          y: mesure === 'part' ? p.part : p.immigres,
          etiquette:
            mesure === 'part'
              ? `${pct(p.part)} (${milliers(p.immigres)})`
              : `${milliers(p.immigres)} (${pct(p.part)})`
        }))
      )
    }
  ]);
  const infobulleB1 = (a: number) => {
    const p = data.serie.find((x) => x.annee === a)!;
    return `${milliers(p.immigres)} immigrés, ${pct(p.part)} de la population · ${CHAMPS_LIBELLES[p.champ]}${p.statut === 'provisoire' ? ' · provisoire' : ''}${p.rupture ? ' · rupture de série' : ''}`;
  };

  // B2.
  const yMaxNat = $derived(Math.max(...data.vagues.flatMap((v) => v.points.map((p) => p.part))));
  const yMaxPays = $derived(Math.max(...data.pays.flatMap((p) => p.points.map((x) => x.immigres))));
  const europe = $derived(data.vagues.filter((v) => v.groupe === 'europe'));
  const ailleurs = $derived(data.vagues.filter((v) => v.groupe !== 'europe'));
  const liste = (vs: typeof data.vagues) =>
    vs.map((v) => `les ${v.nationalite} en ${v.pic.annee} (${pct(v.pic.part)})`).join(', ');

  // B5 : couleurs de la rampe (ordinal) et des origines (catégoriel).
  const RAMPE = ['var(--r1)', 'var(--r2)', 'var(--r3)', 'var(--r4)'];

  const italiens = $derived(data.vagues.find((v) => v.nationalite === 'Italiens')!);

  // La page en cinq réponses : chaque chiffre est lu dans les données, comme dans les sections.
  const SOMMAIRE = $derived([
    {
      ancre: 'combien',
      question: 'Combien d’immigrés ?',
      chiffre: pct(c.dernier.part),
      reponse: `de la population en ${c.dernier.annee} (provisoire), contre ${pct(c.premier.part)} en ${c.premier.annee} et ${pct(c.pic1.part)} au premier sommet, en ${c.pic1.annee}.`
    },
    {
      ancre: 'vitesse',
      question: 'Plus vite qu’avant ?',
      chiffre: pts(data.vitesses.v1920.points),
      reponse: `de part des immigrés en dix ans dans les années 1920, contre ${points(data.vitesses.v2015.points)} de 2015 à 2025 (${points(data.vitesses.v2015Corrigee.points)} corrigé de la collecte de 2024). En nombre, la hausse récente est plus forte.`
    },
    {
      ancre: 'vagues',
      question: 'Comment une vague se tarit ?',
      chiffre: pct(italiens.pic.part),
      reponse: `de la population : les étrangers de nationalité italienne au plus haut, en ${italiens.pic.annee} ; ${pct(italiens.derniere.part)} en ${italiens.derniere.annee}. La plupart des vagues européennes montent, culminent puis refluent.`
    },
    {
      ancre: 'descendants',
      question: 'Que deviennent les descendants ?',
      chiffre: pctEntier(c.g3SudUn),
      reponse:
        'des petits-enfants d’immigrés d’Europe du Sud (18-59 ans) n’ont qu’un grand-parent immigré sur quatre.'
    },
    {
      ancre: 'recentes',
      question: 'Et les immigrations plus tardives ?',
      chiffre: pctEntier(c.g3MaghrebMoins18!),
      reponse: `des petits-enfants d’immigrés de moins de 18 ans ont un grand-parent venu du Maghreb, contre ${pctEntier(c.g3Maghreb18a59!)} chez les 18-59 ans.`
    }
  ]);
</script>

<svelte:head>
  <title>Le temps long · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Les immigrés en France depuis 1911, vague par vague : comment elles montent, se tarissent, et ce qu'il reste de leurs descendants."
  />
</svelte:head>

<article class="page tl">
  <header class="colonne">
    <h1>Le temps long</h1>
    <p class="chapeau">
      Belges, Italiens, Polonais, Espagnols, Portugais, Maghrébins : plusieurs vagues d’immigration
      ont suscité des discours d’hostilité, parfois d’« invasion ». Comment ces vagues sont-elles
      montées, comment se sont-elles taries, et que sont devenus leurs descendants ?
    </p>
  </header>

  <Sommaire items={SOMMAIRE} />

  <section id="combien">
    <div class="colonne">
      <h2>Combien d’immigrés, depuis quand ?</h2>
      <p class="reponse">
        <strong>Il n’y a jamais eu autant d’immigrés en France</strong> : {milliers(
          c.dernier.immigres
        )}
        en {c.dernier.annee}, soit <strong>{pct(c.dernier.part)}</strong> de la population (chiffre
        provisoire), contre {pct(c.premier.part)} en {c.premier.annee}. La hausse s’est faite par
        paliers, avec un premier sommet en {c.pic1.annee} ({pct(c.pic1.part)}).
      </p>
    </div>
    <TLCadre
      titre="Immigrés résidant en France, {data.serie[0].annee}-{c.dernier.annee}"
      lecture="en {c.pic1.annee}, {milliers(
        c.pic1.immigres
      )} immigrés vivaient en France métropolitaine, soit {pct(
        c.pic1.part
      )} de la population. Avant 2006, un point par recensement."
      source="Insee, recensements et estimations de population (séries 2381757 et 6793226)"
      champ="France métropolitaine jusqu’en 1982, hors Mayotte de 1990 à 2013, France depuis 2014 (traits pointillés). En 1911, le territoire recensé n’inclut pas l’Alsace-Moselle, allemande de 1871 à 1918"
      statut="2024 et 2025 provisoires ; rupture de série en 2024 (nouveau protocole de collecte), courbe interrompue"
      fichiers={['b1_stock.csv']}
    >
      <div class="bascule" role="group" aria-label="Mesure affichée">
        <button type="button" aria-pressed={mesure === 'part'} onclick={() => (mesure = 'part')}
          >Part de la population</button
        >
        <button
          type="button"
          aria-pressed={mesure === 'effectif'}
          onclick={() => (mesure = 'effectif')}>Nombre</button
        >
      </div>
      <TLLignes
        series={serieB1}
        reperes={reperesB1}
        marqueurs
        aire
        yFormat={mesure === 'part'
          ? (y) => `${virgule(y, 0)} %`
          : (y) => `${virgule(y / 1e6, 0)} M`}
        titre="Immigrés en France de {data.serie[0].annee} à {c.dernier.annee}, {mesure === 'part'
          ? 'en part de la population'
          : 'en nombre'}"
        infobulle={infobulleB1}
      />
      {#snippet tableau()}
        <table>
          <thead><tr><th>Année</th><th>Immigrés</th><th>Part</th><th>Champ</th></tr></thead>
          <tbody>
            {#each data.serie as p (p.annee)}
              <tr
                ><td>{p.annee}{p.statut === 'provisoire' ? ' (p)' : ''}</td><td
                  >{entier(p.immigres)}</td
                ><td>{pct(p.part)}</td><td>{CHAMPS_LIBELLES[p.champ]}</td></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          {milliers(c.premier.immigres)} immigrés en {c.premier.annee}. Après le sommet de {c.pic1
            .annee}, un reflux jusqu’à {pct(c.creux.part)} en {c.creux.annee}, un plateau entre {pct(
            c.plateauMin
          )} et {pct(c.plateauMax)} de 1975 à 1999, puis une reprise depuis les années 2000.
        </p>
        <p>
          Ces vagues ont suscité des discours d’hostilité : le massacre des Italiens d’Aigues-Mortes
          en 1893, étudié par Gérard Noiriel ; l’opinion de l’entre-deux-guerres, étudiée par Ralph
          Schor ; la crainte d’une « invasion » italienne en 1961, relevée par Jérémy Mourlane.
        </p>
      </Detail>
    </div>
  </section>

  <section class="colonne" id="vitesse">
    <h2>Plus vite qu’avant ?</h2>
    <p class="reponse">
      <strong
        >{data.vitesses.v2015Corrigee.effectif > data.vitesses.v1920.effectif
          ? 'En nombre, la hausse récente est la plus forte'
          : 'En nombre, la hausse des années 1920 reste la plus forte'}</strong
      >. Rapportée à la population, celle des années 1920 {data.vitesses.v1920.points >
      data.vitesses.v2015.points
        ? 'reste plus rapide'
        : 'n’est plus la plus rapide'} ({points(data.vitesses.v1920.points)} contre {points(
        data.vitesses.v2015.points
      )} sans correction, {points(data.vitesses.v2015Corrigee.points)} après correction).
    </p>
    <div class="tuiles">
      {#each [{ v: data.vitesses.v1920, note: '' }, { v: data.vitesses.v2010, note: '' }, { v: data.vitesses.v2015, note: 'brut, avec la rupture de 2024' }, { v: data.vitesses.v2015Corrigee, note: 'corrigé de l’effet de collecte de 2024' }] as t, i (i)}
        <div class="tuile">
          <span class="periode">{t.v.debut} → {t.v.fin}</span>
          <span class="grand">{points(t.v.points)}</span>
          <span>{milliers(t.v.effectif)} immigrés de plus</span>
          <span class="discret"
            >{milliers(t.v.effectifParAn)} par an en moyenne{t.note ? ` · ${t.note}` : ''}</span
          >
        </div>
      {/each}
    </div>
    <Detail>
      <p>
        Dans les années 1920, la part des immigrés est passée de {pct(
          data.vitesses.v1920.partDebut
        )}
        à {pct(data.vitesses.v1920.partFin)} : {points(data.vitesses.v1920.points)} en dix ans, soit
        {milliers(data.vitesses.v1920.effectif)} immigrés de plus. De 2015 à 2025, de {pct(
          data.vitesses.v2015.partDebut
        )} à {pct(data.vitesses.v2015.partFin)} : {points(data.vitesses.v2015.points)}, soit {milliers(
          data.vitesses.v2015.effectif
        )}
        de plus ; une fois retiré l’effet de la nouvelle collecte du recensement de 2024 ({milliers(
          data.vitesses.collecte
        )}), il reste {points(data.vitesses.v2015Corrigee.points)} et {milliers(
          data.vitesses.v2015Corrigee.effectif
        )} de plus.
      </p>
      <p class="note">
        Calcul sur la série ci-dessus (Insee). Le champ diffère : métropole en 1921-1931, France
        hors Mayotte en 2010, France ensuite ; l’entrée de Mayotte dans le champ, en 2014, ajoute
        environ {milliers(data.vitesses.mayotte)} immigrés à la décennie 2010-2020. L’effet de collecte
        de 2024 est l’estimation de l’Insee (note méthodologique de rupture de série), retirée du stock
        de 2025.
      </p>
    </Detail>
  </section>

  <section id="vagues">
    <div class="colonne">
      <h2>Comment une vague monte, puis se tarit ?</h2>
      <p class="reponse">
        La plupart des vagues européennes montent, culminent puis refluent. Les Italiens
        représentaient <strong>{pct(italiens.pic.part)}</strong> de la population en {italiens.pic
          .annee} ; {pct(italiens.derniere.part)} en {italiens.derniere.annee}.
      </p>
      <p class="avertissement">
        <strong>Attention au concept.</strong> Ces courbes comptent des <em>étrangers</em> par nationalité,
        seule mesure disponible avant 1968. Une baisse n’est pas forcément un départ : elle mêle les décès,
        les retours au pays et les naturalisations, qui font passer un étranger du côté des Français sans
        qu’il ait bougé (U9).
      </p>
    </div>
    <TLCadre
      titre="Étrangers par nationalité, en % de la population, 1901-2020"
      lecture="en 1931, les Italiens représentaient {pct(
        data.vagues.find((v) => v.nationalite === 'Italiens')!.points.find((p) => p.annee === 1931)!
          .part
      )} de la population. Toutes les facettes ont la même échelle."
      source="Insee Première n° 1910 (2022), encadré, d’après les recensements"
      champ="France métropolitaine"
      statut="parts publiées arrondies à 0,1 point (soit environ 20 000 à 60 000 personnes)"
      fichiers={['b2_nationalites.csv']}
    >
      <TLFacettes
        facettes={data.vagues.map((v) => ({
          titre: v.nationalite,
          points: v.points.map((p) => ({ x: p.annee, y: p.part }))
        }))}
        yFormat={(y) => `${virgule(y)} %`}
        xDomaine={[1901, 2020]}
        yMax={yMaxNat}
        xTicks={[1920, 1970, 2020]}
      />
      <p class="note">
        Algériens : avant 1962, ils étaient juridiquement français ; les recensements d’époque les
        comptaient à part, comme « musulmans algériens ». La série de l’Insee les range néanmoins
        avec les étrangers dès 1954 et 1962 (U9).
      </p>
      {#snippet tableau()}
        <table>
          <thead><tr><th>Nationalité</th><th>Pic</th><th>Année du pic</th><th>2020</th></tr></thead>
          <tbody>
            {#each data.vagues as v (v.nationalite)}
              <tr
                ><td>{v.nationalite}</td><td>{pct(v.pic.part)}</td><td>{v.pic.annee}</td><td
                  >{pct(v.derniere.part)}</td
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
          Les pics des vagues européennes : {liste(europe)}. Les vagues venues du Maghreb culminent
          plus tard : {liste(
            ailleurs.filter((v) => ['Algériens', 'Marocains', 'Tunisiens'].includes(v.nationalite))
          )} ; la part des Algériens remonte depuis 2010 ({pct(c.algerie2010.part)} en 2010, {pct(
            c.algerie2020.part
          )} en 2020). D’autres n’ont pas encore de pic : {c.enHausse
            .map((n) => n.charAt(0).toLowerCase() + n.slice(1))
            .join(', ')} sont à leur plus haut en 2020.
        </p>
      </Detail>

      <p>
        Depuis 1968, on suit aussi les immigrés par pays de naissance, naturalisés compris. Ceux nés
        en Espagne ou en Italie sont passés de {milliers(c.espIt.debut.immigres)} en {c.espIt.debut
          .annee} à {milliers(c.espIt.fin.immigres)} en {c.espIt.fin.annee}.
      </p>
    </div>
    <TLCadre
      titre="Immigrés par pays de naissance, 1968-2021"
      lecture="en {c.espIt.debut.annee}, {milliers(
        c.espIt.debut.immigres
      )} immigrés nés en Espagne ou en Italie vivaient en France. Même échelle pour toutes les facettes ; les Afriques sahélienne et guinéenne ne sont distinguées que depuis 2006."
      source="Insee, Immigrés et descendants d’immigrés, édition 2023 (6793226)"
      champ="France métropolitaine jusqu’en 1990, hors Mayotte de 1999 à 2013, France ensuite"
      statut="huit dates seulement ; 2021 provisoire : l’ensemble des immigrés y vaut {data
        .ensemble2021.pays !== null
        ? milliers(data.ensemble2021.pays)
        : '—'}, contre {data.ensemble2021.b1 !== null
        ? milliers(data.ensemble2021.b1)
        : '—'} dans la série réajustée ci-dessus"
      fichiers={['b2_pays.csv']}
    >
      <TLFacettes
        facettes={data.pays.map((p) => ({
          titre: p.pays,
          points: p.points.map((x) => ({ x: x.annee, y: x.immigres }))
        }))}
        yFormat={(y) => milliers(y)}
        xDomaine={[1968, 2021]}
        yMax={yMaxPays}
        xTicks={[1970, 1995, 2020]}
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Le stock des immigrés nés en Espagne ou en Italie baisse sous l’effet des décès et des
          retours, que la statistique ne mesure pas séparément. Les immigrés nés au Portugal sont
          presque aussi nombreux en {c.portugalFin.annee} ({milliers(c.portugalFin.immigres)}) qu’au
          plus haut des huit dates disponibles ({milliers(c.portugal.immigres)} en {c.portugal
            .annee}) ; ceux nés en Algérie passent de {milliers(c.algerie.debut.immigres)} en {c
            .algerie.debut.annee} à {milliers(c.algerie.fin.immigres)} en {c.algerie.fin.annee}.
        </p>
      </Detail>
    </div>
  </section>

  <section id="descendants">
    <div class="colonne">
      <h2>Que deviennent les descendants ?</h2>
      <p class="reponse">
        Ils se mêlent. Parmi les petits-enfants d’immigrés de 18 à 59 ans qui descendent de l’Europe
        du Sud, <strong>{pctEntier(c.g3SudUn)}</strong> n’ont qu’un seul grand-parent immigré sur
        quatre. Dès la deuxième génération, {pctEntier(c.g2SudUn)} des enfants d’immigrés d’Europe du
        Sud n’ont qu’un parent immigré.
      </p>
    </div>

    <TLCadre
      titre="Combien de grands-parents immigrés ? (G3 de 18 à 59 ans, selon l’origine)"
      lecture="parmi les petits-enfants d’immigrés de 18 à 59 ans ayant au moins un grand-parent venu d’Europe du Sud, {pctEntier(
        c.g3SudUn
      )} n’en ont qu’un seul immigré sur quatre."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 3a (pas le livre TeO2)"
      champ="petits-enfants d’immigrés de 18 à 59 ans, France métropolitaine, logement ordinaire"
      statut="enquêtes 2019-2020"
      fichiers={['ip1910.csv']}
    >
      <TLBarres
        mode="empile"
        lignes={data.g3Nombre.map((o) => ({ libelle: o.origine, valeurs: o.parts }))}
        cles={['Un', 'Deux', 'Trois', 'Quatre'].map((n, i) => ({
          libelle: `${n} grand-parent${i ? 's' : ''} immigré${i ? 's' : ''}`,
          couleur: RAMPE[i],
          texte: i === 0 ? 'var(--encre)' : 'var(--papier)'
        }))}
        format={pctEntier}
        titre="Répartition des petits-enfants d’immigrés selon le nombre de grands-parents immigrés"
      />
    </TLCadre>

    <TLCadre
      titre="Enfants d’immigrés (G2), tous âges : un ou deux parents immigrés, selon l’origine"
      lecture="{pctEntier(
        c.g2SudUn
      )} des enfants d’immigrés d’Europe du Sud n’ont qu’un parent immigré ; {pctEntier(
        c.g2EnsembleUn
      )} pour l’ensemble des enfants d’immigrés{data.g2ParentFrance !== null
        ? ` ; ${pctEntier(data.g2ParentFrance)} des enfants d’immigrés ont au moins un parent originaire de France`
        : ''}."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 3b"
      champ={data.champs.fig3b.replace(/^Champ : /, '').replace(/\.$/, '')}
      statut="enquête Emploi 2019-2020"
      fichiers={['ip1910.csv']}
    >
      <TLBarres
        mode="empile"
        lignes={data.g2.map((o) => ({ libelle: o.origine, valeurs: [o.un, o.deux] }))}
        cles={[
          { libelle: 'Un parent immigré', couleur: 'var(--r1)', texte: 'var(--encre)' },
          { libelle: 'Deux parents immigrés', couleur: 'var(--r3)' }
        ]}
        format={pctEntier}
        titre="Répartition des enfants d’immigrés selon le nombre de parents immigrés"
      />
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Les descendants des vagues européennes sont nombreux. En 2019-2020, {pctEntier(
            c.g3Sud18a59!
          )} des petits-enfants d’immigrés de 18 à 59 ans ont au moins un grand-parent venu d’Espagne,
          d’Italie ou du Portugal, et {pctEntier(c.g3SudFrance!)} ont aussi au moins un grand-parent originaire
          de France. Parmi ceux qui descendent de l’Europe du Sud, {pctEntier(c.g3SudQuatre)}
          ont quatre grands-parents immigrés.
        </p>
        <p>
          Ces chiffres d’IP 1910 (enquête Emploi et TeO2) diffèrent légèrement de ceux du livre TeO2
          cités sur la page Générations ({data.teo2UnGrandParent} % des petits-enfants d’immigrés de 18
          à 59 ans n’y ont qu’un grand-parent immigré) : mêmes enquêtes, regroupements et pondérations
          différents.
        </p>
      </Detail>
    </div>
  </section>

  <section id="recentes">
    <div class="colonne">
      <h2>Et les immigrations plus tardives ?</h2>
      <p class="reponse">
        Leur troisième génération est surtout jeune : <strong
          >{pctEntier(c.g3MaghrebMoins18!)}</strong
        >
        des petits-enfants d’immigrés de moins de 18 ans ont un grand-parent venu du Maghreb, contre
        {pctEntier(c.g3Maghreb18a59!)} chez les 18-59 ans.
      </p>
    </div>

    <TLCadre
      titre="Petits-enfants d’immigrés (G3) de moins de 18 ans et de 18 à 59 ans : origine de leurs grands-parents"
      lecture="{pctEntier(
        c.g3SudMoins18!
      )} des petits-enfants d’immigrés de moins de 18 ans ont au moins un grand-parent venu d’Espagne, d’Italie ou du Portugal. Un même petit-enfant peut avoir des grands-parents de plusieurs origines : les barres ne s’additionnent pas."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 3a, d’après l’enquête Emploi et TeO2 (pas le livre TeO2)"
      champ={data.champs.fig3a.replace(/^Champ : /, '').replace(/\.$/, '')}
      statut="enquêtes 2019-2020"
      fichiers={['ip1910.csv']}
    >
      <TLBarres
        lignes={data.g3Origines.map((o) => ({
          libelle: o.origine,
          valeurs: [o.moins18, o.de18a59]
        }))}
        cles={[
          { libelle: 'G3 de moins de 18 ans', couleur: 'var(--r1)' },
          { libelle: 'G3 de 18 à 59 ans', couleur: 'var(--r3)' }
        ]}
        format={pctEntier}
        max={100}
        titre="Part des petits-enfants d’immigrés ayant au moins un grand-parent de chaque origine"
      />
    </TLCadre>

    <TLCadre
      titre="Petits-enfants d’immigrés (G3) selon l’âge et l’origine des grands-parents, 0-59 ans"
      lecture="{data.g3Synthese
        .map(
          (o) =>
            `les petits-enfants d’immigrés ${o.origine === 'Maghreb' ? 'du Maghreb' : 'd’Europe du Sud'} représentent ${pct(o.moins18 ?? 0)} des 0-17 ans et ${pct(o.de18a59 ?? 0)} des 18-59 ans`
        )
        .join(
          ' ; '
        )}. Un petit-enfant peut compter dans plusieurs origines : la troisième génération issue du Maghreb est surtout jeune, celle d’Europe du Sud présente à tous les âges."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 2c"
      champ={data.champs.fig2c.replace(/^Champ : /, '').replace(/\.$/, '')}
      statut="enquêtes 2019-2020 ; G3 mesurés seulement avant 60 ans (U8)"
      fichiers={['ip1910.csv']}
    >
      <TLLignes
        series={data.g3Ages.map((o, k) => ({
          id: o.origine,
          libelle: o.origine.replace('Espagne, Italie, Portugal', 'Europe du Sud'),
          couleur: `var(--cat-${k + 1})`,
          segments: [o.points.map((p) => ({ x: p.i, y: p.part }))]
        }))}
        xFormat={(i) => data.classes[i] ?? ''}
        xTicks={[0, 2, 4, 6, 8, 10]}
        yFormat={(y) => `${virgule(y, 0)} %`}
        hauteur={260}
        marqueurs
        titre="Part de la classe d’âge ayant un grand-parent immigré de chaque origine"
      />
      <p class="legende-lignes">
        {#each data.g3Ages as o, k (o.origine)}
          <span
            ><b class="pastille" style:background="var(--cat-{k + 1})"></b>{o.origine.replace(
              'Espagne, Italie, Portugal',
              'Europe du Sud (Espagne, Italie, Portugal)'
            )}</span
          >
        {/each}
      </p>
    </TLCadre>
    <div class="colonne">
      <Detail>
        <p>
          Les lignées sont plus souvent homogènes : {pctEntier(c.g3MaghrebQuatre)} des petits-enfants
          d’immigrés de 18 à 59 ans d’origine maghrébine ont quatre grands-parents immigrés. Dès la deuxième
          génération, {pctEntier(c.g2MaghrebUn)} des enfants d’immigrés du Maghreb n’ont qu’un parent
          immigré, contre {pctEntier(c.g2SudUn)} pour l’Europe du Sud.
        </p>
      </Detail>
    </div>

    <aside class="nuance colonne">
      <h3>Un précédent, pas une preuve</h3>
      <p>
        Pour les descendants des migrations européennes de l’entre-deux-guerres, « la dynamique
        d’incorporation dans le groupe majoritaire est perceptible ». Mais « il est encore trop tôt
        pour savoir si les immigrations postcoloniales suivront la même dynamique démographique »
        (TeO2, chap. 8, §43).
      </p>
      <Detail>
        <p>
          Le groupe « Espagne, Italie, Portugal » des graphiques ci-dessus mêle d’ailleurs ces
          vagues anciennes et des arrivées d’après 1950. Ce précédent ne prouve pas que les
          immigrations venues du Maghreb, d’Afrique subsaharienne ou de Turquie suivront le même
          chemin, ni le contraire. Les auteurs de l’enquête TeO2 notent aussi que la saillance des
          origines s’éclaire par « l’expérience d’altérisation : le renvoi aux origines et les
          assignations » (chap. 9, §39), tout en soulignant que la causalité est difficile à
          établir.
        </p>
      </Detail>
    </aside>

    <aside class="nuance colonne">
      {#each data.incertitudes.filter((u) => u.code === 'U10') as u (u.code)}
        <h3>{u.titre}</h3>
        <p>{u.detail}</p>
      {/each}
    </aside>
  </section>

  <section class="colonne">
    <Detail
      encadre
      niveau={2}
      titre="Ce qu’on ne sait pas, et comment c’est montré"
      resume="Les limites des séries de cette page ({data.incertitudes
        .map((u) => u.code)
        .join(', ')}) et la façon dont chacune apparaît dans les graphiques."
    >
      <dl class="incertitudes">
        {#each data.incertitudes as u (u.code)}
          <dt><span class="code">{u.code}</span> {u.titre}</dt>
          <dd>{u.detail} <em>Ici : {u.traitement.toLowerCase()}.</em></dd>
        {/each}
      </dl>
    </Detail>
  </section>
</article>

<style>
  .tl {
    --serie-1: #2a78d6;
    --cat-1: #2a78d6;
    --cat-2: #7a5fb8; /* violet : aucune couleur d'alerte codée par origine */
    --cat-3: #1f8a7a;
    --r1: #86b6ef;
    --r2: #3987e5;
    --r3: #1c5cab;
    --r4: #0d366b;
  }
  @media (prefers-color-scheme: dark) {
    .tl {
      --serie-1: #3987e5;
      --cat-1: #3987e5;
      --cat-2: #a48bdb;
      --cat-3: #3fb3a1;
      --r1: #9ec5f4;
      --r2: #5598e7;
      --r3: #2a78d6;
      --r4: #184f95;
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
  .tuiles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
    gap: 1rem;
    margin: 1rem 0;
  }
  .tuile {
    display: flex;
    flex-direction: column;
    border-left: 3px solid var(--serie-1);
    padding: 0.25rem 0 0.25rem 0.9rem;
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .tuile .periode {
    font-weight: 600;
    color: var(--encre);
  }
  .tuile .grand {
    font-size: var(--t-4);
    font-weight: 700;
    color: var(--encre);
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
  }
  .discret,
  .note {
    color: var(--gris);
    font-size: var(--t-0);
  }
  .avertissement,
  .nuance {
    border-left: 3px solid var(--reglure);
    padding-left: 1rem;
  }
  .nuance h3 {
    font-size: var(--t-1);
    margin: 0.5rem 0;
  }
  .nuance {
    margin: 2rem 0;
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
