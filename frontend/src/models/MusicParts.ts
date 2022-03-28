/**
 * Mapping of song components from backend-supported keys to user-friendly names.
 */
export const MusicPartMap = new Map([
  ['vocals', 'Vocais'],
  ['piano', 'Piano'],
  ['other', 'Outros (Acomp)'],
  ['bass', 'Baixo'],
  ['drums', 'Bateria'],
]);

export type MusicParts = 'vocals' | 'piano' | 'other' | 'bass' | 'drums';
