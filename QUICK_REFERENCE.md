# Voice Agent Quick Reference

## 🚀 Quick Start Commands

### Setup (One-time)
```bash
# Windows
setup_voice_agent.bat

# Linux/Mac
chmod +x setup_voice_agent.sh
./setup_voice_agent.sh
```

### Start All Services (Windows)
```bash
start_all.bat
```

### Start Manually
```bash
# Terminal 1: Django
cd backend
python manage.py runserver

# Terminal 2: Agent
cd backend/voice_agent
python agent.py dev

# Terminal 3: Frontend
cd frontend
npm run dev
```

## 🔑 Required API Keys

| Service | URL | Environment Variable |
|---------|-----|---------------------|
| LiveKit | https://livekit.io | `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` |
| Deepgram | https://deepgram.com | `DEEPGRAM_API_KEY` |
| OpenAI | https://platform.openai.com | `OPENAI_API_KEY` |

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/.env` | API keys and configuration |
| `backend/voice_agent/agent.py` | Main voice agent logic |
| `backend/voice_agent/prompts.py` | Tutor personality and behavior |
| `frontend/src/components/VoiceAssistant/` | Voice UI components |

## 🎛️ Configuration Options

### Change Tutor Topic
Edit `backend/.env`:
```env
TUTOR_TOPIC=your topic here
TUTOR_SUBJECT=your subject here
TUTOR_STYLE=friendly and encouraging
```

### Change AI Model
Edit `backend/.env`:
```env
LLM_CHOICE=gpt-4-turbo        # or gpt-3.5-turbo
```

### Change Voice
Edit `backend/voice_agent/agent.py`:
```python
tts=openai.TTS(voice="echo")  # or alloy, fable, onyx, nova, shimmer
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/voice/get-token/?name=NAME` | GET | Get LiveKit token |
| `/api/voice/config/` | GET | Get agent config |

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Failed to connect" | Check Django is running on port 8000 |
| "Agent not responding" | Verify LiveKit agent is running |
| "No audio" | Grant microphone permission in browser |
| "Module not found" | Run `pip install -r requirements.txt` |
| "npm errors" | Run `npm install` in frontend directory |
| "Invalid token" | Check API keys in `.env` file |

## 📊 Service Status Check

### Django
```bash
# Should see: Starting development server at http://127.0.0.1:8000/
curl http://localhost:8000/api/voice/config/
```

### LiveKit Agent
```bash
# Should see: Agent connected to LiveKit
# Look for: "Worker registered"
```

### Frontend
```bash
# Should see: Local: http://localhost:5173/
# Open browser and check for Voice button
```

## 🎯 User Flow

1. Click Voice Assistant button 🎤
2. Enter your name
3. Click "Start Session"
4. Grant microphone permission
5. Wait for tutor greeting
6. Start speaking
7. View real-time transcription
8. Receive tutor responses
9. Close modal to end session

## 🛠️ Development Tools

### View Logs
```bash
# Django logs
python manage.py runserver --verbosity 2

# Agent logs
python agent.py dev --log-level debug

# Frontend logs
npm run dev (check browser console)
```

### Reset Database
```bash
cd backend
rm db.sqlite3 tutor_db.sqlite
python manage.py migrate
```

### Clear Node Modules
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📱 Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome/Edge | ✅ Full support | Recommended |
| Firefox | ✅ Full support | Works well |
| Safari | ⚠️ Partial | May need tweaks |
| Mobile | ⚠️ Limited | Desktop recommended |

## 💡 Tips & Best Practices

1. **Test microphone** - Use browser's mic test before starting
2. **Stable internet** - Required for real-time communication
3. **Quiet environment** - Better speech recognition
4. **Clear speech** - Speak clearly for best results
5. **Give time to respond** - Agent needs time to process
6. **Watch transcriptions** - See what agent understood
7. **Close unused sessions** - Free up resources

## 🔄 Update Procedure

### Pull Changes
```bash
git pull origin main
```

### Update Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
```

### Update Frontend
```bash
cd frontend
npm install
```

## 📞 Support Resources

- **Full Documentation**: `VOICE_AGENT_README.md`
- **Setup Guide**: `SETUP_CHECKLIST.md`
- **Architecture**: `ARCHITECTURE.md`
- **Integration Summary**: `INTEGRATION_SUMMARY.md`

## 🎨 Customization Quick Links

### Change Colors
`frontend/src/components/VoiceAssistant/*.tsx`
- Look for styled-components
- Modify color values

### Change Behavior
`backend/voice_agent/prompts.py`
- Modify `INSTRUCTIONS` template
- Adjust conversation style

### Add Function Tools
`backend/voice_agent/api.py`
- Add new `@function_tool()` methods
- Define tool behavior

## 🔐 Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong API keys
- [ ] Enable HTTPS in production
- [ ] Set up proper CORS
- [ ] Implement rate limiting
- [ ] Monitor API usage
- [ ] Rotate keys regularly

## 📏 Resource Limits

| Resource | Development | Production |
|----------|-------------|------------|
| Concurrent Sessions | 1-5 | 10-100+ |
| Database | SQLite | PostgreSQL |
| API Rate Limits | Set by providers | Monitor closely |
| Storage | Local disk | Cloud storage |

## 🎓 Learning Resources

- **LiveKit**: https://docs.livekit.io
- **Deepgram**: https://developers.deepgram.com
- **OpenAI**: https://platform.openai.com/docs
- **Django**: https://docs.djangoproject.com
- **React**: https://react.dev

---

**Keep this file handy for quick reference!** 📖

For detailed information, refer to the comprehensive documentation files.
