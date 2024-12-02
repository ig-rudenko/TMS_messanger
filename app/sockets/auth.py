from fastapi import WebSocket, Depends, WebSocketDisconnect, HTTPException, WebSocketException
from fastapi import status

from app.auth.models import User
from app.auth.services.auth import get_user
from app.orm.session import get_session


async def auth_websocket(websocket: WebSocket, session=Depends(get_session)) -> User:
    await websocket.accept()

    try:
        token = await websocket.receive_text()
    except WebSocketDisconnect:
        raise WebSocketException(code=status.WS_1013_TRY_AGAIN_LATER, reason="Disconnected")

    try:
        user = await get_user(token, session)
    except HTTPException as exc:
        raise WebSocketException(code=status.WS_1013_TRY_AGAIN_LATER, reason=exc.detail)

    await websocket.send_json({"type": "system", "status": "ok", "message": "User authenticated"})
    return user
