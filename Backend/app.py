from flask import Flask, request, jsonify
from ultralytics import YOLO
from faster_whisper import WhisperModel
import google.generativeai as genai
import requests
import os
import torch
import asyncio
from flask_cors import CORS
import base64

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# -------------------------
# LOAD MODELS ONCE
# -------------------------

yolo_model = YOLO("yolov8n.pt")
whisper_model = WhisperModel("base", device="cpu")

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------
# BRAILLE PATTERNS
# -------------------------
braille_patterns = {
    'a': [1,0,0,0,0,0],
    'b': [1,1,0,0,0,0],
    'c': [1,0,0,1,0,0],
    'd': [1,0,0,1,1,0],
    'e': [1,0,0,0,1,0],
    'f': [1,1,0,1,0,0],
    'g': [1,1,0,1,1,0],
    'h': [1,1,0,0,1,0],
    'i': [0,1,0,1,0,0],
    'j': [0,1,0,1,1,0],
    'k': [1,0,1,0,0,0],
    'l': [1,1,1,0,0,0],
    'm': [1,0,1,1,0,0],
    'n': [1,0,1,1,1,0],
    'o': [1,0,1,0,1,0],
    'p': [1,1,1,1,0,0],
    'q': [1,1,1,1,1,0],
    'r': [1,1,1,0,1,0],
    's': [0,1,1,1,0,0],
    't': [0,1,1,1,1,0],
    'u': [1,0,1,0,0,1],
    'v': [1,1,1,0,0,1],
    'w': [0,1,0,1,1,1],
    'x': [1,0,1,1,0,1],
    'y': [1,0,1,1,1,1],
    'z': [1,0,1,0,1,1],
    ' ': [0,0,0,0,0,0],
}

# -------------------------
# ENCODE TO BRAILLE
# -------------------------
def encode_to_braille(text):
    result = []
    unicode_braille = ""
    braille_dots = ""
    for char in text.lower():
        if char in braille_patterns:
            bits = braille_patterns[char]
            left = bits[:3]
            right = bits[3:]
            result.append([left, right])
            # unicode
            dot_nums = [i+1 for i,b in enumerate(bits) if b]
            val = sum(1 << (i-1) for i in dot_nums)
            unicode_braille += chr(0x2800 + val)
            # dots
            dots = "-".join(str(i+1) for i,b in enumerate(bits) if b)
            if braille_dots:
                braille_dots += " "
            braille_dots += dots
    return result, unicode_braille, braille_dots

# -------------------------
# YOLO DETECTION
# -------------------------
def detect_objects(image_path):
    results = yolo_model(image_path, device=0)
    names = results[0].names
    classes = results[0].boxes.cls.tolist()

    objects = [names[int(c)] for c in classes]
    return list(set(objects))


# -------------------------
# SPEECH TO TEXT
# -------------------------
def speech_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments])


# -------------------------
# GEMINI LABEL GENERATION (FAST + SMART)
# -------------------------
def generate_label(objects, speech_text):
    prompt = f"""
You are a labeling system.

Objects detected: {objects}
User speech: "{speech_text}"

Return ONLY a short label (max 8 words).
No explanation.
"""

    response = gemini_model.generate_content(prompt)
    return response.text.strip()


# -------------------------
# ELEVENLABS TTS (FAST CLOUD VOICE)
# -------------------------
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{os.getenv('ELEVENLABS_VOICE_ID')}"

    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    r = requests.post(url, json=data, headers=headers)

    return base64.b64encode(r.content).decode()


# -------------------------
# IMAGE PIPELINE ROUTE
# -------------------------
@app.route("/image_pipeline", methods=["POST"])
def image_pipeline():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "No image provided"}), 400

    image_path = "temp.jpg"
    image.save(image_path)

    objects = detect_objects(image_path)
    if not objects:
        audio_file = text_to_speech("please try again")
        return jsonify({"audio": audio_file, "label": None})

    label = generate_label(objects, "")
    audio_file = text_to_speech(f"is this a {label}")
    return jsonify({"audio": audio_file, "label": label})

# -------------------------
# AUDIO PIPELINE ROUTE
# -------------------------
@app.route("/audio_pipeline", methods=["POST"])
def audio_pipeline():
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"error": "No audio provided"}), 400

    audio_path = "temp.wav"
    audio.save(audio_path)

    speech = speech_to_text(audio_path)
    if not speech.strip():
        audio_file = text_to_speech("please try again")
        return jsonify({"audio": audio_file, "label": None})

    label = generate_label([], speech)
    audio_file = text_to_speech(f"is this a {label}")
    return jsonify({"audio": audio_file, "label": label})

# -------------------------
# PRINT ROUTE
# -------------------------
@app.route("/print", methods=["POST"])
def print_label():
    data = request.get_json()
    label = data.get("label")
    if not label:
        return jsonify({"error": "No label provided"}), 400

    encoded, braille, braille_dots = encode_to_braille(label)
    # TODO: Send encoded to ESP32 for printing
    return jsonify({"encoded": encoded, "braille": braille, "braille_dots": braille_dots})

# -------------------------
# CONFIRM ROUTE
# -------------------------
@app.route("/confirm", methods=["POST"])
def confirm():
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"confirmed": False}), 400

    audio_path = "temp_confirm.wav"
    audio.save(audio_path)

    speech = speech_to_text(audio_path)
    confirmed = "yes" in speech.lower() or "confirm" in speech.lower()
    return jsonify({"confirmed": confirmed})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)