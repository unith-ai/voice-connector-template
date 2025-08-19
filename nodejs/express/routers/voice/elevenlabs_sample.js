const stream = require('stream');
const util = require('util');
const axios = require('axios');
const wavefile = require('wavefile');

function pcmToWav(pcmData) {
    // Create a new WAV file
    const wav = new wavefile.WaveFile();

    // Set WAV properties (mono, 16-bit, 16kHz)
    wav.fromScratch(1, 16000, '16', pcmData);

    // Return WAV buffer
    return Buffer.from(wav.toBuffer());
}

async function makeElevenlabsTtsSample(voiceId, text) {
    // voiceId follows this pattern: EXAVITQu4vr4xnSDxMaL
    const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=pcm_16000`;

    const headers = {
        'xi-api-key': '** [your provider api key] **',
        'content-type': 'application/json'
    };

    const payload = {
        text: text,
        model_id: 'eleven_turbo_v2_5', // the model you want to use which is related to the voice id
        voice_settings: {} // optional
    };

    try {
        const response = await axios({
            method: 'post',
            url: url,
            headers: headers,
            data: payload,
            responseType: 'arraybuffer',
        });

        // Convert PCM data to WAV
        return pcmToWav(response.data);
    } catch (error) {
        // Handle errors
        if (error.response) {
            throw new Error(`ElevenLabs API error: ${error.response.status} - ${error.response.statusText}`);
        } else {
            throw error;
        }
    }
}

module.exports = { makeElevenlabsTtsSample };
