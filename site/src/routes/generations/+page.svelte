<script lang="ts">
  import GENFigure from '$lib/components/GENFigure.svelte';
  import GENCurseur from '$lib/components/GENCurseur.svelte';
  import GENEmpile from '$lib/components/GENEmpile.svelte';
  import GENBarres from '$lib/components/GENBarres.svelte';
  import GENPoints from '$lib/components/GENPoints.svelte';
  import { pc, pts } from '$lib/generations';

  let { data } = $props();
  const d = $derived(data.d);
  const e1 = $derived(d.e1);
  const virgule = (x: number) => x.toFixed(1).replace('.', ',');
  const p = (cle: string) => e1.paliers.find((x) => x.cle === cle)!;
  const ligneE2 = (i: number) => d.e2.lignes[i];

  // Rampe des générations (celle de la piscine) et couleurs des catégories.
  const COUL_PALIERS: Record<string, string> = {
    g1: 'var(--t4)',
    g2a: 'var(--t3)',
    g2b: 'var(--t2)',
    g3: 'var(--t1)',
    om: 'var(--neutre-1)',
    conjoints: 'var(--neutre-2)'
  };
  const TEINTE = ['var(--t0)', 'var(--t1)', 'var(--t2)', 'var(--t3)', 'var(--t4)'];
  const LEG_E2 = $derived(
    d.e2.colonnes.map((c, i) => ({
      cle: c,
      libelle: c.replace(/^\([a-e]\) /, ''),
      couleur: `var(--o${4 - i})`,
      claire: i >= 3
    }))
  );
  const LEG_GP = ['1', '2', '3', '4'].map((n, i) => ({
    cle: n,
    libelle: `${n} grand-parent${n === '1' ? '' : 's'} immigré${n === '1' ? '' : 's'}`,
    couleur: `var(--o${i === 0 ? 0 : i + 1})`,
    claire: i === 0
  }));
  const seg = $derived(d.e9.segregation);
  const cho = $derived(d.e9.chomage);
  const choG1Maghreb = $derived(cho.find((x) => x.libelle === 'G1 Maghreb')!);
  const choG2Maghreb = $derived(cho.find((x) => x.libelle === 'G2 Maghreb')!);
  const dis = $derived(d.e9.discriminations);
  const disDe = (l: string) => dis.find((x) => x.libelle === l)!.valeur;
  const ide = $derived(d.e10.identification);
  const effectifs = $derived(d.e3.origines.map((o) => o.effectif));
  const doublon = (n: number) => effectifs.filter((x) => x === n).length > 1;
  const doublonValeur = $derived(effectifs.find((n) => doublon(n)));
  const quatreGp = (o: string) =>
    d.e3.origines.find((x) => x.libelle === o)!.segments.find((s) => s.cle === '4')!.valeur;
</script>

<svelte:head>
  <title>Générations · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Combien sont les immigrés, leurs enfants et leurs petits-enfants ? Mixité des couples, généalogies, inégalités et discriminations : l'enquête TeO2 (Ined-Insee)."
  />
</svelte:head>

