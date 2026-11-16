<script lang="ts">
  // « La page en N réponses » : les questions de la page, chacune avec son chiffre clé et sa
  // réponse en une phrase, liées aux sections. Pour lire la page en survol.
  let {
    items
  }: { items: { ancre: string; question: string; chiffre: string; reponse: string }[] } = $props();
  const NOMBRES = ['', 'une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit'];
  // Pas de coupure de ligne entre un nombre et son unité.
  const insecables = (t: string) =>
    t.replace(/ (%|points?\b|pt\b)/g, '\u00a0$1').replace(/(\d) (\d{3})/g, '$1\u00a0$2');
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
  /* Une règle plutôt que des cartes : filet épais en tête, un filet par réponse. */
  .sommaire {
    margin: 2rem 0 1rem;
  }
  h2 {
    font-size: var(--t-2);
    font-weight: 600;
    color: var(--ardoise);
    margin: 0 0 0.6rem;
  }
  ol {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(11.5rem, 1fr));
    column-gap: 1.5rem;
    border-top: 2px solid var(--encre);
  }
  a {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    height: 100%;
    padding: 0.8rem 0 1rem;
    border-bottom: 1px solid var(--reglure);
    text-decoration: none;
    color: var(--ardoise);
    font-size: var(--t-0);
    line-height: 1.4;
  }
  .question {
    text-wrap: balance;
    font-weight: 600;
    color: var(--encre);
    font-size: 0.9rem;
  }
  a:hover .question,
  a:focus-visible .question {
    text-decoration: underline;
    text-decoration-color: var(--repere);
    text-decoration-thickness: 2px;
    text-underline-offset: 3px;
  }
  .chiffre {
    font-family: var(--titre);
    font-size: var(--t-3);
    white-space: nowrap;
    font-weight: 700;
    color: var(--encre);
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
    margin-top: 0.15rem;
  }
  /* Petit écran : une ligne par réponse (question et chiffre), la phrase en dessous. */
  @media (max-width: 599px) {
    ol {
      grid-template-columns: 1fr;
    }
    a {
      display: grid;
      grid-template-columns: 1fr auto;
      column-gap: 0.75rem;
      padding: 0.6rem 0;
    }
    .chiffre {
      grid-column: 2;
      grid-row: 1;
      font-size: var(--t-2);
      margin-top: 0;
    }
    .reponse-courte {
      grid-column: 1 / -1;
    }
  }
</style>
