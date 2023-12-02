import time
import jwt
from app.config import *

def signJWT(id: str, role: str):
    expiry = time.time() + 60 * 60 * EXPIRY

    return jwt.encode(
        payload={"id": id, "role": role, "expiry": expiry}, 
        key=KEY,
        algorithm=ALGORITHM,
    )

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            jwt=token, 
            key=KEY, 
            algorithms=[ALGORITHM]
        )
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else: 
            return None
    except:
        return {}