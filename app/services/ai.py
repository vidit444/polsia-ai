from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.audit_log import AuditLog
from app.schemas.ai import AIChatRequest, AIChatResponse


class AIService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.settings = get_settings()

    async def chat(self, payload: AIChatRequest, actor) -> AIChatResponse:
        provider = self.settings.ai_default_provider.lower()
        credential_map = {
            "openai": self.settings.openai_api_key,
            "anthropic": self.settings.anthropic_api_key,
        }
        _ = credential_map.get(provider)

        response_text = (
            "Polsia AI orchestration response: prompt accepted, workflows and analytics can be chained "
            "through downstream workers with retry, audit, and tenant isolation."
        )
        self.session.add(
            AuditLog(
                tenant_id=payload.tenant_id,
                actor_user_id=actor.id,
                action="ai.chat",
                entity="ai_request",
                metadata_json={"provider": provider, "prompt_length": len(payload.prompt)},
            )
        )
        await self.session.commit()
        return AIChatResponse(
            provider=provider,
            message=response_text,
            debug_review_interval_seconds=self.settings.debug_review_interval_seconds,
            payment_qr_url=self.settings.upi_qr_url,
        )