<article class="page generations">
  <header class="colonne">
    <h1>Générations</h1>
    <p class="chapeau">
      Combien sont-ils ? Tout dépend de qui l’on compte. Et que deviennent les enfants d’immigrés :
      un bloc à part, ou une population qui se mêle aux autres ? Avec, en regard, les inégalités et
      les discriminations déclarées, y compris par les enfants nés en France.
    </p>
    <p class="brouillon">
      Page en construction. Textes en brouillon. Les chiffres viennent de l’enquête Trajectoires et
      Origines 2 (Ined-Insee, collecte 2019-2020, livre paru en 2026), ressaisis à la main avec une
      référence par cellule, et de l’Insee (IP 1910).
    </p>
  </header>

  <section class="colonne">
    <h2>Combien sont-ils ? Ça dépend de qui l’on compte</h2>
    <p>
      Avec la définition de l’immigré (né étranger à l’étranger), {pc(p('g1').cumul)} des 18-59 ans vivant
      en métropole. En y ajoutant les enfants d’immigrés, puis leurs petits-enfants, on passe à
      {pc(p('g3').cumul)}. Le chiffre de {pc(e1.total41)}, souvent cité, compte en plus les
      originaires des outre-mer et leurs enfants ({pc(e1.om)}), puis d’autres liens ({pc(
        e1.conjoints
      )}, part déduite :
      {pc(e1.total41)} moins les autres crans) : selon la note 6 du chapitre, surtout des conjoints, mais
      aussi les petits-enfants d’originaires des outre-mer et les conjoints de descendants plus lointains.
      Du premier au dernier cran, le chiffre est multiplié par {virgule(e1.etendue)}. Un chiffre à
      une date ne dit rien de la croissance : il change surtout avec la définition.
    </p>
    <GENFigure
      titre="La part de la population « liée à l’immigration », selon la définition"
      lecture="en comptant les immigrés, leurs enfants et leurs petits-enfants, {pc(
        p('g3').cumul
      )} des 18-59 ans ont un lien à l’immigration sur trois générations."
      source="TeO2 (Ined-Insee, 2026), ch. 8, tableau 1 et texte du §19 (41 %, note 6)"
      champ={d.champs.teo2_18_59}
      statut="Saisi ; le cran « conjoints et autres liens » est déduit (41 % moins la somme des autres crans)"
      badges={['U14']}
    >
      <GENCurseur paliers={e1.paliers} couleurs={COUL_PALIERS} champ="18-59 ans" />
      {#snippet tableau()}
        <table>
          <thead><tr><th>Groupe</th><th>Part</th><th>Cumul</th></tr></thead>
          <tbody>
            {#each e1.paliers as x (x.cle)}
              <tr
                ><td>{x.libelle}{x.deduit ? ' (déduit)' : ''}</td><td>{pc(x.ajout)}</td><td
                  >{pc(x.cumul)}</td
                ></tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </GENFigure>

    <p>
      L’Insee fait le même compte sur les 0-59 ans, enfants compris : {pc(e1.ip1910[0].cumul)}
      d’immigrés, {pc(e1.ip1910[2].cumul)} avec leurs enfants, {pc(e1.ip1910[3].cumul)} avec leurs petits-enfants.
      Sur la même tranche des 18-59 ans, l’Insee arrive à {pc(e1.ip1910_18_59)}, contre
      {pc(p('g3').cumul)} dans TeO2 : les deux sources et leurs méthodes diffèrent (enquête Emploi d’un
      côté, enquête spécialisée de l’autre).
    </p>
    <GENFigure
      titre="Le même compte chez les 0-59 ans (Insee)"
      lecture="{pc(e1.ip1910[3].ajout)} des 0-59 ans sont des petits-enfants d’immigrés."
      source="Insee Première 1910 (2022, révisé 2023), figure 1 (enquête Emploi 2019-2020 et TeO2)"
      champ={d.champs.ip1910}
      statut="Publié en tableur (lu par script)"
      csv="ip1910.csv"
      badges={['U8']}
    >
      <GENEmpile
        lignes={[
          {
            libelle: '0-59 ans',
            segments: e1.ip1910.map((x) => ({ cle: x.cle, valeur: x.ajout })),
            fin: `= ${pc(e1.ip1910[3].cumul)}`
          }
        ]}
        legende={e1.ip1910.map((x) => ({
          cle: x.cle,
          libelle: x.libelle,
          couleur: COUL_PALIERS[x.cle],
          claire: x.cle === 'g3'
        }))}
      />
    </GENFigure>

    <aside class="contradicteurs">
      <h3>Ce que disent les contradicteurs</h3>
      <p class="etat">
        Brouillon. D’après le résumé publié : la note complète n’a pas encore été lue.
      </p>
      <p>
        <strong>La version forte.</strong> L’Observatoire de l’immigration et de la démographie a publié
        le 21 septembre 2026 une note intitulée « Les scénarios démographiques de la France au XXIe siècle
        », qui projette la population par origine sur trois générations. D’après son résumé, les personnes
        « sans ascendance migratoire » y deviendraient minoritaires dans certains scénarios, et l’émigration,
        y compris celle des natifs, n’y est pas modélisée.
      </p>
      <p>
        <strong>L’argument du site</strong>, qui répond à une projection par une photo de 2019-2020
        : la catégorie « sans ascendance » rétrécit mécaniquement quand on compte plus de
        générations.
        {pc(e1.sansAscendance.deuxGenerations)} des 18-59 ans ne sont ni immigrés ni enfants d’immigrés,
        mais
        {pc(e1.sansAscendance.troisGenerations)} seulement n’ont aucun parent ni grand-parent immigré
        (originaires des outre-mer et Français de l’étranger compris dans ce dernier chiffre). Compter
        une génération de plus fait baisser la part des « sans ascendance », même sans nouvelle arrivée.
        La définition de l’ascendance retenue par la note n’étant pas connue, on ne peut pas dire si elle
        produit cet effet.
      </p>
      <p>
        Le mélange, lui, est mesuré. {pc(e1.g3Un)} des petits-enfants d’immigrés de 18 à 59 ans n’ont
        qu’un grand-parent immigré sur quatre ; chez les moins de 18 ans, les plus concernés par une projection,
        c’est {pc(e1.g3Moins18.un)}, et {pc(e1.g3Moins18.quatre)} en ont quatre (Insee, IP 1910, fig.
        3a). Selon TeO2 (ch. 8, §39), la mixité s’installe dès la génération des grands-parents pour
        {pc(e1.lignages.grandsParents)} des petits-enfants d’immigrés, et à la génération des parents
        pour
        {pc(e1.lignages.parents)}.
      </p>
      <p class="etat">
        À vérifier avant publication : le contenu exact de la note (scénarios, fécondité, mixité,
        définition de l’ascendance). La contre-projection viendra avec le mode projection de la
        piscine.
      </p>
    </aside>
  </section>

  <section class="colonne">
    <h2>Avec qui vivent-ils ?</h2>
    <p>
      {pc(ligneE2(0).mixte)} des immigrés en couple vivent avec un conjoint d’une autre origine, dont
      {pc(ligneE2(0).majoritaire)} avec une personne de la population majoritaire. C’est {pc(
        ligneE2(1).mixte
      )} pour les enfants de deux parents immigrés et {pc(ligneE2(2).mixte)} pour les enfants d’un seul
      parent immigré. Ces parts de couples mixtes sont des sommes : conjoint immigré d’une autre origine,
      enfant d’immigrés d’une autre origine, et conjoint de la population majoritaire.
    </p>
    <GENFigure
      titre="Origine du conjoint, selon la génération"
      lecture="{pc(
        ligneE2(2).majoritaire
      )} des enfants d’un seul parent immigré vivant en couple ont un conjoint de la population majoritaire."
      source="TeO2 (Ined-Insee, 2026), ch. 8, tableau 3"
      champ={d.champs.couples}
      badges={['U14']}
    >
      <GENEmpile
        lignes={d.e2.lignes.map((l) => ({
          libelle: l.libelle,
          segments: l.segments,
          fin: `mixte : ${pc(l.mixte)}`
        }))}
        legende={LEG_E2}
      />
      {#snippet tableau()}
        <table>
          <thead
            ><tr
              ><th>Groupe</th>{#each d.e2.colonnes as c (c)}<th>{c}</th>{/each}<th>Couple mixte</th
              ></tr
            ></thead
          >
          <tbody>
            {#each d.e2.lignes as l (l.libelle)}
              <tr
                ><td>{l.libelle}</td>{#each l.segments as s (s.cle)}<td
                    >{s.valeur ? pc(s.valeur) : '—'}</td
                  >{/each}<td>{pc(l.mixte)}</td></tr
              >
            {/each}
          </tbody>
        </table>
        <p>
          Population majoritaire : les colonnes (a) et (b) sont sans objet (tirets dans la source) ;
          son couple mixte est (c) + (d).
        </p>
      {/snippet}
    </GENFigure>
  </section>

  <section class="colonne">
    <h2>Les petits-enfants d’immigrés : combien de grands-parents immigrés ?</h2>
    <p>
      {pc(d.e3.ensemble[0].valeur)} des petits-enfants d’immigrés de 18 à 59 ans n’ont qu’un grand-parent
      immigré, {pc(d.e3.ensemble[1].valeur)} en ont deux, et {pc(d.e3.ensemble[3].valeur)} en ont quatre.
      La répartition varie selon l’origine : les lignées européennes sont les plus mêlées ; celles venues
      du Maghreb, d’Afrique subsaharienne, de Turquie et du Moyen-Orient le sont moins pour l’instant.
      Leur migration est plus récente, et l’enquête juge trop tôt pour dire si elles suivront le même
      chemin (TeO2, ch. 8) : le précédent européen est un précédent, pas une preuve.
    </p>
    <GENFigure
      titre="Petits-enfants d’immigrés (G3) de 18 à 59 ans : nombre de grands-parents immigrés"
      lecture="{pc(
        d.e3.ensemble[0].valeur
      )} des G3 de 18 à 59 ans n’ont qu’un grand-parent immigré sur quatre."
      source="TeO2 (Ined-Insee, 2026), ch. 8, tableau 4"
      champ={d.champs.g3}
      badges={['U14', 'U8']}
    >
      <GENEmpile
        lignes={[
          {
            libelle: 'Ensemble des G3',
            segments: d.e3.ensemble.map((x) => ({ cle: x.n, valeur: x.valeur }))
          },
          {
            libelle: 'G3 avec un grand-parent non européen',
            segments: d.e3.ensemble.map((x) => ({ cle: x.n, valeur: x.nonEuropeen }))
          }
        ]}
        legende={LEG_GP}
      />
    </GENFigure>
    <GENFigure
      titre="Enfants des enquêtés, tous âges, qui sont petits-enfants d’immigrés : selon l’origine des grands-parents"
      lecture="{pc(
        quatreGp('Europe du Sud')
      )} des petits-enfants d’immigrés venus d’Europe du Sud ont quatre grands-parents immigrés, contre {pc(
        quatreGp('Maghreb')
      )} pour le Maghreb."
      source="TeO2 (Ined-Insee, 2026), ch. 8, tableau 6 (base enfants)"
      champ={d.champs.g3_enfants}
      statut="Saisi ; la source donne le même effectif non pondéré (2 532) pour le Maghreb et l’Europe du Sud"
      badges={['U14']}
    >
      <GENEmpile
        lignes={d.e3.origines.map((o) => ({
          ...o,
          fin: doublon(o.effectif) ? `n = ${o.effectif.toLocaleString('fr-FR')} *` : undefined
        }))}
        legende={LEG_GP}
      />
      <p class="note-graphique">
        * La source donne le même effectif non pondéré ({doublonValeur?.toLocaleString('fr-FR')})
        pour le Maghreb et l’Europe du Sud : coïncidence ou coquille, à vérifier auprès des auteurs.
      </p>
      {#snippet tableau()}
        <table>
          <thead><tr><th>Origine</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead>
          <tbody>
            {#each d.e3.origines as o (o.libelle)}
              <tr
                ><td>{o.libelle}</td>{#each o.segments as s (s.cle)}<td>{pc(s.valeur)}</td
                  >{/each}</tr
              >
            {/each}
          </tbody>
        </table>
      {/snippet}
    </GENFigure>
  </section>

  <section class="colonne">
    <h2>Les inégalités qui persistent</h2>
    <p>
      Le mélange n’efface pas les inégalités. Les enfants d’immigrés vivent plus souvent que la
      population majoritaire dans les quartiers où les immigrés sont nombreux ({pc(seg[1].v2019)}
      contre {pc(seg[2].v2019)} en 2019, chez les 18-49 ans), et cet écart s’est creusé depuis 2008.
    </p>
    <GENFigure
      titre="Vivre dans un quartier à forte concentration d’immigrés (quintile supérieur), 2008 et 2019"
      lecture="en 2019, {pc(
        seg[1].v2019
      )} des enfants d’immigrés de 18 à 49 ans vivent dans les quartiers du quintile le plus concentré, contre {pc(
        seg[1].v2008
      )} en 2008."
      source="TeO2 (Ined-Insee, 2026), ch. 5, tableau 1"
      champ={d.champs.seg}
      badges={['U14']}
    >
      <GENPoints
        lignes={seg.map((s) => ({
          libelle: s.libelle,
          valeurs: { a2008: s.v2008, a2019: s.v2019 }
        }))}
        series={[
          { cle: 'a2008', libelle: '2008', couleur: 'var(--s1)', forme: 'creux' },
          { cle: 'a2019', libelle: '2019', couleur: 'var(--s1)', forme: 'rond' }
        ]}
        min={0}
        max={60}
        unite="%"
        format={pc}
      />
    </GENFigure>

    <p>
      À caractéristiques identiques (âge, diplôme, nationalité, vie en couple, santé, niveau de
      français, arrivée avant 16 ans, couple mixte des parents, quartier prioritaire et région), le
      risque de chômage reste plus élevé pour certaines origines, y compris chez les enfants
      d’immigrés : environ {pts(choG2Maghreb.hommes)} pour les fils d’immigrés du Maghreb. Pour d’autres
      origines, l’écart est proche de zéro, comme pour les enfants d’immigrés d’Europe du Sud.
    </p>
    <GENFigure
      titre="Écart de risque de chômage avec la population majoritaire, à caractéristiques identiques"
      lecture="à profil égal, le risque de chômage des immigrées venues du Maghreb dépasse d’environ {pts(
        choG1Maghreb.femmes
      )} celui des femmes de la population majoritaire."
      source="TeO2 (Ined-Insee, 2026), ch. 11, figure 1 (valeurs lues sur le graphique)"
      champ="actifs de 18 à 59 ans, France métropolitaine, 2019-2020"
      statut="Lu sur une figure sans étiquettes, à ± {virgule(
        d.e9.precisionCho ?? 0
      )} point ; les intervalles de confiance de la figure ne sont pas repris, et beaucoup incluent zéro (écart non significatif) ; le texte du §35 donne d’autres valeurs que la figure"
      badges={['U14']}
    >
      <GENPoints
        lignes={cho.map((c) => ({
          libelle: c.libelle,
          valeurs: { hommes: c.hommes, femmes: c.femmes }
        }))}
        series={[
          { cle: 'hommes', libelle: 'Hommes', couleur: 'var(--c1)', forme: 'rond' },
          { cle: 'femmes', libelle: 'Femmes', couleur: 'var(--c2)', forme: 'carre' }
        ]}
        min={-4}
        max={14}
        precision={d.e9.precisionCho}
      />
    </GENFigure>

    <p>
      {pc(disDe('Population majoritaire'))} des personnes de la population majoritaire déclarent avoir
      subi une discrimination au cours des cinq dernières années. C’est {pc(disDe('Immigrés (G1)'))} des
      immigrés et {pc(disDe('Enfants de deux parents immigrés (G2)'))} des enfants de deux parents immigrés.
      Selon l’origine, les enfants d’immigrés (un ou deux parents immigrés) venus d’Afrique subsaharienne
      sont {pc(disDe('Enfants d’immigrés (un ou deux parents), Afrique subsaharienne'))} à en déclarer,
      ceux d’Europe du Sud {pc(disDe('Enfants d’immigrés (un ou deux parents), Europe du Sud'))}.
    </p>
    <GENFigure
      titre="Discriminations déclarées au cours des cinq dernières années"
      lecture="{pc(
        disDe('Enfants d’immigrés (un ou deux parents), Maghreb')
      )} des enfants d’immigrés venus du Maghreb déclarent une discrimination."
      source="TeO2 (Ined-Insee, 2026), ch. 16, tableau 2 (discriminations autodéclarées)"
      champ="18-59 ans, France métropolitaine, 2019-2020"
      badges={['U14', 'U15']}
    >
      <GENBarres lignes={dis} max={50} />
    </GENFigure>
  </section>

  <section class="colonne">
    <h2>Le paradoxe : la France citée comme origine, et des discriminations déclarées</h2>
    <p>
      Interrogés sur leurs origines (question ouverte), les enquêtés citent plus souvent la France
      seule d’une génération à l’autre : {pc(ide[0].valeur)} des immigrés, {pc(ide[1].valeur)} des enfants
      de deux parents immigrés, {pc(ide[2].valeur)} des enfants d’un seul parent immigré, {pc(
        ide[3].valeur
      )}
      des petits-enfants, contre {pc(ide[4].valeur)} dans la population majoritaire. Dans le même temps,
      les enfants de deux parents immigrés déclarent plus de discriminations que les immigrés de l’enquête
      ({pc(d.e10.discriParGen[1].valeur)} contre {pc(d.e10.discriParGen[0].valeur)}). La comparaison
      est transversale : les immigrés enquêtés ne sont pas les parents des enfants d’immigrés
      enquêtés. Le paradoxe vaut pour certaines origines seulement : les enfants d’immigrés d’Europe
      du Sud déclarent moins de discriminations ({pc(
        disDe('Enfants d’immigrés (un ou deux parents), Europe du Sud')
      )}) que les immigrés venus d’Europe du Sud ({pc(disDe('Immigrés, Europe du Sud'))}). Cette
      lecture croisée des chapitres 9 et 16 est celle du site, pas une phrase du livre.
    </p>
    <div class="paire">
      <GENFigure
        titre="Citer la France seule comme origine"
        lecture="{pc(
          ide[3].valeur
        )} des petits-enfants d’immigrés citent la France seule comme origine."
        source="TeO2, ch. 9, tableau 4"
        champ="18-59 ans, France métropolitaine, 2019-2020"
        statut="Saisi ; dans la source, la ligne des immigrés somme à {100 +
          d.e10.anomalieG1} % (coquille probable du livre)"
        badges={['U14', 'U15']}
      >
        <GENBarres
          lignes={ide.map((x) => ({
            libelle: x.libelle,
            valeur: x.valeur,
            couleur: TEINTE[x.teinte]
          }))}
        />
      </GENFigure>
      <GENFigure
        titre="Déclarer une discrimination"
        lecture="{pc(
          d.e10.discriParGen[1].valeur
        )} des enfants de deux parents immigrés déclarent une discrimination."
        source="TeO2, ch. 16, tableau 2"
        champ="18-59 ans, France métropolitaine, 2019-2020"
        badges={['U14', 'U15']}
      >
        <GENBarres
          lignes={d.e10.discriParGen.map((x) => ({
            libelle: x.libelle,
            valeur: x.valeur,
            couleur: TEINTE[x.teinte]
          }))}
        />
      </GENFigure>
    </div>
  </section>

  <section class="colonne">
    <h2>Ce qu’on ne sait pas</h2>
    <dl class="incertitudes">
      {#each data.incertitudes as u (u.code)}
        <dt><span class="code">{u.code}</span> {u.titre}</dt>
        <dd>{u.detail}</dd>
      {/each}
    </dl>
  </section>
</article>

<style>
  .generations {
    --t0: #c9d3de;
    --t1: #6da7ec;
    --t2: #3987e5;
    --t3: #1c5cab;
    --t4: #0d366b;
    --o0: #86b6ef;
    --o1: #5598e7;
    --o2: #2a78d6;
    --o3: #1c5cab;
    --o4: #0d366b;
    --s1: #2a78d6;
    --c1: #2a78d6;
    --c2: #eb6834;
    --neutre-1: #7d879b;
    --neutre-2: #a7b0bf;
  }
  @media (prefers-color-scheme: dark) {
    .generations {
      --t0: #4a5a6c;
      --t1: #2a78d6;
      --t2: #5598e7;
      --t3: #86b6ef;
      --t4: #cde2fb;
      --o0: #184f95;
      --o1: #256abf;
      --o2: #3987e5;
      --o3: #6da7ec;
      --o4: #b7d3f6;
      --s1: #3987e5;
      --c1: #3987e5;
      --c2: #d95926;
      --neutre-1: #8691a6;
      --neutre-2: #5b667a;
    }
  }
  .colonne {
    max-width: 46rem;
  }
  section {
    margin-top: 2.5rem;
  }
  .contradicteurs {
    border: 1px solid var(--reglure);
    border-radius: 6px;
    padding: 0.25rem 1rem 0.5rem;
    margin: 2rem 0;
  }
  .contradicteurs h3 {
    margin: 0.75rem 0 0.25rem;
  }
  .note-graphique {
    font-size: var(--t-0);
    color: var(--ardoise);
    margin: 0.5rem 0 0;
  }
  .etat {
    font-size: var(--t-0);
    color: var(--gris);
    font-style: italic;
  }
  .paire {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 2rem;
  }
  @media (max-width: 799px) {
    .paire {
      grid-template-columns: 1fr;
    }
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
