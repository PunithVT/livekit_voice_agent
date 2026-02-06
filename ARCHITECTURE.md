# 🏗️ Architecture Documentation

## System Overview

The LiveKit Voice Agent is a modern, production-ready voice tutoring platform built with a microservices architecture. The system combines real-time communication, AI-powered conversation, and comprehensive data persistence.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Browser    │  │    Mobile    │  │   Desktop    │         │
│  │  (React App) │  │   (Future)   │  │   (Future)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │    Load Balancer    │
                    │   (Nginx/ALB)      │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┼────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌───────▼─────────┐   ┌─────▼───────┐
│   Frontend     │   │    Backend      │   │  LiveKit    │
│ React + Vite   │   │    FastAPI      │   │   Server    │
│   (Nginx)      │   │  (Uvicorn)      │   │   (WebRTC)  │
└────────────────┘   └──────┬──────────┘   └─────┬───────┘
                             │                     │
                    ┌────────┼─────────────────────┤
                    │        │                     │
            ┌───────▼────┐ ┌▼──────────┐  ┌──────▼──────┐
            │ PostgreSQL │ │   Redis   │  │   OpenAI    │
            │  Database  │ │   Cache   │  │ Realtime API│
            └────────────┘ └───────────┘  └─────────────┘
                    │
            ┌───────┴──────────┐
            │                  │
    ┌───────▼────────┐  ┌─────▼────────┐
    │   Prometheus   │  │   Grafana    │
    │    (Metrics)   │  │ (Dashboards) │
    └────────────────┘  └──────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology:** React 18 + Vite 6 + LiveKit Components

**Responsibilities:**
- User interface rendering
- WebRTC connection management
- Audio visualization
- Real-time transcription display
- Token acquisition from backend

**Key Files:**
- `frontend/src/App.jsx` - Main application component
- `frontend/src/components/LiveKitModal.jsx` - Session management
- `frontend/src/components/SimpleVoiceAssistant.jsx` - Voice UI

**Architecture Pattern:** Component-based architecture with hooks

### 2. Backend Layer

**Technology:** FastAPI + Uvicorn + Python 3.11

**Responsibilities:**
- JWT token generation for LiveKit access
- Room management (create, list, delete)
- Database operations (CRUD)
- API rate limiting
- Health monitoring
- Metrics collection

**Key Files:**
- `backend/server.py` - FastAPI application and API endpoints
- `backend/agent.py` - LiveKit agent entry point
- `backend/api.py` - TutorAgent with teaching tools
- `backend/db_driver_enhanced.py` - Database abstraction layer

**Architecture Pattern:** Layered architecture with async/await

```
┌─────────────────────────────────┐
│      API Layer (FastAPI)        │
│  - Routing                      │
│  - Validation (Pydantic)        │
│  - Rate Limiting                │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     Business Logic Layer        │
│  - Token Generation             │
│  - Room Management              │
│  - User Management              │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      Data Access Layer          │
│  - Database Driver              │
│  - Model Classes                │
└─────────────────────────────────┘
```

### 3. LiveKit Agent

**Technology:** LiveKit Agents Framework + OpenAI Realtime API

**Responsibilities:**
- Handle real-time voice streams
- AI conversation management
- Teaching tool execution
- Conversation state tracking
- Subtopic management

**Key Components:**
- `TutorAgent` class - Main agent logic
- Function tools - check_understanding, provide_example, etc.
- Event handlers - User speech processing

**Flow:**
```
User Speech → LiveKit → Agent → OpenAI Realtime API → Response → LiveKit → User
```

### 4. Database Layer

**Primary:** PostgreSQL 16 (Production)
**Fallback:** SQLite (Development)

**Schema:**

```sql
-- Core Tables
subtopics           # Educational content
conversations       # Session tracking
messages            # Conversation history
user_profiles       # User data & preferences
session_analytics   # Performance metrics

-- Indexes for Performance
idx_subtopics_topic
idx_conversations_room
idx_messages_conversation
idx_messages_timestamp
```

**Data Model:**
```
Conversation (1) ─── (N) Message
     │
     └───── (1) UserProfile

Subtopic ─── (N) Conversation (via topic)
```

### 5. Caching Layer

**Technology:** Redis 7

**Use Cases:**
- Session data caching
- Rate limiting counters
- LiveKit room state
- Temporary data storage

**Cache Strategy:**
- TTL-based expiration
- Write-through for critical data
- Cache-aside for read-heavy operations

### 6. Monitoring & Observability

**Components:**
1. **Prometheus** - Metrics collection
   - Custom metrics from FastAPI
   - System metrics
   - LiveKit metrics

2. **Grafana** - Visualization
   - Pre-built dashboards
   - Alerting rules
   - Query interface

**Metrics Collected:**
- Request rates and latencies
- Error rates by endpoint
- Token generation success/failure
- Room creation statistics
- Database query performance

## Data Flow

### 1. User Join Flow

