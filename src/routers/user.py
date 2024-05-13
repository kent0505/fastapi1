from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.jwt_bearer    import JwtBearer
from src.auth.jwt_handler   import signJWT
from src.database           import get_db
from src.schemas            import *
from src.config             import *
from src.utils              import *
import src.crud             as crud


router = APIRouter()


@router.post("/login")
async def login(
    user: UserModel, 
    db:   AsyncSession = Depends(get_db)
):
    row = await crud.get_user_by_username(db, user.username)

    if row:
        hashed = check_password(user.password, row.password)

        if hashed and row.username == user.username:
            await crud.update_fcmtoken(db, row, user)

            access_token = signJWT(user.username, "admin")

            print(access_token)
            
            return {"access_token": access_token}

    raise HTTPException(401, "username or password invalid")


@router.post("/register")
async def register(
    user: UserModel, 
    db:   AsyncSession = Depends(get_db)
):
    users = await crud.get_all_users(db)
    if users != []:
        raise HTTPException(409, "admin already exists")

    # row = await crud.get_user_by_username(db, user)

    # if row or user.username.lower() == "admin":
    #     raise HTTPException(409, "this username already exists")

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    await crud.add_user(db, user)

    return {"message": "user added"}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_user(
    user: UserUpdateModel, 
    db:   AsyncSession = Depends(get_db)
):
    row = await crud.get_user_by_username(db, user.username)
    if row == None:
        raise HTTPException(404, "user not found")

    if user.new_username != "" or user.new_password != "":
        hashed = check_password(user.password, row.password)

        if hashed:
            hashed_password = hash_password(user.new_password)
            user.new_password = hashed_password

            await crud.update_user(db, row, user)

            return {"message": "user updated"}

        raise HTTPException(401, "username or password invalid")

    raise HTTPException(404, "user not found")


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


# @router.delete("/{id}", dependencies=[Depends(JwtBearer())])
# async def delete_user(id: int, db: Session = Depends(get_db)):
#     row = await crud.get_user_by_id(db, id)

#     if row:
#         await crud.delete_user(db, row)

#         logging.info(f"DELETE 200 /api/v1/user/ {id}")
#         return {"message": "user deleted"}

#     logging.error(f"DELETE 404 /api/v1/user/ {id}")
#     raise HTTPException(404, "user not found")


# @router.post("/login")
# async def login(user: UserModel):
#     hashed = check_password(user.password, PASSWORD)
#     if user.username.lower() == USERNAME and hashed:
#         log("POST 200 /api/v1/user/login/")
#         return {"access_token": signJWT(user.username, "admin")}

#     log(f"POST 401 /api/v1/user/login/ {user.username} {user.password}")
#     raise HTTPException(401, "username or password invalid")