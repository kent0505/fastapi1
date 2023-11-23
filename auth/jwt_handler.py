import time
import jwt
import config

def signJWT(id: str):
    expiry = time.time() + 60 * 60 * config.expiry

    return jwt.encode(
        payload={"id": id, "expiry": expiry}, 
        key=config.key,
        algorithm=config.algorithm,
    )

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(
            jwt=token, 
            key=config.key, 
            algorithms=[config.algorithm]
        )
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else: 
            return None
    except:
        return {}