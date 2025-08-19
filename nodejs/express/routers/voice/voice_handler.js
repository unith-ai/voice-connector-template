const express = require('express');
const { body, validationResult } = require('express-validator');
const {makeElevenlabsTtsSample} = require("./elevenlabs_sample");

const router = express.Router();

/**
 * @swagger
 * /tts/{voice}:
 *   post:
 *     tags:
 *       - Voice
 *     summary: Process text to speech
 *     description: Converts text to speech using the specified voice
 *     security:
 *       - apiKey: []
 *     parameters:
 *       - in: path
 *         name: voice
 *         required: true
 *         schema:
 *           type: string
 *         description: The voice to use for text-to-speech conversion
 *       - in: header
 *         name: unith-voice-x-api
 *         required: true
 *         schema:
 *           type: string
 *         description: API key for authentication
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - text
 *             properties:
 *               text:
 *                 type: string
 *                 description: The text to convert to speech
 *     responses:
 *       200:
 *         description: Audio data in WAV format
 *         content:
 *           audio/wav:
 *             schema:
 *               type: string
 *               format: binary
 *       400:
 *         description: Bad request, missing or invalid parameters
 *       401:
 *         description: Unauthorized, invalid API key
 *       500:
 *         description: Server error
 */
router.post('/tts/:voice', [
  // Validate request body
  body('text').notEmpty().withMessage('Text is required'),
], async (req, res) => {
  // Check for validation errors
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  // Validate API key
  const apiKey = req.header('unith-voice-x-api');
  if (apiKey !== '12345678') {
    return res.status(401).json({ detail: 'Invalid API Key' });
  }

  const voice = req.params.voice;
  const text = req.body.text;

  console.log(`Processing TTS for voice: ${voice} with text: ${text}`);

  try {
    // In a real implementation, this would call a TTS service
    // For now, we'll just return an empty audio buffer
    const audioData = await makeElevenlabsTtsSample(voice, text);

    // Return as a binary response with the correct content type
    res.setHeader('Content-Type', 'audio/wav');
    res.setHeader('Content-Disposition', 'attachment; filename=speech.wav');
    return res.status(200).send(audioData);
  } catch (error) {
    console.error(`Unexpected error: ${error}`);
    return res.status(500).json({ detail: `Unexpected error: ${error.message}` });
  }
});

module.exports = router;
