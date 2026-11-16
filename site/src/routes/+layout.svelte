<script lang="ts">
  import '../app.css';
  import { page } from '$app/state';
  import { SITE } from '$lib/site';

  let { data, children } = $props();

  const LIENS = [
    { href: '/piscine', libelle: 'La piscine' },
    { href: '/temps-long', libelle: 'Le temps long' },
    { href: '/generations', libelle: 'Générations' },
    { href: '/arrivees', libelle: 'Les arrivées' },
    { href: '/naissances', libelle: 'Les naissances' },
    { href: '/ailleurs', libelle: 'Ailleurs' },
    { href: '/limites', libelle: 'Ce qu’on ne sait pas' },
    { href: '/methode', libelle: 'Méthode' },
    { href: '/donnees', libelle: 'Données' }
  ];
  const date = $derived(
    new Date(data.genereLe).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  );
</script>

<svelte:head>
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content={SITE.nom} />
  <meta property="og:locale" content="fr_FR" />
  <meta property="og:title" content={SITE.nom} />
  <meta property="og:description" content={SITE.description} />
  <meta
    property="og:url"
    content="{SITE.url}{page.url.pathname === '/' ? '' : page.url.pathname}"
  />
  <meta property="og:image" content="{SITE.url}/partage.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta
    property="og:image:alt"
    content="Qui remplace qui ? Une règle graduée montre la part des immigrés dans la population, lue comme un niveau d’eau."
  />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<a class="evitement" href="#contenu">Aller au contenu</a>

<header class="entete page">
  <a class="marque" href="/" aria-current={page.url.pathname === '/' ? 'page' : undefined}
    >Qui remplace qui ?</a
  >
  <nav aria-label="Navigation principale">
    {#each LIENS as l (l.href)}
      <a href={l.href} aria-current={page.url.pathname === l.href ? 'page' : undefined}
        >{l.libelle}</a
      >
    {/each}
  </nav>
</header>

<main id="contenu">
  {@render children()}
</main>

<footer class="pied page">
  <p>
    Statistique publique uniquement (Insee, Ined, ministère de l’Intérieur, Eurostat, OCDE, ONU).
    Calculs arrêtés au {date}, reproductibles à partir des <a href="/donnees">fichiers publiés</a>
    et du
    <a href={SITE.depot}>code</a>.
  </p>
  <p>
    Aucun cookie, aucun traceur, aucune ressource tierce. <a href="/a-propos">À propos</a> : contact,
    code, licences.
  </p>
</footer>

<style>
  .entete {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.4rem 2rem;
    padding-top: 1.25rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid var(--reglure);
  }
  .marque {
    font-family: var(--titre);
    font-weight: 700;
    font-size: var(--t-2);
    letter-spacing: 0.01em;
    color: var(--encre);
    text-decoration: none;
  }
  nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem 1.25rem;
    font-size: var(--t-0);
  }
  nav a {
    color: var(--ardoise);
    text-decoration: none;
    padding-block: 0.2rem;
  }
  nav a:hover {
    color: var(--encre);
  }
  nav a[aria-current='page'] {
    color: var(--encre);
    box-shadow: inset 0 -2px 0 var(--repere);
  }
  .pied {
    margin-top: 4rem;
    padding-top: 1.25rem;
    padding-bottom: 2.5rem;
    border-top: 1px solid var(--reglure);
    font-size: var(--t-0);
    color: var(--ardoise);
  }
  .pied p {
    margin: 0.25rem 0;
  }
  .evitement {
    position: absolute;
    left: -999px;
  }
  .evitement:focus {
    left: 1rem;
    top: 1rem;
    background: var(--plaque);
    padding: 0.4rem 0.6rem;
  }
</style>
