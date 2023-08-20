from app.apps.chat import models, schemas
from app.apps.chat.managers import manager
from app.apps.chat.repository import ChatRepository
from fastapi import APIRouter, status, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


@router.get('/', response_model=schemas.Messages)
async def get_all_messages():
    try:
        objects = await models.Message.all()
        return {"items": objects}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete('/{message_id}')
async def delete_message(message_id: int):
    try:
        deleted_message = await ChatRepository().delete_one(message_id)
        if deleted_message is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Message with id: {message_id} not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Success deleted message"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Message with id: {message_id} not found")


@router.websocket('/ws/{client_id}')
async def ws_connection(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} connected")
    try:
        while True:
            data = await websocket.receive_text()
            await ChatRepository().add_one(schemas.MessageBase(
                text=data
            ).model_dump())
            await manager.broadcast(f"({client_id}): {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")