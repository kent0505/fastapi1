from fastapi              import APIRouter, HTTPException, Depends
from pydantic             import BaseModel
from sqlalchemy.orm       import Session
from app.auth.jwt_bearer  import JwtBearer
from app.auth.jwt_handler import signJWT
from app.config           import *
from app.database         import *
from app.utils            import *
import app.crud as DB

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


@router.post("/register")
async def register(user: UserModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_username(db, user.username)

    if row or user.username.lower() == "admin":
        raise HTTPException(409, "this username already exists")

    hashed = hash_password(user.password)

    DB.add_user(db, user.username, hashed)

    return {"message": "user added"}


@router.post("/login")
async def login(user: UserModel, db: Session = Depends(get_db)):    
    if user.username.lower() == USERNAME and user.password == PASSWORD:
        return {"access_token": signJWT(user.username, "admin")}

    row = DB.get_user_by_username(db, user.username)

    if row:
        hashed = check_password(user.password, row.password)

        if hashed and row.username == user.username:
            return {"access_token": signJWT(user.username, "user")}

    raise HTTPException(401, "username or password invalid")


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

    return {"users": usersList}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_user(user: UserUpdateModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_id(db, user.id)

    if row and user.username != "" or user.password != "" and user.username.lower() != "admin":
        hashed = hash_password(user.password)

        DB.update_user(db, row, user.username, hashed)

        return {"message": "user updated"}

    raise HTTPException(404, "user not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_user(user: UserDeleteModel, db: Session = Depends(get_db)):
    row = DB.get_user_by_id(db, user.id)

    if row:
        DB.delete_user(db, row)

        return {"message": "user deleted"}

    raise HTTPException(404, "user not found")