import { incertitudes } from '$lib/server/donnees';

export const load = () => ({
  incertitudes: Object.entries(incertitudes())
    .map(([code, u]) => ({ code, ...u }))
    .sort((a, b) => Number(a.code.slice(1)) - Number(b.code.slice(1)))
});
