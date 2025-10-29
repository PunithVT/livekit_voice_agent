# Voice Agent Setup Checklist

Use this checklist to ensure everything is properly configured.

## ☑️ Pre-Setup

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ and npm installed
- [ ] Git installed (optional)

## ☑️ API Keys & Accounts

- [ ] LiveKit account created at https://livekit.io
  - [ ] Got LIVEKIT_URL (wss://...)
  - [ ] Got LIVEKIT_API_KEY
  - [ ] Got LIVEKIT_API_SECRET

- [ ] Deepgram account created at https://deepgram.com
  - [ ] Got DEEPGRAM_API_KEY

- [ ] OpenAI account with API access
  - [ ] Got OPENAI_API_KEY
  - [ ] Billing configured (required for API usage)

## ☑️ Backend Configuration

- [ ] Created `backend/.env` file
- [ ] Added all required environment variables to `.env`
- [ ] Installed Python dependencies: `pip install -r requirements.txt`
- [ ] Ran migrations: `python manage.py migrate`
- [ ] Verified `voice_agent` app is in INSTALLED_APPS
- [ ] Verified URL routing is configured in `Main/urls.py`

## ☑️ Frontend Configuration

- [ ] Installed npm dependencies: `npm install`
- [ ] Verified LiveKit packages in `package.json`:
  - [ ] @livekit/components-react
  - [ ] @livekit/components-styles
  - [ ] livekit-client

## ☑️ Testing Services

### Test Django Server
- [ ] Started Django: `python manage.py runserver`
- [ ] Django running on http://localhost:8000
- [ ] Visited http://localhost:8000/api/voice/config/
- [ ] Got JSON response with tutor configuration

### Test LiveKit Agent
- [ ] Started agent: `cd backend/voice_agent && python agent.py dev`
- [ ] No errors in console
- [ ] Agent connected to LiveKit

### Test Frontend
- [ ] Started frontend: `npm run dev`
- [ ] Frontend running on http://localhost:5173
- [ ] Application loads without errors
- [ ] Voice Assistant button visible

## ☑️ End-to-End Testing

- [ ] Clicked Voice Assistant button
- [ ] Modal opened
- [ ] Entered name in form
- [ ] Clicked "Start Session"
- [ ] Connected to LiveKit room
- [ ] Granted microphone permission
- [ ] Heard tutor greeting
- [ ] Spoke and saw transcription
- [ ] Tutor responded appropriately
- [ ] Able to end session

## ☑️ Browser Compatibility

Test in these browsers:
- [ ] Google Chrome/Chromium
- [ ] Microsoft Edge
- [ ] Firefox
- [ ] Safari (Mac only)

## 🔍 Troubleshooting Checks

If something doesn't work, verify:

### Backend Issues
- [ ] `.env` file exists in `backend/` directory
- [ ] All API keys are correct (no extra spaces)
- [ ] Django server shows no errors
- [ ] CORS is enabled (already configured)
- [ ] Port 8000 is not blocked by firewall

### Agent Issues
- [ ] LiveKit credentials are valid
- [ ] OpenAI API key is valid and has credits
- [ ] Deepgram API key is valid
- [ ] Agent terminal shows no errors
- [ ] Agent successfully connected to LiveKit

### Frontend Issues
- [ ] `npm install` completed without errors
- [ ] No console errors in browser DevTools
- [ ] API URL is correct (http://localhost:8000)
- [ ] Microphone permission granted
- [ ] Audio input device is working

### Connection Issues
- [ ] All three services are running:
  1. Django (port 8000)
  2. LiveKit Agent
  3. Frontend (port 5173)
- [ ] No firewall blocking connections
- [ ] Internet connection is stable

## 📝 Configuration Customization

Optional customizations to try:

- [ ] Changed TUTOR_TOPIC in `.env`
- [ ] Changed TUTOR_SUBJECT in `.env`
- [ ] Changed TUTOR_STYLE in `.env`
- [ ] Modified prompts in `prompts.py`
- [ ] Tested with different OpenAI model (LLM_CHOICE)
- [ ] Customized component styling

## 🎯 Production Checklist

Before deploying to production:

- [ ] Changed DEBUG=False in Django settings
- [ ] Configured ALLOWED_HOSTS properly
- [ ] Set up proper CORS origins (not CORS_ALLOW_ALL_ORIGINS)
- [ ] Used environment variables for all secrets
- [ ] Set up SSL/TLS certificates
- [ ] Configured proper logging
- [ ] Set up monitoring and error tracking
- [ ] Tested with production LiveKit domain
- [ ] Load tested the voice agent
- [ ] Implemented rate limiting
- [ ] Set up backup for conversation database

## 📊 Success Metrics

You know it's working when:

- ✅ Voice button appears and is clickable
- ✅ Modal opens smoothly
- ✅ Can enter name and start session
- ✅ Microphone permission is granted
- ✅ Audio visualizer shows activity
- ✅ Tutor greets you by name
- ✅ Your speech is transcribed in real-time
- ✅ Tutor responds appropriately to questions
- ✅ Can have a natural conversation
- ✅ No lag or connection issues
- ✅ Can end session cleanly

## 🆘 Getting Help

If you're stuck:

1. Check `VOICE_AGENT_README.md` for detailed documentation
2. Check `INTEGRATION_SUMMARY.md` for overview
3. Review console logs in:
   - Django terminal
   - LiveKit agent terminal
   - Browser DevTools
4. Verify all checklist items above
5. Check API key validity and billing status
6. Try restarting all services

## 🎉 All Done!

If all items are checked, your voice agent is fully configured and ready to use!

---

**Last Updated:** 2025-10-29
**Integration Version:** 1.0
