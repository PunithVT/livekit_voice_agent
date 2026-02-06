# Contributing to LiveKit AI Voice Agent

Thank you for your interest in contributing to the LiveKit AI Voice Agent project! We welcome contributions from the community.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/livekit_voice_agent.git
   cd livekit_voice_agent
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   - Follow the development setup instructions in [README.md](README.md)
   - Install all dependencies
   - Configure your `.env` files

## Development Workflow

### Backend Development

1. **Environment setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run in development mode**
   ```bash
   uvicorn server:app --reload --port 5001
   ```

3. **Run tests**
   ```bash
   pytest
   ```

### Frontend Development

1. **Environment setup**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**
   ```bash
   npm run dev
   ```

3. **Run linter**
   ```bash
   npm run lint
   ```

## Coding Standards

### Python (Backend)

- **Style Guide**: Follow PEP 8
- **Formatter**: Use `black` for code formatting
- **Linter**: Use `ruff` for linting
- **Type Hints**: Use type hints for all function signatures

```bash
# Format code
black backend/

# Lint code
ruff check backend/

# Type check
mypy backend/
```

**Example:**
```python
from typing import Optional

async def create_token(name: str, room: Optional[str] = None) -> TokenResponse:
    """
    Generate an access token for LiveKit.

    Args:
        name: User's display name
        room: Optional room name

    Returns:
        TokenResponse object with token and metadata
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- **Style Guide**: Follow Airbnb JavaScript Style Guide
- **Formatter**: Built into ESLint
- **Linter**: ESLint with React plugins

```bash
# Lint code
npm run lint

# Auto-fix issues
npm run lint -- --fix
```

**Example:**
```javascript
/**
 * Generate a room token for the user
 * @param {string} userName - The user's name
 * @returns {Promise<string>} The access token
 */
const generateToken = async (userName) => {
  const response = await fetch(`/api/getToken?name=${encodeURIComponent(userName)}`);
  return response.text();
};
```

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
feat(backend): add conversation history endpoint

Implement API endpoint to retrieve conversation history
with pagination and filtering options.

Closes #123
```

```bash
fix(frontend): resolve audio visualization rendering issue

Fixed bug where audio visualizer would not render
properly on Safari browsers.
```

## Pull Request Process

1. **Update documentation**
   - Update README.md if needed
   - Add/update docstrings and comments
   - Update API documentation

2. **Add tests**
   - Write unit tests for new features
   - Ensure all tests pass
   - Maintain or improve code coverage

3. **Run quality checks**
   ```bash
   # Backend
   cd backend
   black .
   ruff check .
   pytest

   # Frontend
   cd frontend
   npm run lint
   npm test
   ```

4. **Create Pull Request**
   - Fill out the PR template completely
   - Reference related issues
   - Add screenshots for UI changes
   - Request review from maintainers

5. **Address review feedback**
   - Make requested changes
   - Re-request review when ready
   - Keep discussion professional

### PR Title Format

Follow the same format as commit messages:

```
feat(backend): add conversation history endpoint
```

## Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_server.py

# Run tests by marker
pytest -m unit
pytest -m integration
```

**Writing Tests:**
```python
import pytest

@pytest.mark.unit
class TestTokenGeneration:
    def test_create_token_success(self, client):
        response = client.get("/api/getToken?name=TestUser")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Documentation

### Code Documentation

- **Python**: Use docstrings (Google style)
- **JavaScript**: Use JSDoc comments
- **API**: Document all endpoints in FastAPI with descriptions

### API Documentation

FastAPI automatically generates interactive documentation. Ensure:
- All endpoints have descriptions
- Request/response models are properly typed
- Examples are provided

### README Updates

- Update feature lists
- Add new configuration options
- Include new dependencies
- Update architecture diagrams if needed

## Questions?

- Open an issue for bug reports or feature requests
- Start a discussion for questions or ideas
- Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LiveKit AI Voice Agent!
