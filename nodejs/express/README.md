# Express Template Connector

This is a Node.js Express implementation of the Voice Connector Template, mirroring the functionality of the Python FastAPI version.

## Features

- Health check endpoint
- Text-to-speech endpoint with API key authentication
- Swagger API documentation
- CORS support
- Docker support

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Docker (optional, for containerization)

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
yarn install
```

### Running the Application

#### Development Mode

```bash
yarn run dev
```

This will start the server with nodemon, which automatically restarts the server when changes are detected.

#### Production Mode

```bash
yarn start
```

### Docker

#### Building the Docker Image

```bash
make build
```

or

```bash
docker build . --target builder -t express-connector:0.0.1
```

#### Running the Docker Container

```bash
make run
```

or

```bash
docker run -e unithApiKey=12345678 -it -p 8080:8080 --rm express-connector:0.0.1
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
http://localhost:8080/api-docs
```

This provides an interactive interface to explore the API endpoints, send test requests, and view response formats.

Alternative URLs:
- http://localhost:8080/docs (redirects to /api-docs)
- http://localhost:8080/redoc (redirects to /api-docs)

## License

ISC
