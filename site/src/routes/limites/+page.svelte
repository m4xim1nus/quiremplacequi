<script lang="ts">
  let { data } = $props();
</script>

<svelte:head>
  <title>Ce qu’on ne sait pas · Qui remplace qui ?</title>
  <meta
    name="description"
    content="Les manques et les incertitudes de la statistique des migrations, et comment le site les montre."
  />
</svelte:head>

<article class="page colonne">
  <h1>Ce qu’on ne sait pas</h1>
  <p class="chapeau">
    La statistique des migrations est solide, mais elle a des trous : des flux qu’on ne mesure que
    par différence, des séries qui changent de définition, des générations qu’on ne suit que par
    enquête. Chaque incertitude a un code, et chaque graphique du site qui en dépend la montre.
  </p>
  <p class="brouillon">Textes en brouillon.</p>

  <dl class="registre">
    {#each data.incertitudes as u (u.code)}
      <div class="entree" id={u.code}>
        <dt><span class="code">{u.code}</span> {u.titre}</dt>
        <dd>
          <p>{u.detail}</p>
          <p class="traitement"><strong>Sur le site :</strong> {u.traitement}.</p>
          {#if u.reference}<p class="ref">Référence : {u.reference}</p>{/if}
          {#if !u.verifie}<p class="ref">
              À vérifier : incertitude repérée, pas encore documentée sur source.
            </p>{/if}
        </dd>
      </div>
    {/each}
  </dl>
</article>

<style>
  .registre {
    margin: 2rem 0 0;
  }
  .entree {
    padding: 1rem 0;
    border-top: 1px solid var(--reglure);
  }
  dt {
    font-weight: 600;
    font-size: var(--t-2);
  }
  dd {
    margin: 0.3rem 0 0;
  }
  dd p {
    margin: 0.35rem 0;
  }
  .code {
    font-size: var(--t-0);
    color: var(--gris);
    font-variant-numeric: tabular-nums;
    margin-right: 0.3rem;
  }
  .traitement {
    color: var(--ardoise);
  }
  .ref {
    font-size: var(--t-0);
    color: var(--gris);
  }
</style>
