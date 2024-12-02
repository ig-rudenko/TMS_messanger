from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.services.exc import InvalidCredentialsError, AuthError
from app.auth.services.jwt import auth_scheme, _get_user_from_token
from app.orm.session import get_session


async def get_user_by_credentials(session: AsyncSession, username: str, password: str) -> User:
    query = select(User).where(User.username == username, User.password == password)
    user: User | None = (await session.execute(query)).scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError("Имя пользователя или пароль введены не верно")

    if not user.is_active:
        raise InvalidCredentialsError("Пользователь не активен")

    return user


async def get_user(token: str = Depends(auth_scheme), session: AsyncSession = Depends(get_session)) -> User:
    try:
        user_id = _get_user_from_token(token)
    except AuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

    query = select(User).where(User.id == user_id)
    try:
        user = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user
