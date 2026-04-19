import React, { useRef, useState, useCallback, useEffect } from 'react';
import { CameraView, useCameraPermissions } from 'expo-camera';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  ScrollView,
  Pressable,
  StatusBar,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Audio } from 'expo-av';
import * as Speech from 'expo-speech';
import { Ionicons } from '@expo/vector-icons';
import { RootStackParamList } from '../App';
import { sendVoiceRecording, sendImage, sendConfirmation, sendPrint, PipelineResponse } from '../utils/api';
import { addHistoryEntry } from '../utils/history';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

type AppState =
  | 'idle'
  | 'recording'
  | 'processing'
  | 'confirming'
  | 'confirm_recording'
  | 'scanning'
  | 'done';

type Nav = NativeStackNavigationProp<RootStackParamList, 'Home'>;
type HoldMode = 'voice' | 'scan';

const HOLD_DELAY_MS = 1000;
const ResolvedCameraView: any = (CameraView as any)?.default ?? (CameraView as any);

export default function HomeScreen() {
  const navigation = useNavigation<Nav>();
  const insets = useSafeAreaInsets();
  const scrollRef = useRef<ScrollView>(null);
  const recordingRef = useRef<Audio.Recording | null>(null);
  const cameraRef = useRef<any>(null);
  const holdTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const holdModeRef = useRef<HoldMode | null>(null);
  const isSwipingRef = useRef(false);
  const [activePage, setActivePage] = useState(0);
  const [appState, setAppState] = useState<AppState>('idle');
  const [pendingResult, setPendingResult] = useState<PipelineResponse | null>(null);
  const [statusLabel, setStatusLabel] = useState('');
  const [permission, requestPermission] = useCameraPermissions();
  const [showCamera, setShowCamera] = useState(false);

  const ensureAudioPermission = async () => {
    const { status } = await Audio.requestPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Microphone access is required.');
      return false;
    }
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
    });
    return true;
  };

  const cancelPendingHold = useCallback(() => {
    if (holdTimerRef.current) {
      clearTimeout(holdTimerRef.current);
      holdTimerRef.current = null;
    }
    holdModeRef.current = null;
  }, []);

  const startVoiceRecording = useCallback(async () => {
    if (appState !== 'idle' && appState !== 'done') return;

    const ok = await ensureAudioPermission();
    if (!ok) return;

    Speech.speak('Recording started. Release to finish and send.', { language: 'en' });
    setStatusLabel('Listening… release to send');
    setAppState('recording');

    // Wait 5 seconds for speech to finish and phone to settle before recording
    await new Promise(resolve => setTimeout(resolve, 5000));

    const recording = new Audio.Recording();
    await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
    await recording.startAsync();
    recordingRef.current = recording;
  }, [appState]);

  const startScanSensor = useCallback(async () => {
    if (appState !== 'idle' && appState !== 'done') return;
    if (!permission || !permission.granted) {
      const { status } = await requestPermission();
      if (status !== 'granted') {
        Alert.alert('Permission needed', 'Camera access is required.');
        return;
      }
    }
    Speech.stop();
    Speech.speak('Camera activated. Release to take photo.', { language: 'en' });
    setShowCamera(true);
    setAppState('scanning');
    setStatusLabel('Camera activated… release to take photo');
  }, [appState, permission, requestPermission]);

  const scheduleHoldStart = useCallback(
    (mode: HoldMode) => {
      if (isSwipingRef.current) return;
      if (appState !== 'idle' && appState !== 'done') return;

      cancelPendingHold();
      holdModeRef.current = mode;
      setStatusLabel(mode === 'voice' ? 'Hold 1 second for voice' : 'Hold 1 second for sensor');

      holdTimerRef.current = setTimeout(() => {
        if (isSwipingRef.current || holdModeRef.current !== mode) return;

        if (mode === 'voice') {
          void startVoiceRecording();
        } else {
          startScanSensor();
        }

        holdTimerRef.current = null;
      }, HOLD_DELAY_MS);
    },
    [appState, cancelPendingHold, startVoiceRecording, startScanSensor]
  );

  const handleVoicePressIn = useCallback(() => {
    if (activePage !== 0) return;
    scheduleHoldStart('voice');
  }, [activePage, scheduleHoldStart]);

  const handleVoicePressOut = useCallback(async () => {
    if (holdModeRef.current === 'voice' && holdTimerRef.current) {
      cancelPendingHold();
      setStatusLabel('');
      Speech.stop();
      Speech.speak('Hold to start voice input', { language: 'en' });
      return;
    }

    if (appState !== 'recording' || !recordingRef.current) return;

    const recording = recordingRef.current;
    recordingRef.current = null;

    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      if (!uri) throw new Error('No audio URI');

      setAppState('processing');
      setStatusLabel('Processing…');

      const result = await sendVoiceRecording(uri);
      setPendingResult(result);

      // Play the audio
      const sound = new Audio.Sound();
      await sound.loadAsync({ uri: `data:audio/mp3;base64,${result.audio}` });
      await sound.playAsync();

      if (result.label) {
        setAppState('confirming');
        setStatusLabel(`"${result.label}" — say Confirm to print`);
        // Start confirm recording after audio
        setTimeout(() => {
          void startConfirmRecording(result);
        }, 3000); // Adjust time based on audio length
      } else {
        setAppState('idle');
        setStatusLabel('');
        setPendingResult(null);
      }
    } catch (err) {
      console.error(err);
      setAppState('idle');
      setStatusLabel('');
      Speech.speak('Something went wrong. Hold to try again.', { language: 'en' });
    }
  }, [appState, cancelPendingHold]);

  const handleScanPressIn = useCallback(() => {
    if (activePage !== 1) return;
    scheduleHoldStart('scan');
  }, [activePage, scheduleHoldStart]);

  const handleScanPressOut = useCallback(async () => {
    if (holdModeRef.current === 'scan' && holdTimerRef.current) {
      cancelPendingHold();
      setStatusLabel('');
      setShowCamera(false);
      Speech.stop();
      Speech.speak('Hold to start camera scanning', { language: 'en' });
      return;
    }

    if (appState !== 'scanning') return;

    try {
      const photo = await cameraRef.current?.takePictureAsync();
      if (!photo?.uri) throw new Error('No photo taken');

      setShowCamera(false);
      setAppState('processing');
      setStatusLabel('Processing…');

      const result = await sendImage(photo.uri);
      setPendingResult(result);

      // Play the audio
      const sound = new Audio.Sound();
      await sound.loadAsync({ uri: `data:audio/mp3;base64,${result.audio}` });
      await sound.playAsync();

      if (result.label) {
        setAppState('confirming');
        setStatusLabel(`"${result.label}" — say Confirm to print`);
        // Start confirm recording after audio
        setTimeout(() => {
          void startConfirmRecording(result);
        }, 3000);
      } else {
        setAppState('idle');
        setStatusLabel('');
        setPendingResult(null);
      }
    } catch (err) {
      console.error(err);
      setAppState('idle');
      setStatusLabel('');
      setShowCamera(false);
      Speech.speak('Something went wrong. Hold to try again.', { language: 'en' });
    }
  }, [appState, cancelPendingHold]);

