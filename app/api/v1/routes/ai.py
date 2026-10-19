from fastapi import APIRouter, Depends, Request

from app.api.deps import get_current_user, get_tenant_id
from app.db.memory import store
from app.models.domain import Conversation, Message, User
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_orchestrator import generate_ai_response
from app.services.audit import record_audit_log

router = APIRouter()


@router.post("/chat", response_model=AIChatResponse)
def chat(payload: AIChatRequest, request: Request, current_user: User = Depends(get_current_user), tenant_id: str = Depends(get_tenant_id)):
    conversation = store.get("conversations", payload.conversation_id) if payload.conversation_id else None
    if not conversation:
        conversation = Conversation(tenant_id=tenant_id, channel=payload.channel, external_ref=current_user.id)
        store.insert("conversations", conversation)
    user_message = Message(conversation_id=conversation.id, sender_type="user", content=payload.message, tokens=len(payload.message.split()))
    store.insert("messages", user_message)
    response = generate_ai_response(payload.message, payload.context, payload.model_preference)
    assistant_message = Message(
        conversation_id=conversation.id,
        sender_type="assistant",
        content=response["content"],
        tokens=response["tokens"],
        metadata_json=response["metadata"],
    )
    store.insert("messages", assistant_message)
    record_audit_log(tenant_id, current_user.id, "ai.chat", "conversation", conversation.id, request.client.host if request.client else None)
    return AIChatResponse(
        conversation=conversation.model_dump(mode="json"),
        user_message=user_message.model_dump(mode="json"),
        assistant_message=assistant_message.model_dump(mode="json"),
        debug=response["debug"],
    )