```
1. User opens app → Frontend loads
2. User enters name → Form submission
3. Frontend requests token → GET /api/getToken
4. Backend generates JWT → With room grants
5. Frontend receives token → Initializes LiveKit
6. LiveKit establishes connection → WebRTC handshake
7. Agent joins room → Welcomes user
8. Conversation begins → Real-time audio
```

### 2. Message Flow

```
1. User speaks → Audio captured by browser
2. LiveKit encodes → Sent to server
3. Agent receives audio → Transcribed by OpenAI
4. Text analyzed → Determine response
5. OpenAI generates → Speech + text
6. Agent sends response → Via LiveKit
7. Browser plays audio → User hears response
8. Message saved → Database for history
```

### 3. Monitoring Flow

```
1. API request received → FastAPI endpoint
2. Metrics updated → Prometheus counters/histograms
3. Metrics exposed → /api/metrics endpoint
4. Prometheus scrapes → Every 15 seconds
5. Grafana queries → Prometheus data
6. Dashboards updated → Real-time visualization
7. Alerts triggered → If thresholds exceeded
```

## Security Architecture

### 1. Authentication & Authorization

**JWT Token Flow:**
```
Client → Backend (/api/token) → Validate input
                               → Generate JWT with:
                                   - Identity
                                   - Room name
                                   - Expiration (2 hours)
                                   - Permissions
Backend → Client (Token)
Client → LiveKit (Token) → Validate signature
                          → Grant access
```

**Security Features:**
- Rate limiting (10 requests/minute per IP)
- Input validation (Pydantic models)
- CORS restrictions (configurable origins)
- Token expiration
- No sensitive data in JWT

### 2. Network Security

**HTTPS/WSS:**
- All production traffic encrypted
- TLS 1.2+ required
- Certificate validation

**Headers:**
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block

### 3. Data Security

**At Rest:**
- PostgreSQL encryption available
- Redis password protection
- Volume encryption (Docker/Kubernetes)

**In Transit:**
- WebRTC DTLS encryption
- HTTPS for API calls
- Secure WebSocket (WSS)

## Scalability Considerations

### Horizontal Scaling

**Backend:**
- Stateless design enables multiple instances
- Load balancer distributes requests
- Database connection pooling
- Redis for shared state

**Frontend:**
- Static files served by CDN
- Multiple Nginx instances
- Gzip compression
- Cache headers

### Vertical Scaling

**Database:**
- PostgreSQL read replicas
- Connection pooling (50-100 connections)
- Query optimization with indexes
- Partitioning for large tables

**Redis:**
- Persistence enabled (AOF)
- Memory limits configured
- Eviction policies (LRU)

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| API Latency (p95) | < 200ms | ~100ms |
| Token Generation | < 50ms | ~30ms |
| Database Query | < 10ms | ~5ms |
| WebRTC Connection | < 3s | ~2s |
| Concurrent Users | 1000+ | Tested to 100 |

## Deployment Architecture

### Development
```
Local Machine:
  - Docker Compose (all services)
  - Hot reload enabled
  - Debug logging
  - SQLite database
```

### Staging
```
Cloud Infrastructure:
  - Kubernetes cluster
  - PostgreSQL managed service
  - Redis managed service
  - LiveKit cloud
  - Lower resource limits
```

### Production
```
Cloud Infrastructure:
  - Multi-zone Kubernetes
  - PostgreSQL with replicas
  - Redis cluster mode
  - LiveKit cloud (enterprise)
  - Auto-scaling enabled
  - CDN for static assets
  - Full monitoring stack
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 | UI framework |
| | Vite 6 | Build tool |
| | LiveKit Components | Real-time UI |
| **Backend** | FastAPI | API framework |
| | Uvicorn | ASGI server |
| | Python 3.11 | Language |
| **Agent** | LiveKit Agents | Voice handling |
| | OpenAI Realtime | AI conversation |
| **Database** | PostgreSQL 16 | Primary database |
| | SQLite | Development |
| **Cache** | Redis 7 | Session & cache |
| **Monitoring** | Prometheus | Metrics |
| | Grafana | Dashboards |
| **Deployment** | Docker | Containerization |
| | Docker Compose | Local orchestration |
| | Kubernetes | Production orchestration |

## Design Principles

1. **Separation of Concerns** - Clear layer boundaries
2. **Async-First** - Non-blocking operations throughout
3. **Fail Fast** - Validate inputs early
4. **Observable** - Comprehensive logging and metrics
5. **Scalable** - Horizontal scaling by design
6. **Secure** - Security in every layer
7. **Testable** - High test coverage
8. **Documented** - Code and API documentation

## Future Architecture Enhancements

1. **Event-Driven Architecture** - Message queue (RabbitMQ/Kafka)
2. **Microservices** - Split monolith into services
3. **Service Mesh** - Istio for service-to-service communication
4. **GraphQL API** - Alternative to REST
5. **WebSocket Server** - Real-time updates beyond LiveKit
6. **Machine Learning Pipeline** - Conversation analysis
7. **Multi-Region Deployment** - Global availability
8. **Edge Computing** - CDN for dynamic content

---

For implementation details, see [CHANGES.md](CHANGES.md)
For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)
