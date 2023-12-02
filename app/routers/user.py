from fastapi          import APIRouter, HTTPException, Depends
from pydantic         import BaseModel
from app.auth.jwt_bearer  import JwtBearer, UserJwtBearer
from app.auth.jwt_handler import signJWT
from sqlalchemy.orm   import Session
from database         import *
import bcrypt
import config

router = APIRouter()

class UserModel(BaseModel):
    username: str
    password: str

class UserUpdateModel(BaseModel):
    id:       int
    username: str
    password: str


@router.post("/register")
async def register(user: UserModel, db: Session = Depends(get_db)):
    row = db.query(User).filter(User.username == user.username).first()

    if row or user.username.lower() == "admin":
        raise HTTPException(409, "this username already exists")

    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode()

    db.add(User(username=user.username, password=hashed))
    db.commit()

    return {"message": "user added"}


@router.post("/login")
async def login(user: UserModel, db: Session = Depends(get_db)):    
    if user.username.lower() == config.USERNAME and user.password == config.PASSWORD:
        return {"access_token": signJWT(user.username, "admin")}

    row = db.query(User).filter(User.username == user.username).first()

    if row:
        hashed = bcrypt.checkpw(user.password.encode("utf-8"), row.password.encode("utf-8"))

        if hashed and row.username == user.username:
            return {"access_token": signJWT(user.username, "user")}

    raise HTTPException(401, "username or password invalid")


@router.get("/", dependencies=[Depends(UserJwtBearer())])
async def get_users(db: Session = Depends(get_db)):
    usersList = []

    users = db.query(User).all()

    for user in users:
        usersList.append({
            "id":       user.id,
            "username": user.username,
            "password": user.password,
        })

    return {"users": usersList}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_user(user: UserUpdateModel, db: Session = Depends(get_db)):
    row = db.query(User).filter(User.id == user.id).first()

    if row and user.username.lower() != "admin":
        hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode()

        row.username = user.username
        row.password = hashed
        db.commit()

        return {"message": "user updated"}

    raise HTTPException(404, "user not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_user(user: UserUpdateModel, db: Session = Depends(get_db)):
    row = db.query(User).filter(User.id == user.id).first()

    if row:
        db.delete(row)
        db.commit()

        return {"message": "user deleted"}

    raise HTTPException(404, "user not found")