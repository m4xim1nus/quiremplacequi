// Identité et contacts du site (page « À propos », pied de page). Le site est signé par son dépôt :
// le code, les données et leur historique sont publics, les contributions passent par GitHub.
export const SITE = {
  nom: 'Qui remplace qui ?',
  url: 'https://quiremplacequi.technoperchoir.fr',
  description:
    'La démographie des migrations en France, mesurée avec la statistique publique : combien, depuis quand, à quelle vitesse, qui arrive, qui part, ce que deviennent les enfants.',
  depot: 'https://github.com/m4xim1nus/quiremplacequi',
  tickets: 'https://github.com/m4xim1nus/quiremplacequi/issues',
  contact: 'quiremplacequi.uncork864@passmail.net',
  licenceCode: { nom: 'MIT', url: 'https://opensource.org/license/mit' },
  licenceContenus: { nom: 'CC BY 4.0', url: 'https://creativecommons.org/licenses/by/4.0/deed.fr' }
} as const;
