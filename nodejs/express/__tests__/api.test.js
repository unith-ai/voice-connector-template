const request = require('supertest');
const express = require('express');
const healthRouter = require('../routers/health_check/health_handler');
const voiceRouter = require('../routers/voice/voice_handler');

// Mock the elevenlabs integration
jest.mock('../routers/voice/elevenlabs_sample', () => ({
  makeElevenlabsTtsSample: jest.fn().mockResolvedValue(Buffer.from('fake-wav-data'))
}));

describe('Express API Tests', () => {
  let app;

  beforeEach(() => {
    // Create a fresh app instance for each test
    app = express();
    app.use(express.json());
    app.use('/', healthRouter);
    app.use('/', voiceRouter);
  });

  describe('Health Check Endpoint', () => {
    test('GET /health-check should return 200 with health status', async () => {
      const response = await request(app)
        .get('/health-check')
        .expect(200)
        .expect('Content-Type', /json/);

      expect(response.body).toHaveProperty('message', 'OK');
      expect(response.body).toHaveProperty('version', '0.0.1');
      expect(response.body).toHaveProperty('hostname');
      expect(typeof response.body.hostname).toBe('string');
    });
  });

  describe('TTS Endpoint', () => {
    const validApiKey = '12345678';
    const testVoice = 'EXAVITQu4vr4xnSDxMaL';
    const testText = 'Hello world';

    test('POST /tts/:voice should return 401 without API key', async () => {
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .send({ text: testText })
        .expect(401)
        .expect('Content-Type', /json/);

      expect(response.body).toHaveProperty('detail', 'Invalid API Key');
    });

    test('POST /tts/:voice should return 401 with invalid API key', async () => {
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .set('unith-voice-x-api', 'wrong-key')
        .send({ text: testText })
        .expect(401);

      expect(response.body).toHaveProperty('detail', 'Invalid API Key');
    });

    test('POST /tts/:voice should return 400 when text is missing', async () => {
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .set('unith-voice-x-api', validApiKey)
        .send({})
        .expect(400)
        .expect('Content-Type', /json/);

      expect(response.body).toHaveProperty('errors');
      expect(Array.isArray(response.body.errors)).toBe(true);
    });

    test('POST /tts/:voice should return 400 when text is empty', async () => {
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .set('unith-voice-x-api', validApiKey)
        .send({ text: '' })
        .expect(400);

      expect(response.body).toHaveProperty('errors');
    });

    test('POST /tts/:voice should return 200 with valid request', async () => {
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .set('unith-voice-x-api', validApiKey)
        .send({ text: testText })
        .expect(200)
        .expect('Content-Type', 'audio/wav');

      expect(response.headers['content-disposition']).toContain('attachment');
      expect(response.headers['content-disposition']).toContain('speech.wav');
      expect(Buffer.isBuffer(response.body)).toBe(true);
    });

    test('POST /tts/:voice should handle different voice IDs', async () => {
      const differentVoice = 'another-voice-id';
      const response = await request(app)
        .post(`/tts/${differentVoice}`)
        .set('unith-voice-x-api', validApiKey)
        .send({ text: testText })
        .expect(200);

      expect(response.headers['content-type']).toBe('audio/wav');
    });

    test('POST /tts/:voice should handle longer text', async () => {
      const longText = 'This is a much longer text that should still be processed correctly by the TTS system.';
      const response = await request(app)
        .post(`/tts/${testVoice}`)
        .set('unith-voice-x-api', validApiKey)
        .send({ text: longText })
        .expect(200);

      expect(response.headers['content-type']).toBe('audio/wav');
    });
  });

  describe('Error Handling', () => {
    test('should handle TTS provider errors gracefully', async () => {
      // Mock the elevenlabs function to throw an error for this test
      const { makeElevenlabsTtsSample } = require('../routers/voice/elevenlabs_sample');
      makeElevenlabsTtsSample.mockRejectedValueOnce(new Error('Provider error'));

      const response = await request(app)
        .post(`/tts/test-voice`)
        .set('unith-voice-x-api', '12345678')
        .send({ text: 'test' })
        .expect(500);

      expect(response.body).toHaveProperty('detail');
      expect(response.body.detail).toContain('Unexpected error');
    });
  });
});
