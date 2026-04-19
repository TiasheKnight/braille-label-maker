// ← Swap this with your teammate's actual URL
const BASE_URL = 'http://165.245.138.5:5000';

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
  formData.append('audio', {
    uri: audioUri,
    name: 'recording.m4a',
    type: 'audio/m4a',
  } as any);

  const response = await fetch(`${BASE_URL}/audio_pipeline`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Audio API error: ${response.status}`);
  return response.json();
}

export async function sendImage(imageUri: string): Promise<PipelineResponse> {
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    name: 'photo.jpg',
    type: 'image/jpeg',
  } as any);

  const response = await fetch(`${BASE_URL}/image_pipeline`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Image API error: ${response.status}`);
  return response.json();
}

export async function sendConfirmation(audioUri: string): Promise<ConfirmResponse> {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioUri,
    name: 'confirm.m4a',
    type: 'audio/m4a',
  } as any);

  const response = await fetch(`${BASE_URL}/confirm`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Confirm API error: ${response.status}`);
  return response.json();
}

export async function sendPrint(label: string): Promise<PrintResponse> {
  const response = await fetch(`${BASE_URL}/print`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({label}),
  });

  if (!response.ok) throw new Error(`Print API error: ${response.status}`);
  return response.json();
}
