/**
 * Mapping of song components from backend-supported keys to user-friendly names.
 */
export const MusicPartMap = new Map([
  ['vocals', 'Vocals'],
  ['piano', 'Piano'],
  ['other', 'Outros (Acomp)'],
  ['bass', 'Bass'],
  ['drums', 'Drums'],
]);

export type MusicParts = 'vocals' | 'piano' | 'other' | 'bass' | 'drums';
