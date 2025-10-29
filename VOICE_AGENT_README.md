# Voice Agent Integration Guide

This document explains how to set up and use the Voice Agent feature in the Autonomous Learning Sample project.

## Overview

The Voice Agent provides real-time voice tutoring capabilities using:
- **LiveKit** for real-time audio communication
- **Deepgram** for speech-to-text transcription
- **OpenAI** for natural language processing and text-to-speech
- **Django** backend for API endpoints
- **React + TypeScript** frontend with LiveKit components

## Prerequisites

1. **LiveKit Cloud Account**
   - Sign up at https://livekit.io
   - Create a new project
   - Get your API Key, API Secret, and WebSocket URL

2. **Deepgram Account**
   - Sign up at https://deepgram.com
   - Get your API key

3. **OpenAI Account**
   - Get your API key from https://platform.openai.com

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Add these variables to your `.env` file in the `backend` directory:

```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret

# Tutor Configuration
TUTOR_TOPIC=artificial intelligence
TUTOR_SUBJECT=machine learning basics
TUTOR_STYLE=friendly and encouraging

# OpenAI Configuration
LLM_CHOICE=gpt-4-turbo
OPENAI_API_KEY=your-openai-api-key

# Deepgram Configuration (for speech-to-text)
DEEPGRAM_API_KEY=your-deepgram-api-key
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start the Django Server

```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 5. Start the LiveKit Agent

In a separate terminal, run the voice agent:

```bash
cd backend/voice_agent
python agent.py dev
```

This will start the LiveKit agent that handles the voice interactions.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables (Optional)

Create a `.env` file in the `frontend` directory if you need to override defaults:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start the Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Start a Voice Session**
   - Click on the Voice Assistant button (microphone icon) in the application
   - Enter your name when prompted
   - Click "Start Session"

2. **Interact with the Tutor**
   - The tutor will greet you and introduce the topic
   - Speak naturally - the agent will listen and respond
   - Ask questions about the topic
   - Request examples or clarification

3. **Control the Session**
   - Use the control bar to mute/unmute your microphone
   - View real-time transcriptions of both your speech and the tutor's responses
   - Close the modal to end the session

## API Endpoints

### Get Token
```
GET /api/voice/get-token/?name=<username>
```

Returns a LiveKit access token for joining a voice session.

**Response:**
```json
{
  "token": "eyJhbGc...",
  "room": "room-abc123",
  "url": "wss://your-project.livekit.cloud"
}
```

### Get Configuration
```
GET /api/voice/config/
```

Returns the current voice agent configuration.

**Response:**
```json
{
  "livekit_url": "wss://your-project.livekit.cloud",
  "topic": "artificial intelligence",
  "subject": "machine learning basics",
  "style": "friendly and encouraging"
}
```

## Customization

### Changing the Tutor's Topic

Edit the environment variables in your `.env` file:

```env
TUTOR_TOPIC=quantum computing
TUTOR_SUBJECT=superposition and entanglement
TUTOR_STYLE=professional and detailed
```

### Modifying the Agent's Behavior

Edit `backend/voice_agent/prompts.py` to customize:
- Instruction templates
- Welcome messages
- Conversation flow

### Adjusting Voice Settings

In `backend/voice_agent/agent.py`, you can modify:
- **STT Model**: Change `model="nova-2"` in the Deepgram configuration
- **LLM Model**: Change `model=os.getenv("LLM_CHOICE", "gpt-4-turbo")`
- **TTS Voice**: Change `voice="echo"` in the OpenAI TTS configuration

## Troubleshooting

### "Failed to connect to voice service"

1. Check that the Django server is running on port 8000
2. Verify your LiveKit credentials in the `.env` file
3. Ensure CORS is properly configured (already set to allow all origins in development)

### "Agent not responding"

1. Make sure the LiveKit agent is running (`python agent.py dev`)
2. Check that your OpenAI and Deepgram API keys are valid
3. Look for errors in the agent terminal

### Audio not working

1. Grant microphone permissions in your browser
2. Check that your audio input device is working
3. Try refreshing the page and starting a new session

### "Module not found" errors

1. Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt  # Backend
   npm install                       # Frontend
   ```

## Architecture

### Backend Components

- **voice_agent/agent.py**: Main LiveKit agent with tutoring logic
- **voice_agent/views.py**: Django views for token generation and config
- **voice_agent/db_driver.py**: SQLite driver for storing conversation data
- **voice_agent/prompts.py**: Prompt templates for the agent

### Frontend Components

- **VoiceAssistant/index.tsx**: Main component with trigger button
- **VoiceAssistant/VoiceAssistantModal.tsx**: Modal for voice sessions
- **VoiceAssistant/LiveKitVoiceAssistant.tsx**: LiveKit room interface

## Security Notes

- The current setup allows all CORS origins for development
- In production, configure `CORS_ALLOWED_ORIGINS` in Django settings
- Store API keys securely using environment variables
- Consider implementing user authentication for voice sessions

## Further Resources

- [LiveKit Documentation](https://docs.livekit.io)
- [Deepgram Documentation](https://developers.deepgram.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org)
