import time
import jwt

key = "hfasdg7SDF6gFGsgdf4"

def signJWT(id: str):
    return jwt.encode(
        payload={"id": id, "expiry": time.time() + 60 * 60 * 24}, 
        key=key,
        algorithm="HS256",
    )

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        print(decoded_token)
        print(time.time())
        if decoded_token["expiry"] >= time.time():
            return decoded_token
        else: 
            return None
    except:
        return {}