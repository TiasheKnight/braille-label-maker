import AsyncStorage from '@react-native-async-storage/async-storage';
import { fetchLabels, LabelRow } from './api';

export interface HistoryEntry {
  id: string;
  word: string;
  braille: string;
  brailleDots: string;
  timestamp: number;
  favorited: boolean;
  mode: 'voice' | 'image';
}

const FAVORITES_KEY = 'braille_favorite_ids';

function parseDbTimestamp(ts: string): number {
  const normalized = ts.includes('T') ? ts : `${ts.replace(' ', 'T')}`;
  const ms = Date.parse(normalized);
  return Number.isNaN(ms) ? Date.now() : ms;
}

async function getFavoriteIds(): Promise<Set<string>> {
  try {
    const raw = await AsyncStorage.getItem(FAVORITES_KEY);
    if (!raw) return new Set();
    const arr: string[] = JSON.parse(raw);
    return new Set(arr);
  } catch {
    return new Set();
  }
}

function rowToEntry(row: LabelRow, favoriteIds: Set<string>): HistoryEntry {
  return {
    id: String(row.id),
    word: row.english,
    braille: row.braille,
    brailleDots: row.braille_dots,
    timestamp: parseDbTimestamp(row.timestamp),
    favorited: favoriteIds.has(String(row.id)),
    mode: row.mode === 'image' ? 'image' : 'voice',
  };
}

/** Loads all labels from the backend database (GET /labels). */
export async function getHistory(): Promise<HistoryEntry[]> {
  try {
    const [labels, favoriteIds] = await Promise.all([fetchLabels(), getFavoriteIds()]);
    return labels.map((row) => rowToEntry(row, favoriteIds));
  } catch {
    return [];
  }
}

export async function toggleFavorite(id: string): Promise<void> {
  const favs = await getFavoriteIds();
  if (favs.has(id)) favs.delete(id);
  else favs.add(id);
  await AsyncStorage.setItem(FAVORITES_KEY, JSON.stringify([...favs]));
}

export function groupByDate(entries: HistoryEntry[]): Record<string, HistoryEntry[]> {
  const groups: Record<string, HistoryEntry[]> = {};
  for (const entry of entries) {
    const date = new Date(entry.timestamp);
    const label = date.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });
    if (!groups[label]) groups[label] = [];
    groups[label].push(entry);
  }
  return groups;
}
