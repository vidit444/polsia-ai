# Polsia AI

Production-ready FastAPI SaaS backend for Polsia AI.

## Features
- Multi-tenant API architecture
- JWT authentication
- Lead management
- Workflow execution
- AI chat orchestration
- Billing and UPI payment simulation
- Health, metrics, audit logging, and observability hooks

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `POST /v1/auth/login`
- `POST /v1/leads`
- `POST /v1/workflows/{id}/run`
- `POST /v1/ai/chat`
- `POST /v1/billing/invoices/{id}/pay`
