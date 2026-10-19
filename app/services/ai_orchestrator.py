from typing import Any

SYSTEM_PROMPT = (
    "You are Polsia AI, a tenant-safe enterprise assistant for CRM, workflows, billing, and analytics. "
    "Provide concise, actionable responses with guardrails, avoid unsafe or cross-tenant data disclosure, and suggest next steps."
)


def _route_model(model_preference: str | None) -> str:
    if model_preference in {"openai", "claude", "oss"}:
        return model_preference
    return "router:auto"


async def generate_ai_response(message: str, context: dict[str, Any], model_preference: str | None = None) -> dict[str, Any]:
    routed_model = _route_model(model_preference)
    normalized = message.strip()
    summary_bits = []
    if context:
        summary_bits.append(f"Context keys: {', '.join(sorted(context.keys()))}.")
    if "lead" in normalized.lower():
        guidance = "Recommend qualifying by budget, authority, need, and timeline, then trigger the lead workflow."
    elif "invoice" in normalized.lower() or "payment" in normalized.lower():
        guidance = "Recommend verifying invoice status, payment amount, and UPI reference before marking as settled."
    else:
        guidance = "Recommend capturing intent, updating CRM fields, and automating the next best action."
    content = f"{guidance} {(' '.join(summary_bits)).strip()}".strip()
    tokens = max(12, len(content.split()))
    return {
        "content": content,
        "tokens": tokens,
        "metadata": {"model": routed_model, "system_prompt": SYSTEM_PROMPT[:80]},
        "debug": {
            "model_routed": routed_model,
            "safety": "strict-business",
            "context_received": sorted(context.keys()),
        },
    }
