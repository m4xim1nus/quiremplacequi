<script lang="ts">
  import GENFigure from '$lib/components/GENFigure.svelte';
  import GENCurseur from '$lib/components/GENCurseur.svelte';
  import GENEmpile from '$lib/components/GENEmpile.svelte';
  import GENBarres from '$lib/components/GENBarres.svelte';
  import GENPoints from '$lib/components/GENPoints.svelte';
  import Sommaire from '$lib/components/Sommaire.svelte';
  import Detail from '$lib/components/Detail.svelte';
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
  const LEG_E2O = $derived(
    d.e2origine.colonnes.map((c, i) => ({
      cle: c,
      libelle: c,
      couleur: `var(--o${i === 3 ? 0 : 4 - i})`,
      claire: i === 3
    }))
  );
  const natifE2O = (libelle: string) =>
    d.e2origine.lignes
      .find((l) => l.libelle === libelle)!
      .segments.find((s) => s.cle === 'Français·e sur deux générations')!.valeur;
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

  // La page en cinq réponses : chaque chiffre est lu dans les données, comme dans les sections.
  const SOMMAIRE = $derived([
    {
      ancre: 'combien',
      question: 'Combien sont-ils ?',
      chiffre: `${pc(p('g1').cumul).replace(/\u00a0%$/, '')} → ${pc(e1.total41)}`,
      reponse:
        'des 18-59 ans, selon que l’on compte les seuls immigrés, ou aussi leurs descendants, les originaires des outre-mer et les conjoints.'
    },
    {
      ancre: 'couples',
      question: 'Avec qui vivent-ils ?',
      chiffre: pc(ligneE2(2).mixte),
      reponse: `des enfants d’un seul parent immigré vivant en couple forment un couple mixte, contre ${pc(ligneE2(0).mixte)} des immigrés.`
    },
    {
      ancre: 'grands-parents',
      question: 'Combien de grands-parents immigrés ?',
      chiffre: pc(d.e3.ensemble[0].valeur),
      reponse: 'des petits-enfants d’immigrés de 18 à 59 ans n’en ont qu’un sur quatre.'
    },
    {
      ancre: 'inegalites',
      question: 'Le mélange efface-t-il les inégalités ?',
      chiffre: pc(seg[1].v2019),
      reponse: `des enfants d’immigrés de 18 à 49 ans vivent dans les quartiers à plus forte concentration d’immigrés, contre ${pc(seg[2].v2019)} de la population majoritaire.`
    },
    {
      ancre: 'paradoxe',
      question: 'Que disent-ils de leurs origines ?',
      chiffre: pc(ide[3].valeur),
      reponse: `des petits-enfants d’immigrés citent la France seule comme origine. Mais les enfants de deux parents immigrés déclarent plus de discriminations que les immigrés (${pc(d.e10.discriParGen[1].valeur)} contre ${pc(d.e10.discriParGen[0].valeur)}).`
    }
  ]);
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

  <Sommaire items={SOMMAIRE} />

  <section class="colonne" id="combien">
    <h2>Combien sont-ils ?</h2>
    <p class="reponse">
      Ça dépend de qui l’on compte. <strong>{pc(p('g1').cumul)}</strong> des 18-59 ans sont immigrés
      ;
      <strong>{pc(p('g3').cumul)}</strong> avec leurs enfants et petits-enfants ;
      <strong>{pc(e1.total41)}</strong> en ajoutant les originaires des outre-mer et d’autres liens. Le
      chiffre change surtout avec la définition.
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

    <Detail>
      <p>
        Le chiffre de {pc(e1.total41)}, souvent cité, compte en plus des immigrés et de leurs
        descendants les originaires des outre-mer et leurs enfants ({pc(e1.om)}), puis d’autres
        liens ({pc(e1.conjoints)}, part déduite : {pc(e1.total41)} moins les autres crans). Selon la note
        6 du chapitre, ce sont surtout des conjoints, mais aussi les petits-enfants d’originaires des
        outre-mer et les conjoints de descendants plus lointains.
      </p>
      <p>
        Du premier au dernier cran, le chiffre est multiplié par {virgule(e1.etendue)}. Un chiffre à
        une date ne dit rien de la croissance : il change surtout avec la définition.
      </p>
      <p>
        L’Insee fait le même compte sur les 0-59 ans, enfants compris : {pc(e1.ip1910[0].cumul)}
        d’immigrés, {pc(e1.ip1910[2].cumul)} avec leurs enfants, {pc(e1.ip1910[3].cumul)} avec leurs petits-enfants.
        Sur la même tranche des 18-59 ans, l’Insee arrive à {pc(e1.ip1910_18_59)}, contre {pc(
          p('g3').cumul
        )} dans TeO2 : les deux sources et leurs méthodes diffèrent (enquête Emploi d’un côté, enquête
        spécialisée de l’autre).
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
    </Detail>

    <Detail
      encadre
      niveau={3}
      titre="Ce que disent les contradicteurs"
      resume="Une note de septembre 2026 projette des « sans ascendance migratoire » minoritaires. Ce qu’on peut en dire avec les données de 2019-2020."
    >
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
        3a). Selon TeO2 (ch. 8, §39), parmi les enfants des enquêtés qui sont petits-enfants d’immigrés
        (tous âges), la mixité s’installe dès la génération des grands-parents pour
        {pc(e1.lignages.grandsParents)} d’entre eux, et à la génération des parents pour
        {pc(e1.lignages.parents)}.
      </p>
      <p class="etat">
        À vérifier avant publication : le contenu exact de la note (scénarios, fécondité, mixité,
        définition de l’ascendance). La contre-projection viendra avec le mode projection de la
        piscine.
      </p>
    </Detail>
  </section>

  <section class="colonne" id="couples">
    <h2>Avec qui vivent-ils ?</h2>
    <p class="reponse">
      Souvent avec une personne d’une autre origine. Parmi ceux qui vivent en couple, c’est le cas
      de
      <strong>{pc(ligneE2(2).mixte)}</strong> des enfants d’un seul parent immigré, {pc(
        ligneE2(1).mixte
      )} des enfants de deux parents immigrés et {pc(ligneE2(0).mixte)} des immigrés.
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
    <Detail>
      <p>
        {pc(ligneE2(0).mixte)} des immigrés en couple vivent avec un conjoint d’une autre origine, dont
        {pc(ligneE2(0).majoritaire)} avec une personne de la population majoritaire. Ces parts de couples
        mixtes sont des sommes : conjoint immigré d’une autre origine, enfant d’immigrés d’une autre origine,
        et conjoint de la population majoritaire.
      </p>
      <GENFigure
        titre="Origine du conjoint des enfants d’immigrés, selon leur origine et leur sexe"
        lecture="{pc(
          natifE2O('Un parent immigré (G2.5), hommes')
        )} des fils d’un seul parent immigré vivant en couple ont un conjoint français sur deux générations (ni immigré, ni enfant d’immigré)."
        source="TeO2 (Ined-Insee, 2026), ch. 7, figure 4"
        champ={d.champs.couples_desc}
        badges={['U14']}
      >
        <GENEmpile
          lignes={d.e2origine.lignes.map((l) => ({ libelle: l.libelle, segments: l.segments }))}
          legende={LEG_E2O}
        />
      </GENFigure>
      <p>
        Cette figure classe les conjoints en quatre catégories, autrement que le tableau précédent :
        ses chiffres ne se comparent pas un à un avec lui. Quelques segments trop fins pour porter
        une étiquette dans la source sont déduits du total (à un point près).
      </p>
    </Detail>
  </section>

  <section class="colonne" id="grands-parents">
    <h2>Les petits-enfants d’immigrés : combien de grands-parents immigrés ?</h2>
    <p class="reponse">
      Le plus souvent un seul sur quatre. <strong>{pc(d.e3.ensemble[0].valeur)}</strong> des
      petits-enfants d’immigrés de 18 à 59 ans n’ont qu’un grand-parent immigré, {pc(
        d.e3.ensemble[1].valeur
      )} en ont deux, et {pc(d.e3.ensemble[3].valeur)} en ont quatre.
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

    <p>
      La répartition varie selon l’origine. Les lignées européennes sont les plus mêlées ; celles
      venues du Maghreb, d’Afrique subsaharienne, de Turquie et du Moyen-Orient le sont moins pour
      l’instant.
    </p>
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
    <Detail>
      <p>
        Les migrations venues du Maghreb, d’Afrique subsaharienne, de Turquie et du Moyen-Orient
        sont plus récentes, et l’enquête juge trop tôt pour dire si elles suivront le même chemin
        que les lignées européennes (TeO2, ch. 8) : le précédent européen est un précédent, pas une
        preuve.
      </p>
    </Detail>
  </section>

  <section class="colonne" id="inegalites">
    <h2>Le mélange efface-t-il les inégalités ?</h2>
    <p class="reponse">
      Non. Les enfants d’immigrés vivent plus souvent dans les quartiers où les immigrés sont
      nombreux. À profil égal, certains ont un risque de chômage plus élevé, et ils déclarent plus
      de discriminations que la population majoritaire.
    </p>

    <p>
      En 2019, chez les 18-49 ans, <strong>{pc(seg[1].v2019)}</strong> des enfants d’immigrés vivent
      dans les quartiers à plus forte concentration d’immigrés, contre {pc(seg[2].v2019)} de la population
      majoritaire. L’écart, en points, s’est creusé depuis 2008.
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
      À profil égal, le risque de chômage reste plus élevé pour certaines origines, y compris chez
      les enfants d’immigrés : environ <strong>{Math.round(choG2Maghreb.hommes)} points</strong> pour
      les fils d’immigrés du Maghreb (valeur lue sur la figure ; sa significativité n’est pas reprise
      ici). Pour d’autres, comme les enfants d’immigrés d’Europe du Sud, l’écart est proche de zéro.
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
    <Detail titre="Le détail : « à profil égal »">
      <p>
        Les caractéristiques tenues identiques sont l’âge, le diplôme, la nationalité, la vie en
        couple, la santé, le niveau de français, l’arrivée avant 16 ans, le couple mixte des
        parents, le quartier prioritaire et la région.
      </p>
      <p>
        Le texte du chapitre contredit sa propre figure. Sa conclusion (§35) attribue aux hommes
        immigrés d’Afrique du Nord un écart de {d.e9.texte35.g1.hommes} points et aux femmes de {d
          .e9.texte35.g1.femmes} points ; la note de lecture de la figure donne {d.e9.texte35
          .lectureG1Hommes} points pour les hommes, et la figure environ {virgule(
          choG1Maghreb.femmes
        )} points pour les femmes. Le site suit la figure.
      </p>
    </Detail>

    <p>
      <strong>{pc(disDe('Enfants de deux parents immigrés (G2)'))}</strong> des enfants de deux
      parents immigrés déclarent avoir subi une discrimination au cours des cinq dernières années,
      contre {pc(disDe('Immigrés (G1)'))} des immigrés et {pc(disDe('Population majoritaire'))} de la
      population majoritaire.
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
    <Detail>
      <p>
        Selon l’origine, les enfants d’immigrés (un ou deux parents immigrés) venus d’Afrique
        subsaharienne sont {pc(
          disDe('Enfants d’immigrés (un ou deux parents), Afrique subsaharienne')
        )}
        à en déclarer, ceux d’Europe du Sud {pc(
          disDe('Enfants d’immigrés (un ou deux parents), Europe du Sud')
        )}.
      </p>
    </Detail>
  </section>

  <section class="colonne" id="paradoxe">
    <h2>Que disent-ils de leurs origines ?</h2>
    <p class="reponse">
      D’une génération à l’autre, ils citent plus souvent la France seule : <strong
        >{pc(ide[3].valeur)}</strong
      >
      des petits-enfants d’immigrés, contre {pc(ide[0].valeur)} des immigrés (valeur fragile : la ligne
      des immigrés est incohérente dans la source). Pourtant, les enfants de deux parents immigrés déclarent
      plus de discriminations que les immigrés : les deux mouvements ne vont pas dans le même sens.
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
    <Detail>
      <p>
        Interrogés sur leurs origines (question ouverte), les enquêtés citent la France seule dans
        {pc(ide[0].valeur)} des cas chez les immigrés, {pc(ide[1].valeur)} chez les enfants de deux parents
        immigrés, {pc(ide[2].valeur)} chez les enfants d’un seul parent immigré, {pc(ide[3].valeur)} chez
        les petits-enfants, contre {pc(ide[4].valeur)} dans la population majoritaire. Les enfants de
        deux parents immigrés déclarent une discrimination dans {pc(d.e10.discriParGen[1].valeur)}
        des cas, contre {pc(d.e10.discriParGen[0].valeur)} chez les immigrés.
      </p>
      <p>
        La comparaison est transversale : les immigrés enquêtés ne sont pas les parents des enfants
        d’immigrés enquêtés. Cet écart vaut pour certaines origines seulement : les enfants
        d’immigrés d’Europe du Sud déclarent moins de discriminations ({pc(
          disDe('Enfants d’immigrés (un ou deux parents), Europe du Sud')
        )}) que les immigrés venus d’Europe du Sud ({pc(disDe('Immigrés, Europe du Sud'))}). Cette
        lecture croisée des chapitres 9 et 16 est celle du site, pas une phrase du livre.
      </p>
    </Detail>
  </section>

  <section class="colonne">
    <Detail
      encadre
      niveau={2}
      titre="Ce qu’on ne sait pas"
      resume="Les limites des sources de cette page ({data.incertitudes
        .map((u) => u.code)
        .join(', ')}) : champ, date et définitions des enquêtes."
    >
      <dl class="incertitudes">
        {#each data.incertitudes as u (u.code)}
          <dt><span class="code">{u.code}</span> {u.titre}</dt>
          <dd>{u.detail}</dd>
        {/each}
      </dl>
    </Detail>
  </section>
</article>

<style>
  .generations {
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
