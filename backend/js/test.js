const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

const BASE_URL = "https://anatomist-waving-sternness.ngrok-free.dev";

// ------------------
// TEST CONNECTION
// ------------------
async function testPing() {
    const res = await axios.get(`${BASE_URL}/ping`);
    console.log("Connection:", res.data);
}

// ------------------
// TEST IMAGE PIPELINE
// ------------------
async function testImagePipeline() {
    const form = new FormData();
    form.append("image", fs.createReadStream("test.jpg"));

    const res = await axios.post(`${BASE_URL}/image_pipeline`, form, {
        headers: form.getHeaders()
    });

    console.log("Image Pipeline:", res.data);
}

// ------------------
// TEST AUDIO PIPELINE
// ------------------
async function testAudioPipeline() {
    const form = new FormData();
    form.append("audio", fs.createReadStream("audio.m4a"));

    const res = await axios.post(`${BASE_URL}/audio_pipeline`, form, {
        headers: form.getHeaders()
    });

    console.log("Audio Pipeline:", res.data);
}

// ------------------
// TEST CONFIRM
// ------------------
async function testConfirm() {
    const form = new FormData();
    form.append("audio", fs.createReadStream("confirm.m4a"));

    const res = await axios.post(`${BASE_URL}/confirm`, form, {
        headers: form.getHeaders()
    });

    console.log("Confirm:", res.data);
}

// ------------------
// TEST PRINT
// ------------------
async function testPrint() {
    const res = await axios.post(`${BASE_URL}/print`, {
        label: "test"
    });

    console.log("Print:", res.data);
}

// Run tests
(async () => {
    try {
        await testPing();
        await testImagePipeline();
        await testAudioPipeline();
        await testConfirm();
        await testPrint();
    } catch (error) {
        console.error("Test failed:", error.response ? error.response.data : error.message);
    }
})();