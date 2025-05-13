# Voice Connector Template

A set of examples to develop a private voice connector for the Unith platform.

## Requirements for creating the voice connector

- a restful api service with a well-defined endpoint following this specification:
    - `POST /tts/{voice}` where voice is a string url param that defines the id of the voice to be used.
    - body: (the text to be converted to speech)
        ```json
        {
          "text": "string"
        }
        ```
    - `GET /health-check` (optional)

- public exposed endpoint (http or https), we prefer https but http is also acceptable.

- a way to authenticate the request, we prefer api key authentication through the header `unith-voice-x-api`.

- a binary response with the audio data.

- to contact unith support to register the endpoint in the platform, you will need to provide the name of the connector and the url
  (https://unith.ai/contact).

## Requirements for the audio output

- PCM format
- 16-bit
- Number of channels: 1

## Time cost processing examples

The request should be processed in less than 10 seconds.

----

TEXT SAMPLE

```
{
  "text": "In a quiet village nestled between rolling hills, there was a small bakery known for its delicious pastries. Every morning, the scent of freshly baked bread and warm croissants wafted through the air, drawing villagers and travelers alike. The baker, an elderly man with a kind smile, took pride in his craft, using recipes passed down through generations. Each pastry was a work of art, filled with love and care. The bakery wasn't just a place to buy bread; it was a cornerstone of the community, a place where stories were shared and memories made."
}
```

WORD COUNT: 95

ACCEPTABLE TIME EXECUTION: 1.50s to 3.00s

----

TEXT SAMPLE

```
{
  "text": "hello, this is a test message to check the api audio."
}
```

WORD COUNT: 11

ACCEPTABLE TIME EXECUTION: 0.50s to 1.00s

## Project Overview

This repository contains two example implementations of a voice connector for the Unith platform:

1. **Node.js Express Implementation** - Located in the [nodejs/express](./nodejs/express) directory
2. **Python FastAPI Implementation** - Located in the [python/fastapi](./python/fastapi) directory

Both implementations provide the same core functionality:

- Health check endpoint (`GET /health-check`)
- Text-to-speech endpoint with API key authentication (`POST /tts/{voice}`)
- Swagger API documentation
- CORS support
- Docker support

## Getting Started

Please refer to the README files in each implementation directory for specific setup and usage instructions:

- [Node.js Express README](./nodejs/express/README.md)
- [Python FastAPI README](./python/fastapi/README.md)


