from src.config import *
import time
import jwt


def signJWT(id: str, role: str):
    expiry = time.time() + 60 * 60 * 24 # 24 hours

    return jwt.encode(
        payload={"id": id, "role": role, "expiry": expiry}, 
        key=KEY,
        algorithm="HS256",
    )


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            jwt=token, 
            key=KEY, 
            algorithms=["HS256"]
        )
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else: 
            return None
    except:
        return {}