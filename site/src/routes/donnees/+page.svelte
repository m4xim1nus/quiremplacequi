<script lang="ts">
  let { data } = $props();
  const taille = (o: number) =>
    o > 1e6
      ? `${(o / 1e6).toFixed(1).replace('.', ',')} Mo`
      : `${Math.max(1, Math.round(o / 1e3))} ko`;
</script>

<svelte:head>
  <title>Données · Qui remplace qui ?</title>
  <meta name="description" content="Tous les fichiers calculés par le site, et leurs sources." />
</svelte:head>

<article class="page colonne">
  <h1>Données</h1>
  <p class="chapeau">
    Tout ce que le site affiche est calculé à partir de ces fichiers, eux-mêmes produits par un
    programme ouvert à partir de la statistique publique. Données sources sous Licence Ouverte 2.0
    (Insee) ; tableaux de TeO2 ressaisis avec leur référence.
  </p>

  <h2>Fichiers publiés</h2>
  <table>
    <thead
      ><tr><th scope="col">Fichier</th><th scope="col">Contenu</th><th scope="col">Taille</th></tr
      ></thead
    >
    <tbody>
      {#each data.fichiers as f (f.nom)}
        <tr>
          <td><a href="/donnees/{f.nom}" download>{f.nom}</a></td>
          <td>{f.description}</td>
          <td class="nombre">{taille(f.octets)}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  <h2>Sources</h2>
  <ul class="sources">
    {#each data.sources as s (s.cle)}
      <li>
        <a href={s.page}>{s.titre}</a>
        <span class="date">téléchargé le {s.telecharge_le.slice(0, 10)}</span>
      </li>
    {/each}
  </ul>
</article>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--t-0);
  }
  th,
  td {
    text-align: left;
    padding: 0.4rem 0.5rem 0.4rem 0;
    border-bottom: 1px solid var(--reglure);
    vertical-align: top;
  }
  td a {
    word-break: break-all;
  }
  .nombre {
    text-align: right;
    white-space: nowrap;
  }
  .sources li {
    margin: 0.4rem 0;
  }
  .date {
    color: var(--gris);
    font-size: var(--t-0);
    margin-left: 0.4rem;
  }
</style>
