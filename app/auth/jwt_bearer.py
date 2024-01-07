from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decodeJWT


class JwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool=True):
        super(JwtBearer, self).__init__(auto_error=auto_Error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="invalid authorization code")


    def verify_jwt(self, token: str):
        valid: bool = False
        try:
            payload = decodeJWT(token)
        except:
            payload = None
        if payload["role"] == "admin":
            valid = True
        return valid


# class UserJwtBearer(HTTPBearer):
#     def __init__(self, auto_Error: bool=True):
#         super(UserJwtBearer, self).__init__(auto_error=auto_Error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(UserJwtBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="invalid authentication scheme")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="invalid or expired token")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="invalid authorization code")

#     def verify_jwt(self, token: str):
#         valid: bool = False
#         try:
#             payload = decodeJWT(token)
#         except:
#             payload = None
#         if payload:
#             valid = True
#         return valid