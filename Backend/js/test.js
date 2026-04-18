const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

const BASE_URL = "http://localhost:5000";

// ------------------
// TEST IMAGE DETECTION
// ------------------
async function testDetect() {
    const form = new FormData();
    form.append("image", fs.createReadStream("test.jpg"));

    const res = await axios.post(`${BASE_URL}/detect`, form, {
        headers: form.getHeaders()
    });

    console.log("Detect:", res.data);
}

// ------------------
// TEST SPEECH
// ------------------
async function testTranscribe() {
    const form = new FormData();
    form.append("audio", fs.createReadStream("audio.m4a"));

    const res = await axios.post(`${BASE_URL}/transcribe`, form, {
        headers: form.getHeaders()
    });

    console.log("Speech:", res.data);
}

// ------------------
// TEST LLM
// ------------------
async function testLabel() {
    const res = await axios.post(`${BASE_URL}/label`, {
        prompt: "Objects: pills, bottle. User said: these are my pills. Label:"
    });

    console.log("Label:", res.data);
}

// ------------------
// TEST TTS
// ------------------
async function testTTS() {
    const res = await axios.post(`${BASE_URL}/tts`, {
        text: "These are medicines"
    });

    console.log("TTS:", res.data);
}

// ------------------
// FULL PIPELINE
// ------------------
async function testPipeline() {
    const form = new FormData();
    form.append("image", fs.createReadStream("test.jpg"));
    form.append("audio", fs.createReadStream("audio.m4a"));

    const res = await axios.post(`${BASE_URL}/pipeline`, form, {
        headers: form.getHeaders()
    });

    console.log("Pipeline:", res.data);
}

// Run tests
(async () => {
    await testDetect();
    await testTranscribe();
    await testLabel();
    await testTTS();
    await testPipeline();
})();