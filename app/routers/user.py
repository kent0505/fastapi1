from fastapi              import APIRouter, HTTPException

from app.auth.jwt_handler import signJWT
from app.schemas          import *
from app.config           import *
from app.utils            import *


router = APIRouter()


@router.post("/login")
async def login(user: UserModel):
    if user.username.lower() == USERNAME and user.password == PASSWORD:
        log("POST 200 /api/v1/user/login/")
        return {"access_token": signJWT(user.username, "admin")}

    log(f"POST 401 /api/v1/user/login/ {user.username} {user.password}")
    raise HTTPException(401, "username or password invalid")


# @router.post("/login")
# async def login(user: UserModel, db: Session = Depends(get_db)):
#     if user.username.lower() == USERNAME and user.password == PASSWORD:
#         logging.info("POST 200 /api/v1/user/login/")
#         return {"access_token": signJWT(user.username, "admin")}

#     row = await crud.get_user_by_username(db, user.username)

#     if row:
#         hashed = check_password(user.password, row.password)

#         if hashed and row.username == user.username:
#             logging.info("POST 200 /api/v1/user/login/")
#             return {"access_token": signJWT(user.username, "user")}

#     logging.error("POST 401 /api/v1/user/login/")
#     raise HTTPException(401, "username or password invalid")


# @router.post("/register")
# async def register(user: UserModel, db: Session = Depends(get_db)):
#     row = await crud.get_user_by_username(db, user)

#     if row or user.username.lower() == "admin":
#         logging.error("POST 409 /api/v1/user/register/")
#         raise HTTPException(409, "this username already exists")

#     hashed = hash_password(user.password)
#     user.password = hashed

#     await crud.add_user(db, user)

#     logging.info("POST 200 /api/v1/user/register/")
#     return {"message": "user added"}


# @router.get("/", dependencies=[Depends(JwtBearer())])
# async def get_users(db: Session = Depends(get_db)):
#     usersList = []

#     users = await crud.get_all_users(db)

#     for user in users:
#         usersList.append({
#             "id":       user.id,
#             "username": user.username,
#             "password": user.password,
#         })

#     logging.info("GET 200 /api/v1/user/")
#     return {"users": usersList}


# @router.put("/", dependencies=[Depends(JwtBearer())])
# async def update_user(user: UserUpdateModel, db: Session = Depends(get_db)):
#     row = await crud.get_user_by_id(db, user.id)

#     if row and user.username != "" or user.password != "" and user.username.lower() != "admin":
#         hashed = hash_password(user.password)
#         user.password = hashed

#         await crud.update_user(db, row, user)

#         logging.info("PUT 200 /api/v1/user/")
#         return {"message": "user updated"}
    
#     logging.error("PUT 404 /api/v1/user/ NOT FOUND")
#     raise HTTPException(404, "user not found")


# @router.delete("/", dependencies=[Depends(JwtBearer())])
# async def delete_user(user: UserDeleteModel, db: Session = Depends(get_db)):
#     row = await crud.get_user_by_id(db, user.id)

#     if row:
#         await crud.delete_user(db, row)

#         logging.info(f"DELETE 200 /api/v1/user/")
#         return {"message": "user deleted"}

#     logging.error(f"DELETE 404 /api/v1/user/ NOT FOUND")
#     raise HTTPException(404, "user not found")