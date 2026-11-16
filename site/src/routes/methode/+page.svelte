<script lang="ts">
  import { milliers, pct } from '$lib/format';
  let { data } = $props();
  const v = (x: number, n = 2) => x.toFixed(n).replace('.', ',');
  const LIB: Record<string, string> = {
    G1: 'Immigrés',
    G2a: 'G2, deux parents',
    G2b: 'G2, un parent',
    G3: 'G3'
  };
</script>

<svelte:head>
  <title>Méthode · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Comment les chiffres du site sont produits, modélisés et contrôlés."
  />
</svelte:head>

<article class="page colonne">
  <h1>Méthode</h1>
  <p class="chapeau">
    Des sources publiques, lues par un programme ; des identités comptables vérifiées à chaque
    calcul ; un modèle là où la statistique ne mesure pas, calé sur ce qu’elle mesure et affiché
    comme tel.
  </p>
  <p class="brouillon">Textes en brouillon.</p>

  <h2>Trois régimes de données</h2>
  <ul>
    <li>
      <strong>Publié par l’Insee</strong> : stocks d’immigrés, naissances, décès, entrées des immigrés
      et des non-immigrés. Les sorties (2006-2022) sont calculées par l’Insee par différence entre le
      solde migratoire et les entrées (U2) ; les décès d’immigrés sont estimés par l’Insee, l’état civil
      ne les identifiant pas (U18). Dans la piscine, ce régime s’appelle « publié » : ces chiffres viennent
      de l’Insee, mais tous ne sont pas des comptages.
    </li>
    <li>
      <strong>Reconstruit</strong> : ce qui se déduit de mesures sans être publié tel quel (le flux net
      des immigrés entre deux recensements, avant 2006).
    </li>
    <li>
      <strong>Modélisé</strong> : les enfants et petits-enfants d’immigrés, année par année et âge par
      âge (modèle de cohortes), et les décès d’immigrés hors 2006-2022.
    </li>
  </ul>

  <h2>Les identités comptables, vérifiées à chaque calcul</h2>
  <p>
    Population de l’année suivante = population + naissances − décès + entrées − sorties (+
    ajustements). Immigrés de l’année suivante = immigrés + entrées − sorties − décès :
    <strong>aucune naissance</strong>, puisqu’un enfant né en France n’est pas un immigré. Les
    changements de champ (outre-mer en 1990, Mayotte en 2014), l’effet de la nouvelle collecte du
    recensement en 2024 et les années de guerre sont des ajustements, jamais des arrivées. Le calcul
    échoue si une identité ne tient pas.
  </p>

  <h2>Le modèle de cohortes</h2>
  <p>
    De 1911 à 2025, le modèle suit les immigrés (G1), leurs enfants nés en France (G2, avec deux
    parents ou un seul parent immigré) et leurs petits-enfants (G3), âge par âge. Chaque année, il
    applique la mortalité nationale par âge (aucune hypothèse de surmortalité par origine), fait
    naître les enfants selon la composition observée des naissances, et ajuste les arrivées
    d’immigrés pour retomber sur les stocks des recensements. Statut des paramètres :
    <strong>{data.statut === 'valide' ? 'validés' : 'à valider'}</strong>.
  </p>
  <p>
    Valeurs calées à chaque calcul : taux de départ des immigrés {pct(
      100 * data.calage.taux_departs
    )}
    par an (calé sur les sorties publiées par l’Insee de 2006 à 2021 ; 2022, atypique, est exclue) ; part
    des naissances « deux parents nés à l’étranger » attribuée à deux parents immigrés : {pct(
      100 * data.calage.correction_deux
    )} ; part des naissances « un parent né à l’étranger » attribuée à un parent immigré :
    {pct(100 * data.calage.correction_un)} (calées sur l’enquête Insee de 2019-2020, IP 1910).
  </p>

  <h3>Le modèle face à ses cibles et à ses témoins</h3>
  <table>
    <caption>Part de chaque génération en 2020 (modèle / enquête IP 1910), en %</caption>
    <thead
      ><tr
        ><th scope="col">Génération</th><th scope="col">Âge</th><th scope="col">Modèle</th><th
          scope="col">IP 1910</th
        ></tr
      ></thead
    >
    <tbody>
      {#each data.ip as r (r.groupe + r.classe)}
        <tr
          ><td>{LIB[r.groupe]}</td><td>{r.classe}</td><td class="n">{v(r.modele, 1)}</td><td
            class="n">{v(r.observe, 1)}</td
          ></tr
        >
      {/each}
    </tbody>
  </table>
  <p>
    Témoins indépendants (non utilisés pour caler) : descendants d’immigrés en 2025,
    {milliers(data.descendants.modele)} dans le modèle contre {milliers(data.descendants.observe)}
    mesurés par l’enquête Emploi (logement ordinaire, hors Mayotte) ; décès d’immigrés sur
    {data.deces.annees} ans, {milliers(data.deces.modele)} dans le modèle contre
    {milliers(data.deces.observe)} estimés par l’Insee ; âge des immigrés au recensement de {data.rp
      .annee} (tous logements), {v(data.rp.jeunes.modele, 1)} % de 15-24 ans dans le modèle contre {v(
      data.rp.jeunes.observe,
      1
    )} %, et {v(data.rp.ages.modele, 1)} % de 55 ans ou plus contre {v(data.rp.ages.observe, 1)} %.
  </p>

  <p>
    Limites connues : le modèle surestime les immigrés d’environ un point de pourcentage par rapport
    à l’enquête de 2019-2020, et jusqu’à {v(data.ecartMaxG1, 1)} points pour certaines classes d’âge,
    surtout chez les jeunes adultes et les plus de 75 ans. Une partie de l’écart tient au champ (l’enquête
    ne couvre que les logements ordinaires, sans foyers ni résidences), mais le recensement, qui couvre
    tous les logements, montrait aussi trop de jeunes adultes tant que le modèle faisait arriver les immigrés
    de toutes les époques avec l’âge des arrivants de 2024. Avant 1990, ce profil est désormais rajeuni
    à l’âge médian à l’arrivée des immigrés présents en 1999 (22 ans, contre 26 pour les arrivants de
    2024). Contrepartie : des immigrés plus jeunes meurent moins, et le modèle s’écarte davantage des
    décès estimés par l’Insee. La répartition des enfants d’immigrés entre un et deux parents immigrés
    suit la convention de l’enquête de 2019-2020 ; l’Insee l’a modifiée en 2021, et les deux mesures ne
    sont pas comparables (U21) ; la troisième génération au-delà de 60 ans n’a aucune cible ; dans les
    années anciennes, les générations dépendent d’une hypothèse sur les enfants d’immigrés vivants en
    1911 : le modèle est recalé avec la moitié et une fois et demie cette hypothèse, et la fourchette
    obtenue s’affiche au survol de la piscine (U20).
  </p>

  <h2>Les décès d’immigrés dans la piscine</h2>
  <p>
    Hors de 2006-2022, la piscine estime les décès d’immigrés en appliquant à leur part dans la
    population le rapport observé de {data.ratio.calage[0]} à {data.ratio.calage[1]} entre leur part dans
    les décès et leur part dans la population ({v(data.ratio.moyen)} en moyenne, de {v(
      data.ratio.min
    )}
    à {v(data.ratio.max)}).
  </p>

  <h2>Reproduire</h2>
  <p>
    Le programme télécharge les tableurs de l’Insee, en note l’empreinte, calcule et contrôle tout :
    <code>qrq download</code>, <code>qrq build</code>, <code>qrq check</code>. Les fichiers produits
    sont sur la page <a href="/donnees">Données</a>.
  </p>
</article>

<style>
  table {
    border-collapse: collapse;
    font-size: var(--t-0);
    font-variant-numeric: tabular-nums;
    margin: 0.5rem 0 1rem;
  }
  caption {
    text-align: left;
    color: var(--ardoise);
    margin-bottom: 0.3rem;
  }
  th,
  td {
    padding: 0.25rem 1rem 0.25rem 0;
    border-bottom: 1px solid var(--reglure);
    text-align: left;
  }
  .n {
    text-align: right;
  }
</style>
