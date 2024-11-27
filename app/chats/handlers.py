from fastapi import APIRouter, Depends, HTTPException

from app.auth.services.auth import get_user
from app.chats.schemas import NewMessageSchema, MessageSchema
from app.chats.services import create_message, get_last_messages, ChatError
from app.orm.session import get_session

router = APIRouter(prefix="/chats", tags=["chats"])


# TEMP API


@router.post("/{chat_id}/sendMessage", response_model=MessageSchema)
async def create_message_api_view(
    chat_id: int,
    data: NewMessageSchema,
    user=Depends(get_user),
    session=Depends(get_session),
):
    try:
        return await create_message(session, sender_id=user.id, recipient_id=chat_id, message=data.message)
    except ChatError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{chat_id}/lastMessages", response_model=list[MessageSchema])
async def get_last_messages_api_view(
    chat_id: int,
    user=Depends(get_user),
    session=Depends(get_session),
):
    try:
        return await get_last_messages(session, chat_id=chat_id, user_id=user.id, limit=100)
    except ChatError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{chat_id}/unreadMessagesCount", response_model=int)
async def get_unread_messages_count_api_view(chat_id: int):
    pass
