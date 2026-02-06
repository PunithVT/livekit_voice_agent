# 🎓 LiveKit AI Voice Agent - Advanced Tutoring Platform

[![CI/CD Pipeline](https://github.com/yourusername/livekit_voice_agent/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/livekit_voice_agent/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A cutting-edge, production-ready voice tutoring platform powered by LiveKit and OpenAI's Realtime API. Features real-time voice interaction, intelligent conversation management, and comprehensive monitoring.

## ✨ Features

### Core Capabilities
- 🎤 **Real-time Voice Interaction** - Ultra-low latency voice communication using LiveKit
- 🤖 **AI-Powered Tutoring** - OpenAI Realtime API with GPT-4 for natural conversations
- 📊 **Advanced Analytics** - Prometheus metrics and Grafana dashboards
- 🔒 **Enterprise Security** - Rate limiting, JWT authentication, and input validation
- 🐳 **Container-Ready** - Full Docker Compose setup with all services
- 🧪 **Comprehensive Testing** - 95%+ test coverage with pytest
- 📚 **Interactive API Docs** - Automatic OpenAPI/Swagger documentation
- 🌍 **Production-Ready** - Health checks, logging, monitoring, and error handling

### Advanced Features
- **Adaptive Pace Control** - Automatically adjusts teaching speed based on student responses
- **Comprehension Checking** - Regular understanding verification
- **Dynamic Examples** - Context-aware example generation
- **Conversation History** - Full session recording and replay
- **Multi-Topic Support** - Organized knowledge base with subtopic management
- **Audio Visualization** - Real-time waveform display
- **Room Management** - Create, join, and manage tutoring sessions

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend    │────▶│  LiveKit    │
│ React + Vite│     │   FastAPI    │     │   Server    │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │                     │
       │                    ▼                     │
       │            ┌──────────────┐             │
       │            │  PostgreSQL  │             │
       │            │   Database   │             │
       │            └──────────────┘             │
       │                    │                     │
       │                    ▼                     │
       │            ┌──────────────┐             │
       └───────────▶│    Redis     │◀────────────┘
                    │    Cache     │
                    └──────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  Monitoring  │
                   │ (Prometheus/ │
                   │   Grafana)   │
                   └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended)
- OR:
  - Python 3.11+
  - Node.js 20+
  - PostgreSQL 16+
  - Redis 7+
  - LiveKit Server

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/livekit_voice_agent.git
   cd livekit_voice_agent
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:5001
   - API Docs: http://localhost:5001/api/docs
   - Grafana: http://localhost:3001
   - Prometheus: http://localhost:9090

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (if using PostgreSQL)
# alembic upgrade head

# Start the server
python server.py
# or with uvicorn:
uvicorn server:app --reload --port 5001
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

## 📝 Configuration

### Required Environment Variables

**Backend (.env)**
```bash
# LiveKit
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=ws://localhost:7880

# OpenAI
OPENAI_API_KEY=sk-your_openai_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Redis
REDIS_URL=redis://:password@localhost:6379/0
```

**Frontend (.env)**
```bash
VITE_LIVEKIT_URL=ws://localhost:7880
VITE_API_URL=http://localhost:5001
```

See [.env.example](.env.example) for complete configuration options.

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api          # API tests only
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📚 API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:5001/api/docs
- **ReDoc**: http://localhost:5001/api/redoc
- **OpenAPI JSON**: http://localhost:5001/api/openapi.json

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/getToken` | Generate JWT token (legacy) |
| POST | `/api/token` | Generate JWT token |
| GET | `/api/rooms` | List active rooms |
| DELETE | `/api/rooms/{name}` | Delete a room |
| GET | `/api/metrics` | Prometheus metrics |

## 🔧 Development

### Project Structure
```
livekit_voice_agent/
├── backend/
│   ├── server.py           # FastAPI application
│   ├── agent.py            # LiveKit agent entrypoint
│   ├── api.py              # TutorAgent class
│   ├── db_driver.py        # Database driver
│   ├── prompts.py          # AI prompts
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container
│   └── tests/              # Test suite
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component
│   │   ├── components/     # React components
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── monitoring/
│   ├── prometheus.yml      # Prometheus config
│   └── grafana/            # Grafana dashboards
├── docker-compose.yml      # Full stack orchestration
└── .github/
    └── workflows/          # CI/CD pipelines
```

### Code Quality

**Backend**
```bash
# Format code
black backend/

# Lint
ruff check backend/

# Type check
mypy backend/
```

**Frontend**
```bash
# Lint
npm run lint

# Format
npm run format
```

## 📊 Monitoring

### Prometheus Metrics
Access metrics at: http://localhost:9090

Available metrics:
- `token_requests_total` - Total token generation requests
- `token_errors_total` - Token generation errors
- `room_creations_total` - Total rooms created
- `api_request_duration_seconds` - API latency histogram

### Grafana Dashboards
Access dashboards at: http://localhost:3001 (admin/admin)

Pre-configured dashboards:
- API Performance
- System Resources
- LiveKit Metrics
- Error Rates

## 🚢 Deployment

### Docker Compose (Production)
```bash
# Build and start
docker-compose -f docker-compose.yml up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) - Real-time communication infrastructure
- [OpenAI](https://openai.com/) - Realtime API and GPT models
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend library

## 📧 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/livekit_voice_agent/issues)

## 🗺️ Roadmap

- [ ] Multi-language support (i18n)
- [ ] Screen sharing functionality
- [ ] File upload and analysis
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Offline mode support
- [ ] Integration with LMS platforms

---

**Made with ❤️ by the LiveKit Voice Agent Team**
