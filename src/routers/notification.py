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
    row = await crud.get_user_by_username(db, model.username)
    if row == None:
        raise HTTPException(404, "user not found")

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title = model.title,
            body  = model.body,
        ),
        tokens=[row.fcmtoken]
    )
    messaging.send_multicast(message)
    return {"message": "notification sent"}
