import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import create_app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_elevenlabs():
    """Mock the ElevenLabs TTS integration."""
    with patch('routers.voice.voice_handler.make_elevenlabs_tts_sample') as mock:
        mock.return_value = b'fake-wav-data'
        yield mock


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health check returns 200 OK."""
        response = client.get("/health-check")
        assert response.status_code == 200

    def test_health_check_returns_correct_structure(self, client):
        """Test that health check returns expected JSON structure."""
        response = client.get("/health-check")
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "hostname" in data
        
        assert data["message"] == "OK"
        assert data["version"] == "0.0.1"
        assert isinstance(data["hostname"], str)
        assert len(data["hostname"]) > 0


class TestTTSEndpoint:
    """Tests for the text-to-speech endpoint."""

    VALID_API_KEY = "12345678"
    TEST_VOICE = "EXAVITQu4vr4xnSDxMaL"
    TEST_TEXT = "Hello world"

    def test_tts_requires_api_key(self, client, mock_elevenlabs):
        """Test that TTS endpoint requires API key."""
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={"text": self.TEST_TEXT}
        )
        assert response.status_code == 401
        assert "Invalid API Key" in response.json()["detail"]

    def test_tts_rejects_invalid_api_key(self, client, mock_elevenlabs):
        """Test that TTS endpoint rejects invalid API key."""
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={"text": self.TEST_TEXT},
            headers={"unith-voice-x-api": "wrong-key"}
        )
        assert response.status_code == 401
        assert "Invalid API Key" in response.json()["detail"]

    def test_tts_requires_text_field(self, client, mock_elevenlabs):
        """Test that TTS endpoint requires text field."""
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={},
            headers={"unith-voice-x-api": self.VALID_API_KEY}
        )
        assert response.status_code == 422  # Validation error

    def test_tts_success_with_valid_request(self, client, mock_elevenlabs):
        """Test successful TTS request."""
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={"text": self.TEST_TEXT},
            headers={"unith-voice-x-api": self.VALID_API_KEY}
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"
        assert "attachment" in response.headers["content-disposition"]
        assert "speech.wav" in response.headers["content-disposition"]
        assert len(response.content) > 0

    def test_tts_handles_different_voices(self, client, mock_elevenlabs):
        """Test TTS with different voice IDs."""
        different_voice = "another-voice-id"
        response = client.post(
            f"/tts/{different_voice}",
            json={"text": self.TEST_TEXT},
            headers={"unith-voice-x-api": self.VALID_API_KEY}
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

    def test_tts_handles_longer_text(self, client, mock_elevenlabs):
        """Test TTS with longer text input."""
        long_text = "This is a much longer text that should still be processed correctly by the TTS system."
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={"text": long_text},
            headers={"unith-voice-x-api": self.VALID_API_KEY}
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

    def test_tts_handles_special_characters(self, client, mock_elevenlabs):
        """Test TTS with special characters in text."""
        special_text = "Hello! How are you? I'm fine, thanks. 123 #test"
        response = client.post(
            f"/tts/{self.TEST_VOICE}",
            json={"text": special_text},
            headers={"unith-voice-x-api": self.VALID_API_KEY}
        )
        
        assert response.status_code == 200

    def test_tts_handles_provider_request_error(self, client):
        """Test graceful handling of TTS provider request errors."""
        with patch('routers.voice.voice_handler.make_elevenlabs_tts_sample') as mock:
            from httpx import RequestError
            mock.side_effect = RequestError("Connection failed")
            
            response = client.post(
                f"/tts/{self.TEST_VOICE}",
                json={"text": self.TEST_TEXT},
                headers={"unith-voice-x-api": self.VALID_API_KEY}
            )
            
            assert response.status_code == 503
            assert "Service unavailable" in response.json()["detail"]

    def test_tts_handles_unexpected_error(self, client):
        """Test graceful handling of unexpected errors."""
        with patch('routers.voice.voice_handler.make_elevenlabs_tts_sample') as mock:
            mock.side_effect = Exception("Unexpected error")
            
            response = client.post(
                f"/tts/{self.TEST_VOICE}",
                json={"text": self.TEST_TEXT},
                headers={"unith-voice-x-api": self.VALID_API_KEY}
            )
            
            assert response.status_code == 500
            assert "Unexpected error" in response.json()["detail"]


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_docs_endpoint_exists(self, client):
        """Test that /docs endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_exists(self, client):
        """Test that /redoc endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema_exists(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
