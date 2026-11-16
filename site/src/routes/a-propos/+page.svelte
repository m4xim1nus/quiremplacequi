<script lang="ts">
  import { SITE } from '$lib/site';
</script>

<svelte:head>
  <title>À propos · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Qui fait ce site, comment le contacter, sous quelles licences réutiliser ses textes, ses données et son code."
  />
</svelte:head>

<article class="page colonne">
  <h1>À propos</h1>
  <p class="chapeau">
    Un projet indépendant, qui signe par son dépôt public : le code, les données et tout leur
    historique sont consultables.
  </p>

  <h2>Le dépôt</h2>
  <p>
    Tout ce qui produit ce site est sur <a href={SITE.depot}>GitHub</a> : les scripts qui lisent les
    fichiers de l’Insee, du ministère de l’Intérieur, d’Eurostat et de l’OCDE, les saisies
    référencées des tableaux qui n’existent qu’en PDF, les contrôles, le modèle de la piscine et ses
    paramètres. Chaque chiffre du site peut être recalculé à partir de là (voir
    <a href="/methode">Méthode</a>
    et
    <a href="/donnees">Données</a>).
  </p>

  <h2>Signaler une erreur</h2>
  <p>
    Une erreur, une source mal lue, une formulation trompeuse : ouvrez un
    <a href={SITE.tickets}>ticket sur GitHub</a>, ou écrivez à
    <a href="mailto:{SITE.contact}" class="adresse">{SITE.contact}</a>. Les corrections sont datées
    et visibles dans l’historique du dépôt.
  </p>

  <h2>Licences</h2>
  <ul>
    <li>
      Textes, figures et données calculées : <a href={SITE.licenceContenus.url}
        >{SITE.licenceContenus.nom}</a
      >. Vous pouvez les reprendre, y compris pour un usage commercial, en citant « Qui remplace qui
      ? » et l’adresse de la page.
    </li>
    <li>Code : licence <a href={SITE.licenceCode.url}>{SITE.licenceCode.nom}</a>.</li>
    <li>
      Données sources : celles de l’Insee et du ministère de l’Intérieur, sous Licence Ouverte 2.0 ;
      celles d’Eurostat et de l’OCDE, sous CC BY 4.0 ; les chiffres de l’enquête TeO2 (Ined-Insee)
      sont ressaisis à partir des tableaux et figures du livre, avec une référence par cellule, sans
      reproduire ses illustrations : à citer comme tels.
    </li>
    <li>Polices : Atkinson Hyperlegible Next et Barlow Semi Condensed, licence SIL Open Font.</li>
  </ul>

  <h2>Vie privée</h2>
  <p>
    Aucun cookie, aucun traceur, aucune mesure d’audience, aucune ressource chargée depuis un autre
    site. Les polices et les données sont servies par le site lui-même.
  </p>
</article>

<style>
  .adresse {
    overflow-wrap: anywhere;
  }
</style>
