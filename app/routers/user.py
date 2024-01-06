from fastapi              import APIRouter, HTTPException, Depends
from pydantic             import BaseModel
from sqlalchemy.orm       import Session
from app.auth.jwt_bearer  import JwtBearer
from app.auth.jwt_handler import signJWT
from app.database         import get_db
from app.config           import *
from app.utils            import *
import app.crud as DB
import logging


router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str

class UserUpdateModel(BaseModel):
    id:       int
    username: str
    password: str

class UserDeleteModel(BaseModel):
    id: int


@router.post("/login")
async def login(user: UserModel, db: Session = Depends(get_db)):
    if user.username.lower() == USERNAME and user.password == PASSWORD:
        logging.info("POST 200 /api/v1/user/login/")
        return {"access_token": signJWT(user.username, "admin")}

    row = DB.get_user_by_username(db, user.username)

    if row:
        hashed = check_password(user.password, row.password)

        if hashed and row.username == user.username:
            logging.info("POST 200 /api/v1/user/login/")
            return {"access_token": signJWT(user.username, "user")}

    logging.error("POST 401 /api/v1/user/login/")
    raise HTTPException(401, "username or password invalid")


@router.post("/register")
async def register(user: UserModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_username(db, user.username)

    if row or user.username.lower() == "admin":
        logging.error("POST 409 /api/v1/user/register/")
        raise HTTPException(409, "this username already exists")

    hashed = hash_password(user.password)

    DB.add_user(db, user.username, hashed)

    logging.info("POST 200 /api/v1/user/register/")
    return {"message": "user added"}


@router.get("/", dependencies=[Depends(JwtBearer())])
async def get_users(db: Session = Depends(get_db)):
    usersList = []

    users = DB.get_all_users(db)

    for user in users:
        usersList.append({
            "id":       user.id,
            "username": user.username,
            "password": user.password,
        })

    logging.info("GET 200 /api/v1/user/")
    return {"users": usersList}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_user(user: UserUpdateModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_id(db, user.id)

    if row and user.username != "" or user.password != "" and user.username.lower() != "admin":
        hashed = hash_password(user.password)

        DB.update_user(db, row, user.username, hashed)

        logging.info("PUT 200 /api/v1/user/")
        return {"message": "user updated"}
    
    logging.error("PUT 404 /api/v1/user/ NOT FOUND")
    raise HTTPException(404, "user not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_user(user: UserDeleteModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_id(db, user.id)

    if row:
        DB.delete_user(db, row)

        logging.info(f"DELETE 200 /api/v1/user/")
        return {"message": "user deleted"}

    logging.error(f"DELETE 404 /api/v1/user/ NOT FOUND")
    raise HTTPException(404, "user not found")