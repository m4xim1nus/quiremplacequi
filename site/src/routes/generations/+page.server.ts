import { donneesGenerations } from '$lib/server/generations';
import { incertitudes } from '$lib/server/donnees';

export const load = () => {
  const u = incertitudes();
  return {
    d: donneesGenerations(),
    incertitudes: ['U14', 'U15', 'U8', 'U13']
      .filter((c) => u[c])
      .map((code) => ({ code, ...u[code] }))
  };
};
