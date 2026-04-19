// ← Replace with your backend's IP address (e.g., http://192.168.1.100:5000 for local network)
const BASE_URL = 'https://anatomist-waving-sternness.ngrok-free.dev';

export interface PipelineResponse {
  audio: string; // base64
  label: string | null;
}

export interface ConfirmResponse {
  confirmed: boolean;
}

export interface PrintResponse {
  encoded: number[][][];
  braille: string;
  braille_dots: string;
}

export async function sendVoiceRecording(audioUri: string): Promise<PipelineResponse> {
  const formData = new FormData();

  if (audioUri.startsWith('blob:')) {
    const blob = await fetch(audioUri).then(r => r.blob());
    formData.append('audio', blob, 'recording.wav');
  } else {
    formData.append('audio', {
      uri: audioUri,
      name: 'recording.wav',
      type: 'audio/wav',
    } as any);
  }

  const response = await fetch(`${BASE_URL}/audio_pipeline`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Audio API error: ${response.status}`);
  return response.json();
}

export async function sendImage(imageUri: string): Promise<PipelineResponse> {
  const formData = new FormData();

  if (imageUri.startsWith('blob:')) {
    const blob = await fetch(imageUri).then(r => r.blob());
    formData.append('image', blob, 'photo.jpg');
  } else {
    formData.append('image', {
      uri: imageUri,
      name: 'photo.jpg',
      type: 'image/jpeg',
    } as any);
  }

  const response = await fetch(`${BASE_URL}/image_pipeline`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Image API error: ${response.status}`);
  return response.json();
}

export async function sendConfirmation(audioUri: string): Promise<ConfirmResponse> {
  const formData = new FormData();

  if (audioUri.startsWith('blob:')) {
    const blob = await fetch(audioUri).then(r => r.blob());
    formData.append('audio', blob, 'confirm.wav');
  } else {
    formData.append('audio', {
      uri: audioUri,
      name: 'confirm.wav',
      type: 'audio/wav',
    } as any);
  }

  const response = await fetch(`${BASE_URL}/confirm`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Confirm API error: ${response.status}`);
  return response.json();
}

export async function sendPrint(label: string, mode: string): Promise<PrintResponse> {
  const response = await fetch(`${BASE_URL}/print`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({label, mode}),
  });

  if (!response.ok) throw new Error(`Print API error: ${response.status}`);
  return response.json();
}
