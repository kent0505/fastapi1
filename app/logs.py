from fastapi             import APIRouter, WebSocket, Depends
from app.auth.jwt_bearer import JwtBearer
from app.config          import *
import logging

router = APIRouter(dependencies=[Depends(JwtBearer())])

@router.get("/convert")
async def convert():
    with open('logfile.log', 'r') as file:
        logs_content = file.read()

    return {"logs": logs_content}


@router.get("/delete-logs")
async def delete_logs():
    with open('logfile.log', 'w'): pass
    logging.warning("LOGS DELETED")
    return {"message": "logs deleted"}


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     ws_clients.add(websocket)

#     try:
#         while True:
#             text = await websocket.receive_text()

#             ws_messages.append(text)

#             for client in ws_clients:
#                 await client.send_json({"message": ws_messages})
#     except Exception as e:
#         print(e)
#     finally:
#         ws_clients.remove(websocket)