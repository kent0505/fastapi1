from fastapi          import APIRouter, HTTPException, Depends
from pydantic         import BaseModel
from auth.jwt_bearer  import JwtBearer
from auth.jwt_handler import signJWT
import database as DB
import bcrypt

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: User):
    username = await DB.get_username(user.username)
    if username:
        raise HTTPException(409, "this username already exists")
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode()
    await DB.create_user(user.username, hashed)
    return {"user": user}
    
@router.post("/login")
async def login(user: User):
    username = await DB.get_username(user.username)
    if username:
        hashed = bcrypt.checkpw(user.password.encode("utf-8"), username[2].encode("utf-8"))
        if hashed and username[1] == user.username:
            return {"access_token": signJWT(user.username)}
    raise HTTPException(401, "username or password invalid")
    
@router.get("/", dependencies=[Depends(JwtBearer())])
async def get_users():
    usersList = []
    users = await DB.get_users()
    for user in users:
        usersList.append({
            "id":       user[0],
            "username": user[1],
            "password": user[2],
        })
    return {"users": usersList}
    
@router.put("/{id}", dependencies=[Depends(JwtBearer())])
async def update_user(user: User, id: int):
    row = await DB.get_user(id)
    if not row:
        raise HTTPException(404, "user not found")
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode()
    await DB.update_user(user.username, hashed, id)
    return {"message": f"id {id} updated from '{row[1], row[2]}' to '{user.username, user.password}'"}
    
@router.delete("/{id}", dependencies=[Depends(JwtBearer())])
async def delete_user(id: int):
    row = await DB.get_user(id)
    if not row:
        raise HTTPException(404, "user not found")
    await DB.delete_user(id)
    return {"message": f"id {id} deleted"}