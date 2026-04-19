from flask import Flask, request, jsonify
from ultralytics import YOLO
from faster_whisper import WhisperModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import edge_tts
import asyncio
import os
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------
# LOAD MODELS (once!)
# -------------------------

# YOLO (GPU)
yolo_model = YOLO("yolov8n.pt")

# Whisper (CPU)
whisper_model = WhisperModel("base", device="cpu")

# LLM (GPU)
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
llm_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16
).to("cuda")

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
# FUNCTIONS
# -------------------------

def detect_objects(image_path):
    results = yolo_model(image_path, device=0)
    names = results[0].names
    classes = results[0].boxes.cls.tolist()

    objects = [names[int(c)] for c in classes]
    return list(set(objects))


def speech_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments])


def generate_label(objects, speech_text):
    # Enforce: use EITHER objects OR speech_text, not both
    if objects and speech_text:
        raise ValueError("Cannot use both objects and speech_text - use one or the other")
    
    if objects:
        prompt = f"Create a one to three word label for the following objects: {', '.join(objects)}."
    elif speech_text:
        prompt = f"Create a one to three word label that summarises:{speech_text}."
    else:
        raise ValueError("Must provide either objects or speech_text")

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    input_length = inputs["input_ids"].shape[1]

    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=15,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

    # Handle both Tensor and dict-like outputs
    if isinstance(outputs, torch.Tensor):
        sequences = outputs.cpu()
    else:
        sequences = outputs.sequences.cpu()
    
    new_tokens = sequences[0][input_length:]
    label = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    # Clean up any trailing punctuation or weird characters
    label = label.split('\n')[0].strip()
    return label


async def tts_async(text, output_file="output.mp3"):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(output_file)
    with open(output_file, "rb") as f:
        audio_data = f.read()
    return base64.b64encode(audio_data).decode()


def text_to_speech(text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(tts_async(text))


# -------------------------
# ROUTES
# -------------------------

@app.route("/image_pipeline", methods=["POST"])
def image_pipeline():
    try:
        print("[IMAGE] Received request")
        image = request.files.get("image")
        if not image:
            print("[IMAGE] No image file found")
            return jsonify({"error": "No image provided"}), 400

        image_path = "temp.jpg"
        image.save(image_path)
        print(f"[IMAGE] Saved image to {image_path}")

        objects = detect_objects(image_path)
        print(f"[IMAGE] Detected objects: {objects}")
        if not objects:
            print("[IMAGE] No objects detected, sending 'please try again'")
            audio_file = text_to_speech("please try again")
            return jsonify({"audio": audio_file, "label": None})

        label = generate_label(objects, "")
        print(f"[IMAGE] Generated label: {label}")
        audio_file = text_to_speech(f"is this a {label}")
        return jsonify({"audio": audio_file, "label": label})
    except Exception as e:
        print(f"[IMAGE] Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/audio_pipeline", methods=["POST"])
def audio_pipeline():
    try:
        print("[AUDIO] Received request")
        audio = request.files.get("audio")
        if not audio:
            print("[AUDIO] No audio file found")
            return jsonify({"error": "No audio provided"}), 400

        audio_path = "temp.wav"
        audio.save(audio_path)
        print(f"[AUDIO] Saved audio to {audio_path}")

        speech = speech_to_text(audio_path)
        print(f"[AUDIO] Transcribed speech: {speech}")
        if not speech.strip():
            print("[AUDIO] Empty transcription, sending 'please try again'")
            audio_file = text_to_speech("please try again")
            return jsonify({"audio": audio_file, "label": None})

        label = generate_label([], speech)
        print(f"[AUDIO] Generated label: {label}")
        audio_file = text_to_speech(f"is this a {label}")
        return jsonify({"audio": audio_file, "label": label})
    except Exception as e:
        print(f"[AUDIO] Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/print", methods=["POST"])
def print_label():
    data = request.get_json()
    label = data.get("label")
    if not label:
        return jsonify({"error": "No label provided"}), 400

    encoded, braille, braille_dots = encode_to_braille(label)
    # TODO: Send encoded to ESP32 for printing
    return jsonify({"encoded": encoded, "braille": braille, "braille_dots": braille_dots})


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "test ok"})


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

# # -------------------------
# # TEST ROUTE
# # -------------------------
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "test ok"})

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)