// Formats d'affichage (français).

const nf = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
const nf1 = new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

/** 7970000 → « 7 970 000 ». */
export const entier = (x: number) => nf.format(x);

/** Arrondi au millier : 7029100 → « 7 029 000 » ; −26000 → « −26 000 ». */
export const milliers = (x: number) => nf.format(Math.round(x / 1000) * 1000).replace('-', '−');

/** 11.58 → « 11,6 % ». */
export const pct = (x: number) => `${nf1.format(x)} %`;
