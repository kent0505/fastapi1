from fastapi         import APIRouter, HTTPException, Depends
from firebase_admin  import messaging
from src.core.utils  import check_firebase_file
from src.core.models import *


router = APIRouter()


class NotificationModel(BaseModel):
    title:    str
    body:     str


async def db_get_all_users(db: AsyncSession) -> List[User]:
    users = await db.scalars(select(User))
    return list(users)


@router.post("/send_notification")
async def send_notification(
    model: NotificationModel, 
    db:    AsyncSession = Depends(db_helper.get_db)
):  
    error = check_firebase_file()
    
    if error:
        raise HTTPException(400, "firebase error")

    tokens: List[str] = []

    users = await db_get_all_users(db)

    for user in users:
        if user.fcmtoken != "":
            tokens.append(user.fcmtoken)

    if tokens == []:
        return {"message": "fcm tokens not found"}

    else:
        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title = model.title,
                    body  = model.body,
                ),
                tokens=tokens
            )
            messaging.send_multicast(message)

            return {"message": "notification sent"}
        except:
            raise HTTPException(400, "firebase error")