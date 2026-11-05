<script lang="ts">
  import '../app.css';
  import { page } from '$app/state';

  let { data, children } = $props();

  const LIENS = [
    { href: '/piscine', libelle: 'La piscine' },
    { href: '/temps-long', libelle: 'Le temps long' },
    { href: '/generations', libelle: 'Générations' },
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
    Site en construction. Données publiques uniquement (Insee, Ined). Calculs arrêtés au {date},
    reproductibles à partir des <a href="/donnees">fichiers publiés</a>.
  </p>
  <p>Aucun cookie, aucun traceur, aucune ressource tierce.</p>
</footer>

<style>
  .entete {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem 1.5rem;
    padding-top: 1.25rem;
    padding-bottom: 1rem;
  }
  .marque {
    font-weight: 700;
    font-size: var(--t-2);
    color: var(--encre);
    text-decoration: none;
  }
  nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem 1.1rem;
    font-size: var(--t-0);
  }
  nav a {
    color: var(--ardoise);
    text-decoration: none;
  }
  nav a[aria-current='page'] {
    color: var(--encre);
    font-weight: 600;
  }
  .pied {
    margin-top: 4rem;
    padding-bottom: 2rem;
    font-size: var(--t-0);
    color: var(--gris);
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
  }
</style>
