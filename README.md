# Voice Connector Template

A set of examples to develop a private voice connector for the Unith platform.

## Project Overview

This repository contains two example implementations of a voice connector for the Unith platform:

1. **Node.js Express Implementation** - Located in the [nodejs/express](./nodejs/express) directory
2. **Python FastAPI Implementation** - Located in the [python/fastapi](./python/fastapi) directory

Both implementations provide the same core functionality:

- Health check endpoint (`GET /health-check`)
- Text-to-speech endpoint with API key authentication (`POST /tts/{voice}`)
- Swagger API documentation
- CORS support
- Logging
- Docker support

## Getting Started

Please refer to the README files in each implementation directory for specific setup and usage instructions:

- [Node.js Express README](./nodejs/express/README.md)
- [Python FastAPI README](./python/fastapi/README.md)
