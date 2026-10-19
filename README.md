# Polsia AI

Production-ready FastAPI SaaS backend for Polsia AI.

## Security changes
- `.env` removed from source control; use environment variables or `.env.example`
- `JWT_SECRET`, `DEFAULT_ADMIN_PASSWORD`, and `BILLING_WEBHOOK_SECRET` are mandatory
- Startup no longer auto-creates privileged admin users
- Auth now enforces MFA when enabled and applies account/IP lockouts
- Data is persisted via SQL-backed repositories
- Rate limiting respects trusted proxies and tenant/user separation
- Billing callbacks validate signature, idempotency, and invoice values

## Run
```bash
pip install -r requirements.txt
export JWT_SECRET="your-secret"
export DEFAULT_ADMIN_PASSWORD="one-time-password"
export BILLING_WEBHOOK_SECRET="webhook-secret"
uvicorn app.main:app --reload
```

## One-time admin setup
Create the initial admin explicitly instead of on application startup:
```python
import asyncio
from app.services.bootstrap import create_initial_admin

asyncio.run(create_initial_admin())
```
