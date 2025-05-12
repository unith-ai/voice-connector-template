# FastAPI Template Connector

This is a Python FastAPI implementation of the Voice Connector Template.

## Features

- Health check endpoint
- Text-to-speech endpoint with API key authentication
- Swagger API documentation
- CORS support
- Logging
- Docker support

## Getting Started

### Prerequisites

- Python 3.11.5
- Poetry (for dependency management)
- Docker (optional, for containerization)

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
poetry install
```

### Running the Application

#### Development Mode

```bash
poetry run python main.py
```

This will start the server with Uvicorn, which handles the FastAPI application.

### Docker

#### Building the Docker Image

```bash
make build
```

or

```bash
docker build . --target builder -t fast-api-connector:0.0.1
```

#### Running the Docker Container

```bash
make docker-run
```

or

```bash
docker run -e unithApiKey=12345678 -it -p 8080:8080 --rm fast-api-connector:0.0.1
```

## API Endpoints

### Health Check

```
GET /health-check
```

Returns a JSON response with status information.

### Text-to-Speech

```
POST /tts/{voice}
```

Converts text to speech using the specified voice.

#### Request Headers

- `unith-voice-x-api`: API key for authentication (required)

#### Request Body

```json
{
  "text": "Text to convert to speech"
}
```

#### Response

Binary audio data (WAV format) with appropriate headers for download.

## API Documentation

The API documentation is available through Swagger UI. You can access it at:

```
http://localhost:8080/docs
```

This provides an interactive interface to explore the API endpoints, send test requests, and view response formats.

Alternative URL:
- http://localhost:8080/redoc (ReDoc alternative UI)

## License

ISC
