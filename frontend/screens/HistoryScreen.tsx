import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SectionList,
  TouchableOpacity,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { getHistory, toggleFavorite, groupByDate, HistoryEntry } from '../utils/history';

export default function HistoryScreen() {
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();
  const [sections, setSections] = useState<{ title: string; data: HistoryEntry[] }[]>([]);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());

  const load = async () => {
    const entries = await getHistory();
    const grouped = groupByDate(entries);
    const sects = Object.entries(grouped).map(([title, data]) => ({ title, data }));
    setSections(sects);
    setFavorites(new Set(entries.filter((e) => e.favorited).map((e) => e.id)));
  };

  useFocusEffect(useCallback(() => { load(); }, []));

  const handleFavorite = async (id: string) => {
    await toggleFavorite(id);
    setFavorites((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const renderItem = ({ item }: { item: HistoryEntry }) => (
    <View style={styles.entryRow}>
      <View style={styles.entryLeft}>
        <Text style={styles.word}>{item.word}</Text>
        <Text style={styles.braille}>{item.braille || '⠀'}</Text>
      </View>
      <TouchableOpacity onPress={() => handleFavorite(item.id)} style={styles.heartBtn}>
        <Ionicons
          name={favorites.has(item.id) ? 'heart' : 'heart-outline'}
          size={22}
          color={favorites.has(item.id) ? '#F47B20' : '#C0C0C0'}
        />
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={20} color="#1A1A1A" />
          <Text style={styles.backText}>Back</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>History</Text>
        <View style={{ minWidth: 70 }} />
      </View>

      <View style={styles.divider} />

      {sections.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons name="document-text-outline" size={48} color="#D0D0D0" />
          <Text style={styles.emptyText}>No history yet</Text>
          <Text style={styles.emptySubtext}>Words you print will appear here</Text>
        </View>
      ) : (
        <SectionList
          sections={sections}
          keyExtractor={(item) => item.id}
          renderItem={renderItem}
          renderSectionHeader={({ section }) => (
            <Text style={styles.dateHeader}>{section.title}</Text>
          )}
          contentContainerStyle={styles.list}
          ItemSeparatorComponent={() => <View style={styles.separator} />}
          stickySectionHeadersEnabled={false}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  backBtn: { flexDirection: 'row', alignItems: 'center', minWidth: 70 },
  backText: { fontSize: 16, color: '#1A1A1A' },
  headerTitle: { flex: 1, textAlign: 'center', fontSize: 17, fontWeight: '600' },

  divider: { height: StyleSheet.hairlineWidth, backgroundColor: '#E0E0E0' },

  list: { paddingHorizontal: 20, paddingBottom: 40 },

  dateHeader: {
    fontSize: 15,
    fontWeight: '600',
    color: '#F47B20',
    marginTop: 24,
    marginBottom: 12,
  },

  entryRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 10,
  },
  entryLeft: { flex: 1 },
  word: { fontSize: 16, fontWeight: '500', color: '#1A1A1A', marginBottom: 4 },
  braille: { fontSize: 22, color: '#1A1A1A', letterSpacing: 4 },
  heartBtn: { padding: 8 },

  separator: { height: StyleSheet.hairlineWidth, backgroundColor: '#F0F0F0' },

  emptyState: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12 },
  emptyText: { fontSize: 18, fontWeight: '600', color: '#A0A0A0' },
  emptySubtext: { fontSize: 14, color: '#C0C0C0' },
});
