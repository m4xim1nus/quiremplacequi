<script lang="ts">
  import TLCadre from '$lib/components/TLCadre.svelte';
  import TLLignes from '$lib/components/TLLignes.svelte';
  import TLFacettes from '$lib/components/TLFacettes.svelte';
  import TLBarres from '$lib/components/TLBarres.svelte';
  import { entier, milliers, pct } from '$lib/format';
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
      Belges, Italiens, Polonais, Espagnols, Portugais, Maghrébins : chaque vague d’immigration a
      suscité son discours de l’« invasion ». Comment ces vagues sont-elles montées, comment se
      sont-elles taries, et que sont devenus leurs descendants ?
    </p>
    <p class="brouillon">Page en construction. Textes en brouillon, à valider.</p>
  </header>

  <section>
    <div class="colonne">
      <h2>Combien d’immigrés, depuis quand ?</h2>
      <p>
        <strong>Il n’y a jamais eu autant d’immigrés en France</strong> : {milliers(
          c.dernier.immigres
        )}
        en {c.dernier.annee} ({pct(c.dernier.part)} de la population, chiffre provisoire), contre
        {milliers(c.premier.immigres)} en {c.premier.annee} ({pct(c.premier.part)}). Mais la hausse
        s’est faite par paliers : un premier sommet en {c.pic1.annee} ({pct(c.pic1.part)}), un
        reflux jusqu’à {pct(c.creux.part)} en {c.creux.annee}, un plateau entre {pct(c.plateauMin)} et
        {pct(c.plateauMax)} de 1975 à 1999, puis une reprise depuis les années 2000.
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
      champ="France métropolitaine jusqu’en 1982, hors Mayotte de 1990 à 2013, France depuis 2014 (traits pointillés)"
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
  </section>

  <section class="colonne">
    <h2>Plus vite qu’avant ?</h2>
    <p>
      Dans les années 1920, la part des immigrés est passée de {pct(data.vitesses.v1920.partDebut)} à
      {pct(data.vitesses.v1920.partFin)} :
      <strong>{points(data.vitesses.v1920.points)}</strong> en dix ans, soit {milliers(
        data.vitesses.v1920.effectif
      )} immigrés de plus. Dans les années 2010, de {pct(data.vitesses.v2010.partDebut)} à {pct(
        data.vitesses.v2010.partFin
      )} : <strong>{points(data.vitesses.v2010.points)}</strong>, soit {milliers(
        data.vitesses.v2010.effectif
      )} de plus. En nombre, les deux décennies se valent ; rapportée à la population, la hausse des années
      1920 a été {data.vitesses.v1920.points > data.vitesses.v2010.points
        ? 'nettement plus rapide'
        : 'moins rapide'}.
    </p>
    <div class="tuiles">
      {#each [data.vitesses.v1920, data.vitesses.v2010] as v (v.debut)}
        <div class="tuile">
          <span class="periode">{v.debut} → {v.fin}</span>
          <span class="grand">{points(v.points)}</span>
          <span>{milliers(v.effectif)} immigrés de plus</span>
          <span class="discret">{milliers(v.effectifParAn)} par an en moyenne</span>
        </div>
      {/each}
    </div>
    <p class="note">
      Calcul sur la série ci-dessus (Insee). Le champ diffère : métropole en 1921-1931, France en
      2010-2020 (hors Mayotte en 2010).
    </p>
  </section>

  <section>
    <div class="colonne">
      <h2>Vague par vague</h2>
      <p>
        Chaque vague monte, culmine puis reflue. Parmi les nationalités européennes : {liste(
          europe
        )}. Puis {liste(ailleurs.slice(0, 4))}. Aujourd’hui, les Italiens ne représentent plus que {pct(
          data.vagues.find((v) => v.nationalite === 'Italiens')!.derniere.part
        )} de la population.
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
      <p>
        Depuis 1968, on suit les immigrés par pays de naissance, naturalisés compris. Les immigrés
        nés en Espagne ou en Italie étaient {milliers(c.espIt.debut.immigres)} en {c.espIt.debut
          .annee}, {milliers(c.espIt.fin.immigres)} en {c.espIt.fin.annee} : la vague s’écoule par les
        décès et les retours. Les immigrés nés au Portugal culminent en {c.portugal.annee}
        ({milliers(c.portugal.immigres)}) ; ceux nés en Algérie passent de {milliers(
          c.algerie.debut.immigres
        )} en {c.algerie.debut.annee} à {milliers(c.algerie.fin.immigres)} en {c.algerie.fin.annee}.
      </p>
    </div>
    <TLCadre
      titre="Immigrés par pays de naissance, 1968-2021"
      lecture="en {c.espIt.debut.annee}, {milliers(
        c.espIt.debut.immigres
      )} immigrés nés en Espagne ou en Italie vivaient en France. Même échelle pour toutes les facettes ; les Afriques sahélienne et guinéenne ne sont distinguées que depuis 2006."
      source="Insee, Immigrés et descendants d’immigrés, édition 2023 (6793226)"
      champ="France métropolitaine jusqu’en 1990, hors Mayotte de 1999 à 2013, France ensuite"
      statut="huit dates seulement ; 2021 provisoire"
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
  </section>

  <section>
    <div class="colonne">
      <h2>Ce qu’il reste d’une vague</h2>
      <p>
        Les descendants des vagues européennes sont partout. En 2019-2020, <strong
          >{pctEntier(c.g3Sud18a59!)} des petits-enfants d’immigrés de 18 à 59 ans ont au moins un grand-parent
          venu d’Espagne, d’Italie ou du Portugal</strong
        >, et {pctEntier(c.g3SudFrance!)} ont aussi au moins un grand-parent originaire de France. Parmi
        ceux qui descendent de l’Europe du Sud, {pctEntier(c.g3SudUn)} n’ont qu’un seul grand-parent immigré
        sur quatre ; {pctEntier(c.g3SudQuatre)} en ont quatre. Dès la deuxième génération, {pctEntier(
          c.g2SudUn
        )} des enfants d’immigrés d’Europe du Sud n’ont qu’un parent immigré.
      </p>
      <p>
        Chez les plus jeunes, les origines changent : parmi les petits-enfants d’immigrés de moins
        de 18 ans, {pctEntier(c.g3MaghrebMoins18!)} ont un grand-parent venu du Maghreb, contre {pctEntier(
          c.g3Maghreb18a59!
        )} chez les 18-59 ans. Les lignées sont plus souvent homogènes : {pctEntier(
          c.g3MaghrebQuatre
        )}
        des petits-enfants d’immigrés de 18 à 59 ans d’origine maghrébine ont quatre grands-parents immigrés,
        et {pctEntier(c.g2MaghrebUn)} des enfants d’immigrés du Maghreb n’ont qu’un parent immigré (contre
        {pctEntier(c.g2SudUn)} pour l’Europe du Sud).
      </p>
    </div>

    <TLCadre
      titre="Petits-enfants d’immigrés (G3) : origine de leurs grands-parents"
      lecture="{pctEntier(
        c.g3SudMoins18!
      )} des petits-enfants d’immigrés de moins de 18 ans ont au moins un grand-parent venu d’Espagne, d’Italie ou du Portugal. Un même petit-enfant peut avoir des grands-parents de plusieurs origines : les barres ne s’additionnent pas."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 3a, d’après l’enquête Emploi et TeO2"
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
      titre="Combien de grands-parents immigrés ? (G3 de 18 à 59 ans, selon l’origine)"
      lecture="parmi les petits-enfants d’immigrés de 18 à 59 ans ayant au moins un grand-parent venu d’Europe du Sud, {pctEntier(
        c.g3SudUn
      )} n’en ont qu’un seul immigré sur quatre."
      source="Insee Première n° 1910 (2022, révisé 2023), figure 3a"
      champ={data.champs.fig3a.replace(/^Champ : /, '').replace(/\.$/, '')}
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
      titre="Enfants d’immigrés (G2) : un ou deux parents immigrés, selon l’origine"
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

    <TLCadre
      titre="Petits-enfants d’immigrés selon l’âge : une vague chasse l’autre"
      lecture="les petits-enfants d’immigrés d’Europe du Sud sont surtout adultes, ceux du Maghreb surtout enfants : la troisième génération des vagues postcoloniales est encore jeune."
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

    <aside class="nuance colonne">
      <h3>Un précédent, pas une preuve</h3>
      <p>
        Les vagues européennes de l’entre-deux-guerres se sont fondues dans la population. Cela ne
        prouve pas que les immigrations venues du Maghreb, d’Afrique subsaharienne ou de Turquie
        suivront le même chemin, ni le contraire. Les auteurs de l’enquête TeO2 l’écrivent : « Il
        est encore trop tôt pour savoir si les immigrations postcoloniales suivront la même
        dynamique démographique » (TeO2, chap. 8, §43). Ils notent aussi que la saillance des
        origines s’éclaire en partie par « l’expérience d’altérisation : le renvoi aux origines et
        les assignations » (chap. 9, §39), tout en soulignant que la causalité est difficile à
        établir.
      </p>
    </aside>

    <aside class="encadre colonne">
      <h3>Ce que la statistique ne voit pas</h3>
      {#each data.incertitudes.filter((u) => u.code === 'U10') as u (u.code)}
        <p>{u.detail}</p>
      {/each}
    </aside>
  </section>

  <section class="colonne">
    <h2>Ce qu’on ne sait pas, et comment c’est montré</h2>
    <dl class="incertitudes">
      {#each data.incertitudes as u (u.code)}
        <dt><span class="code">{u.code}</span> {u.titre}</dt>
        <dd>{u.detail} <em>Ici : {u.traitement.toLowerCase()}.</em></dd>
      {/each}
    </dl>
  </section>
</article>

<style>
  .tl {
    --serie-1: #2a78d6;
    --cat-1: #2a78d6;
    --cat-2: #eb6834;
    --cat-3: #1baf7a;
    --r1: #86b6ef;
    --r2: #3987e5;
    --r3: #1c5cab;
    --r4: #0d366b;
  }
  @media (prefers-color-scheme: dark) {
    .tl {
      --serie-1: #3987e5;
      --cat-1: #3987e5;
      --cat-2: #d95926;
      --cat-3: #199e70;
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
    border-radius: 999px;
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
  .nuance,
  .encadre {
    border-left: 3px solid var(--reglure);
    padding-left: 1rem;
  }
  .nuance h3,
  .encadre h3 {
    font-size: var(--t-1);
    margin: 0.5rem 0;
  }
  .nuance,
  .encadre {
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
