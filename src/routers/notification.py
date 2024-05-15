from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from firebase_admin         import credentials, messaging
from src.database           import get_db
from src.schemas            import *
import src.crud             as crud
import firebase_admin


firebase_cred = credentials.Certificate("firebase.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)


router = APIRouter()

@router.post("/send_notification")
async def send_notification(
    model: NotificationModel, 
    db:    AsyncSession = Depends(get_db)
):
    tokens = []

    users = await crud.get_all_users(db)
    for user in users:
        tokens.append(user.fcmtoken)

    print(tokens)

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title = model.title,
            body  = model.body,
        ),
        tokens=tokens
    )
    messaging.send_multicast(message)

    return {"message": "notification sent"}
