# Polsia AI

Production-ready FastAPI backend for the Polsia AI multi-tenant SaaS platform.

## Features
- JWT authentication with tenant-aware RBAC
- Tenant onboarding and CRM foundations
- Workflow orchestration with fixed-interval health/debug metadata
- AI chat gateway abstraction with provider configuration from environment
- Dashboard analytics endpoints
- Structured logging, rate limiting, audit logging, and security middleware
- SQLAlchemy async models, repository/service split, and lifespan-managed startup

## Required Environment Variables
Secrets must be supplied via environment variables with no insecure defaults.

- `APP_NAME`
- `APP_ENV`
- `APP_HOST`
- `APP_PORT`
- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_MINUTES`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `AI_DEFAULT_PROVIDER`
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`
- `DEBUG_REVIEW_INTERVAL_SECONDS`
- `WEBHOOK_SIGNING_SECRET`
- `UPI_QR_URL`
- `CORS_ALLOW_ORIGINS`

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
