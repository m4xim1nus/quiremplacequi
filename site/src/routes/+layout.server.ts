import { meta } from '$lib/server/donnees';

export const load = () => ({ genereLe: meta().genere_le.slice(0, 10) });
