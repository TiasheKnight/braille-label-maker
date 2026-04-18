// ← Swap this with your teammate's actual URL
const BASE_URL = 'https://YOUR_TEAMMATES_API_URL';

export interface AIResponse {
  word: string;
  braille: string;        // unicode braille e.g. "⠚⠁⠍"
  brailleDots: string;    // dot notation e.g. "245-1-134"
  confirmationText: string; // e.g. "Jam. Say confirm to print."
}

export interface ConfirmResponse {
  confirmed: boolean;
}

export async function sendVoiceRecording(audioUri: string): Promise<AIResponse> {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioUri,
    name: 'recording.m4a',
    type: 'audio/m4a',
  } as any);

  const response = await fetch(`${BASE_URL}/voice`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Voice API error: ${response.status}`);
  return response.json();
}

export async function sendConfirmation(audioUri: string, word: string): Promise<ConfirmResponse> {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioUri,
    name: 'confirm.m4a',
    type: 'audio/m4a',
  } as any);
  formData.append('word', word);

  const response = await fetch(`${BASE_URL}/confirm`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error(`Confirm API error: ${response.status}`);
  return response.json();
}
