import { expect, it } from 'vitest';
import { entier, milliers, pct } from './format';

it('formate en français', () => {
  expect(entier(7970000)).toBe('7 970 000'.replaceAll(' ', ' '));
  expect(milliers(7029100)).toBe('7 029 000'.replaceAll(' ', ' '));
  expect(milliers(-26000)).toBe('−26 000');
  expect(pct(11.58)).toBe('11,6\u00a0%');
});
