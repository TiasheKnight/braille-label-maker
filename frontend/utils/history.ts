import AsyncStorage from '@react-native-async-storage/async-storage';

export interface HistoryEntry {
  id: string;
  word: string;
  braille: string;
  brailleDots: string;
  timestamp: number;
  favorited: boolean;
  mode: 'voice' | 'scan';
}

const STORAGE_KEY = 'braille_history';

export async function getHistory(): Promise<HistoryEntry[]> {
  try {
    const raw = await AsyncStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export async function addHistoryEntry(
  entry: Omit<HistoryEntry, 'id' | 'timestamp' | 'favorited'>
): Promise<HistoryEntry> {
  const history = await getHistory();
  const newEntry: HistoryEntry = {
    ...entry,
    id: Date.now().toString(),
    timestamp: Date.now(),
    favorited: false,
  };
  history.unshift(newEntry);
  await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  return newEntry;
}

export async function toggleFavorite(id: string): Promise<void> {
  const history = await getHistory();
  const updated = history.map((e) =>
    e.id === id ? { ...e, favorited: !e.favorited } : e
  );
  await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
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
