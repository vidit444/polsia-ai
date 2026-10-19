# Polsia AI

Production-ready multi-tenant FastAPI backend for SaaS operations, billing, workflows, CRM, analytics, audit logging, and operational health monitoring.

## Features
- FastAPI with versioned API routing
- Multi-tenant data model with tenant-aware services
- JWT authentication with environment-only secrets
- SQLAlchemy async-ready ORM models
- Pydantic settings with strict secret validation
- Billing invoice creation and payment capture endpoint
- Workflow execution with audit/event emission
- Dashboard metrics aggregation
- Health and smoke-check endpoints for scheduled debugging cadence
- UPI QR support via configurable invoice metadata

## Required environment variables
The application refuses to start if required secrets are missing.

- `APP_ENV`
- `APP_NAME`
- `API_V1_PREFIX`
- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `WEBHOOK_SIGNING_SECRET`
- `OPENAI_API_KEY`
- `REDIS_URL`
- `DEFAULT_UPI_QR_URL`
- `CORS_ORIGINS`

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes
- No secrets are hardcoded.
- Required package marker files are included:
  - `app/__init__.py`
  - `app/api/__init__.py`
  - `app/api/v1/__init__.py`
  - `app/api/v1/routes/__init__.py`
