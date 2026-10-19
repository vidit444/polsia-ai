# Polsia AI

Production-ready FastAPI backend for a multi-tenant AI operations platform.

## Features
- Multi-tenant API architecture
- JWT authentication with RBAC
- Workflow orchestration APIs
- KPI analytics APIs
- Webhook ingestion with signature validation
- Structured logging, rate limiting, idempotency, and audit trails
- Health, readiness, and liveness endpoints

## Quick Start
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables from `.env.example`.
4. Run locally:
   ```bash
   uvicorn app.main:app --reload
   ```

## Required Environment Variables
Secrets are required and are never hardcoded. You must provide:
- `JWT_SECRET`
- `ADMIN_PASSWORD`
- `DATABASE_URL`
- `WEBHOOK_SIGNING_SECRET`

Optional non-secret settings are documented in `.env.example`.

## Operational Cadence
- Debugging/monitoring cadence: every 15 minutes in production
- Daily incident review
- Weekly schema and performance tuning