const startConfirmRecording = async (result: PipelineResponse) => {
  if (!result.label) return;

  const label = result.label; // ✅ now guaranteed string

  const ok = await ensureAudioPermission();
  if (!ok) return;

  setAppState('confirm_recording');
  setStatusLabel('Say "Confirm" or "Cancel"');

  const confirmRec = new Audio.Recording();
  await confirmRec.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
  await confirmRec.startAsync();

  setTimeout(async () => {
    try {
      await confirmRec.stopAndUnloadAsync();
      const uri = confirmRec.getURI();
      if (!uri) return;

      const confirmation = await sendConfirmation(uri);
      if (confirmation.confirmed) {
        const printResult = await sendPrint(label); // ✅ no error

        await addHistoryEntry({
          word: label,
          braille: printResult.braille,
          brailleDots: printResult.braille_dots,
          mode: activePage === 0 ? 'voice' : 'image',
        });

        Speech.speak(`${label} sent to printer.`, { language: 'en' });
        setStatusLabel('Sent to printer ✓');
      } else {
        Speech.speak('Cancelled. Tap to try again.', { language: 'en' });
        setStatusLabel('Cancelled');
      }
    } catch {
      setStatusLabel('Error — tap to retry');
    }

    setTimeout(() => {
      setAppState('idle');
      setStatusLabel('');
      setPendingResult(null);
      setShowCamera(false);
    }, 2000);
}, 3000);
};

  const speakPagePrompt = useCallback((page: number) => {
    const label = page === 0 ? 'Hold to start voice input' : 'Hold to start camera';
    Speech.stop();
    Speech.speak(label, { language: 'en' });
  }, []);

  useEffect(() => {
    speakPagePrompt(0);
  }, [speakPagePrompt]);

  const handleMomentumScrollEnd = (e: any) => {
    const page = Math.round(e.nativeEvent.contentOffset.x / SCREEN_WIDTH);
    setActivePage(page);
    speakPagePrompt(page);
    isSwipingRef.current = false;
  };

  const handleScrollBeginDrag = () => {
    isSwipingRef.current = true;
    cancelPendingHold();
  };

  const handleScrollEndDrag = () => {
    setTimeout(() => {
      isSwipingRef.current = false;
    }, 120);
  };

  const busy = appState !== 'idle' && appState !== 'done';

  const voiceTitle = () => {
    if (appState === 'recording' || appState === 'confirm_recording') return 'Recording…';
    if (appState === 'processing') return 'Processing…';
    if (appState === 'confirming') return 'Confirming…';
    return 'Voice Input';
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ScrollView
        ref={scrollRef}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onScrollBeginDrag={handleScrollBeginDrag}
        onScrollEndDrag={handleScrollEndDrag}
        onMomentumScrollEnd={handleMomentumScrollEnd}
        scrollEnabled={!busy}
        style={styles.scroller}
      >
        {/* PAGE 1 — VOICE */}
        <Pressable
          style={[styles.page, styles.orangePage]}
          onPressIn={handleVoicePressIn}
          onPressOut={handleVoicePressOut}
          accessible
          accessibilityLabel="Hold to record and release to finish"
          accessibilityRole="button"
        >
          {/* History button */}
          <TouchableOpacity
            style={[styles.historyBtn, { top: insets.top + 12 }]}
            onPress={() => navigation.navigate('History')}
          >
            <Ionicons name="time-outline" size={26} color="#fff" />
          </TouchableOpacity>

          {/* Title */}
          <View style={[styles.titleBlock, { top: insets.top + 70 }]}>
            <Text style={styles.titleLight}>Hold To</Text>
            <Text style={styles.titleLight}>Start</Text>
            <Text style={styles.titleBold}>{voiceTitle()}</Text>
          </View>

          {/* Status */}
          {statusLabel ? (
            <Text style={styles.statusLabel}>{statusLabel}</Text>
          ) : null}

          {/* Icon */}
          <View style={styles.iconArea}>
            {appState === 'processing' ? (
              <ActivityIndicator size="large" color="#fff" />
            ) : (
              <Ionicons
                name={busy ? 'radio' : 'mic-outline'}
                size={72}
                color="#fff"
              />
            )}
          </View>

          {/* Dots */}
          <View style={[styles.dots, { bottom: insets.bottom + 32 }]}>
            <View style={[styles.dot, activePage === 0 && styles.dotActive]} />
            <View style={[styles.dot, activePage === 1 && styles.dotActive]} />
          </View>
        </Pressable>

        {/* PAGE 2 — SCAN */}
        <Pressable
          style={[styles.page, styles.bluePage]}
          onPressIn={handleScanPressIn}
          onPressOut={handleScanPressOut}
          accessible
          accessibilityLabel="Hold to start camera and release to finish"
          accessibilityRole="button"
        >
          <TouchableOpacity
            style={[styles.historyBtn, { top: insets.top + 12 }]}
            onPress={() => navigation.navigate('History')}
          >
            <Ionicons name="time-outline" size={26} color="#fff" />
          </TouchableOpacity>

          <View style={[styles.titleBlock, { top: insets.top + 70 }]}> 
            <Text style={styles.titleLight}>Hold To</Text>
            <Text style={styles.titleLight}>Start</Text>
            <Text style={styles.titleBold}>Camera</Text>
            <Text style={styles.titleBold}>Scanning</Text>
          </View>

          {statusLabel ? (
            <Text style={styles.statusLabel}>{statusLabel}</Text>
          ) : null}

          <View style={showCamera ? styles.cameraPreviewArea : styles.iconArea}>
            {showCamera && permission && permission.granted ? (
              <View style={{ width: 220, height: 220, borderRadius: 16, overflow: 'hidden', backgroundColor: '#222' }}>
                <ResolvedCameraView
                  ref={cameraRef}
                  style={{ flex: 1 }}
                  facing="back"
                />
              </View>
            ) : (
              <Ionicons name={appState === 'scanning' ? 'scan-circle' : 'camera-outline'} size={72} color="#fff" />
            )}
          </View>

          <View style={[styles.dots, { bottom: insets.bottom + 32 }]}> 
            <View style={[styles.dot, activePage === 0 && styles.dotActive]} />
            <View style={[styles.dot, activePage === 1 && styles.dotActive]} />
          </View>
        </Pressable>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroller: { flex: 1 },
  page: { width: SCREEN_WIDTH, flex: 1 },
  orangePage: { backgroundColor: '#F47B20' },
  bluePage: { backgroundColor: '#1AABF0' },

  historyBtn: {
    position: 'absolute',
    right: 20,
    zIndex: 10,
    padding: 8,
  },

  titleBlock: {
    position: 'absolute',
    left: 32,
  },
  titleLight: {
    fontSize: 44,
    fontWeight: '300',
    color: '#fff',
    lineHeight: 50,
  },
  titleBold: {
    fontSize: 44,
    fontWeight: '800',
    color: '#fff',
    lineHeight: 54,
  },

  statusLabel: {
    position: 'absolute',
    bottom: 200,
    left: 32,
    right: 32,
    color: 'rgba(255,255,255,0.9)',
    fontSize: 16,
    fontWeight: '500',
    textAlign: 'center',
  },

  iconArea: {
    position: 'absolute',
    bottom: 110,
    left: 0,
    right: 0,
    alignItems: 'center',
  },

  cameraPreviewArea: {
    position: 'absolute',
    top: '50%',
    left: 0,
    right: 0,
    marginTop: -110,
    alignItems: 'center',
  },

  dots: {
    position: 'absolute',
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: 'rgba(255,255,255,0.4)',
  },
  dotActive: { backgroundColor: '#fff' },
});
