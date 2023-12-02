import time
import jwt
import config

def signJWT(id: str, role: str):
    expiry = time.time() + 60 * 60 * config.EXPIRY

    return jwt.encode(
        payload={"id": id, "role": role, "expiry": expiry}, 
        key=config.KEY,
        algorithm=config.ALGORITHM,
    )

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            jwt=token, 
            key=config.KEY, 
            algorithms=[config.ALGORITHM]
        )
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else: 
            return None
    except:
        return {}