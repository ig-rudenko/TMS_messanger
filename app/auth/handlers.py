from fastapi import APIRouter, HTTPException, Depends

from app.auth.schemas import TokenPairSchema, UserCredentialsSchema
from app.auth.services.auth import get_user_by_credentials
from app.auth.services.exc import InvalidCredentialsError
from app.auth.services.jwt import create_token_pair
from app.orm.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenPairSchema)
async def create_token(user_data: UserCredentialsSchema, session=Depends(get_session)):
    try:
        user = await get_user_by_credentials(session, user_data.username, user_data.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return create_token_pair(user.id)


@router.post("/token/refresh")
async def refresh_token(token: str):
    return {"token": "ko3489ryn8c9n3459y2nm3904"}
