from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_, and_

from .models import Message
from ..auth.models import User


class ChatError(Exception):
    pass


async def create_message(session: AsyncSession, sender_id: int, recipient_id: int, message: str) -> Message:
    recipient = await session.get(User, recipient_id)
    if recipient is None:
        raise ChatError("Получатель не найден")

    message = Message(sender_id=sender_id, recipient_id=recipient_id, message=message)
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def get_last_messages(session: AsyncSession, chat_id: int, user_id: int, limit: int = 100) -> list[Message]:
    chat = await session.get(User, chat_id)
    if chat is None:
        raise ChatError("Чат не найден")

    query = (
        select(Message)
        .where(
            or_(
                and_(Message.sender_id == user_id, Message.recipient_id == chat_id),
                and_(Message.recipient_id == user_id, Message.sender_id == chat_id),
            )
        )
        .group_by(Message.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = (await session.execute(query)).scalars()
    return list(result)
