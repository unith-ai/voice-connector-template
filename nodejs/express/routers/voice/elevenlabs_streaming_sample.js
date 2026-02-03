const axios = require('axios');

async function makeElevenlabsStreamTtsSample(voiceId, text) {
    // voiceId follows this pattern: EXAVITQu4vr4xnSDxMaL
    if (!text) {
        throw new Error("Text cannot be empty");
    }

    if (!voiceId) {
        throw new Error("Voice ID and model cannot be empty");
    }

    const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream?output_format=pcm_16000`;

    const headers = {
        'xi-api-key': '** [your provider api key] **',
        'content-type': 'application/json'
    };

    const payload = {
        text: text,
        model_id: 'eleven_turbo_v2_5', // the model you want to use which is related to the voice id
    };

    try {
        console.log(`Starting streaming request for voice ${voiceId}`);
        const response = await axios({
            method: 'post',
            url: url,
            headers: headers,
            data: payload,
            responseType: 'stream',
        });

        return response.data;
    } catch (error) {
        console.error(`Error in streaming TTS: ${error.message}`);
        if (error.response) {
            // It's important to read the stream error if possible, but axios error handling with streams can be tricky
            throw new Error(`ElevenLabs API error: ${error.response.status}`);
        }
        throw error;
    }
}

module.exports = { makeElevenlabsStreamTtsSample };
