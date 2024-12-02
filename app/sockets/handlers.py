from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .auth import auth_websocket
from .manager import manager

router = APIRouter(prefix="", tags=["ws"])


@router.websocket("")
async def ws(websocket: WebSocket, user=Depends(auth_websocket)):
    await manager.connect(websocket, user.id)

    try:
        while True:
            message = await websocket.receive_text()
            await manager.analyze_message(message, user.id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user.id)
