<script lang="ts">
  // « La page en N réponses » : les questions de la page, chacune avec son chiffre clé et sa
  // réponse en une phrase, liées aux sections. Pour lire la page en survol.
  let {
    items
  }: { items: { ancre: string; question: string; chiffre: string; reponse: string }[] } = $props();
  const NOMBRES = ['', 'une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit'];
  // Pas de coupure de ligne entre un nombre et son unité.
  const insecables = (t: string) => t.replace(/ (%|points?\b|pt\b)/g, '\u00a0$1');
  const n = $derived(NOMBRES[items.length] ?? String(items.length));
</script>

<nav class="sommaire" aria-labelledby="sommaire-titre">
  <h2 id="sommaire-titre">La page en {n} réponses</h2>
  <ol>
    {#each items as it (it.ancre)}
      <li>
        <a href="#{it.ancre}">
          <span class="question">{it.question}</span>
          <span class="chiffre">{it.chiffre}</span>
          <span class="reponse-courte">{insecables(it.reponse)}</span>
        </a>
      </li>
    {/each}
  </ol>
</nav>

<style>
  .sommaire {
    margin: 2rem 0 1rem;
  }
  h2 {
    font-size: var(--t-1);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--gris);
    margin: 0 0 0.75rem;
  }
  ol {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr));
    gap: 0.75rem;
  }
  a {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    height: 100%;
    padding: 0.8rem 0.95rem 0.9rem;
    border: 1px solid var(--reglure);
    border-radius: 0.6rem;
    text-decoration: none;
    color: var(--ardoise);
    font-size: var(--t-0);
    line-height: 1.4;
  }
  a:hover,
  a:focus-visible {
    border-color: var(--lien);
  }
  .question {
    text-wrap: balance;
    font-weight: 600;
    color: var(--encre);
    font-size: 0.9rem;
  }
  .chiffre {
    font-size: var(--t-3);
    white-space: nowrap;
    font-weight: 700;
    color: var(--encre);
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
    margin-top: 0.2rem;
  }
</style>
