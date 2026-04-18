# from flask import Flask, request, jsonify
# from ultralytics import YOLO
# from faster_whisper import WhisperModel
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# import edge_tts
# import asyncio
# import os

# app = Flask(__name__)

# # -------------------------
# # LOAD MODELS (once!)
# # -------------------------

# # YOLO (GPU)
# yolo_model = YOLO("yolov8n.pt")

# # Whisper (CPU)
# whisper_model = WhisperModel("base", device="cpu")

# # LLM (GPU)
# model_id = "microsoft/phi-2"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# llm_model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     torch_dtype=torch.float16
# ).to("cuda")

# # -------------------------
# # FUNCTIONS
# # -------------------------

# def detect_objects(image_path):
#     results = yolo_model(image_path, device=0)
#     names = results[0].names
#     classes = results[0].boxes.cls.tolist()

#     objects = [names[int(c)] for c in classes]
#     return list(set(objects))


# def speech_to_text(audio_path):
#     segments, _ = whisper_model.transcribe(audio_path)
#     return " ".join([seg.text for seg in segments])


# def generate_label(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

#     outputs = llm_model.generate(
#         **inputs,
#         max_new_tokens=10,
#         do_sample=False
#     )

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


# async def tts_async(text, output_file="output.mp3"):
#     communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
#     await communicate.save(output_file)
#     return output_file


# def text_to_speech(text):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(tts_async(text))


# # -------------------------
# # ROUTES
# # -------------------------

# @app.route("/detect", methods=["POST"])
# def detect():
#     file = request.files["image"]
#     path = "temp_image.jpg"
#     file.save(path)

#     objects = detect_objects(path)
#     return jsonify({"objects": objects})


# @app.route("/transcribe", methods=["POST"])
# def transcribe():
#     file = request.files["audio"]
#     path = "temp_audio.m4a"
#     file.save(path)

#     text = speech_to_text(path)
#     return jsonify({"text": text})


# @app.route("/label", methods=["POST"])
# def label():
#     data = request.json
#     prompt = data["prompt"]

#     result = generate_label(prompt)
#     return jsonify({"label": result})


# @app.route("/tts", methods=["POST"])
# def tts_route():
#     data = request.json
#     text = data["text"]

#     output = text_to_speech(text)
#     return jsonify({"audio_file": output})


# @app.route("/pipeline", methods=["POST"])
# def full_pipeline():
#     image = request.files["image"]
#     audio = request.files["audio"]

#     image_path = "temp_image.jpg"
#     audio_path = "temp_audio.m4a"

#     image.save(image_path)
#     audio.save(audio_path)

#     objects = detect_objects(image_path)
#     speech = speech_to_text(audio_path)

#     prompt = f"""
#     Objects: {objects}
#     User said: {speech}
#     Give a single label:
#     """

#     label = generate_label(prompt)
#     audio_file = text_to_speech(label)

#     return jsonify({
#         "objects": objects,
#         "speech": speech,
#         "label": label,
#         "audio": audio_file
#     })


# # -------------------------
# # RUN
# # -------------------------

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from ultralytics import YOLO
from faster_whisper import WhisperModel
import google.generativeai as genai
import requests
import os
import torch
import asyncio

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# -------------------------
# LOAD MODELS ONCE
# -------------------------

yolo_model = YOLO("yolov8n.pt")
whisper_model = WhisperModel("base", device="cpu")

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

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
def text_to_speech(text, output_file="output.mp3"):
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

    with open(output_file, "wb") as f:
        f.write(r.content)

    return output_file


# -------------------------
# MAIN PIPELINE ROUTE
# -------------------------
@app.route("/pipeline", methods=["POST"])
def pipeline():
    image = request.files.get("image")
    audio = request.files.get("audio")

    image_path = "temp.jpg"
    audio_path = "temp.wav"

    image.save(image_path)
    audio.save(audio_path)

    objects = detect_objects(image_path)
    speech = speech_to_text(audio_path)

    label = generate_label(objects, speech)
    audio_file = text_to_speech(label)

    return jsonify({
        "objects": objects,
        "speech": speech,
        "label": label,
        "audio": audio_file
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)