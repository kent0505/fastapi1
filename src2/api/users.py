from fastapi         import APIRouter, HTTPException, Depends
from src.core.models import *
from src.core.jwt    import *


router = APIRouter()


class UserModel(BaseModel):
    username: str
    password: str
    fcmtoken: str

class UserRegisterModel(BaseModel):
    username: str
    password: str

class UserUpdateModel(BaseModel):
    username:     str
    password:     str
    new_username: str
    new_password: str


async def db_get_all_users(db: AsyncSession) -> List[User]:
    users = await db.scalars(select(User))
    return list(users)
async def db_get_user_by_id(db: AsyncSession, id: int) -> User | None:
    user = await db.scalar(select(User).filter_by(id=id))
    return user
async def db_get_user_by_username(db: AsyncSession, username: str) -> User | None:
    user = await db.scalar(select(User).filter(User.username == username))
    return user
async def db_add_user(db: AsyncSession, body: UserRegisterModel) -> None:
    db.add(User(
        username = body.username, 
        password = body.password, 
        fcmtoken = "",
    ))
    await db.commit()
async def db_update_user(db: AsyncSession, user: User, body: UserUpdateModel) -> None:
    user.username = body.new_username
    user.password = body.new_password
    await db.commit()
async def db_update_fcmtoken(db: AsyncSession, user: User, body: UserModel) -> None:
    user.fcmtoken = body.fcmtoken
    await db.commit()
async def db_delete_user(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit()


@router.post("/login")
async def login(
    body: UserModel, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_username(db, body.username)

    if user:
        hashed = check_password(body.password, user.password)

        if hashed and user.username == body.username:
            if body.fcmtoken != "":
                await db_update_fcmtoken(db, user, body)

            access_token = signJWT(user.id, "admin")

            print(access_token)

            return {"access_token": access_token}

    raise HTTPException(401, "username or password invalid")


@router.post("/register")
async def register(
    body: UserRegisterModel, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    users = await db_get_all_users(db)
    
    for user in users:    
        if body.username == user.username:
            raise HTTPException(409, "this username already exists")

    body.password = hash_password(body.password)

    await db_add_user(db, body)

    return {"message": "user added"}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_user(
    body: UserUpdateModel, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_username(db, body.username)

    if user == None:
        raise HTTPException(404, "user not found")

    if body.new_username != "" or body.new_password != "":
        hashed = check_password(body.password, user.password)
    
        if hashed:
            body.new_password = hash_password(body.new_password)

            await db_update_user(db, user, body)

            return {"message": "user updated"}

        raise HTTPException(401, "username or password invalid")

    raise HTTPException(404, "user not found")



@router.delete("/{id}", dependencies=[Depends(JwtBearer())])
async def delete_user(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    user = await db_get_user_by_id(db, id)

    if user:
        await db_delete_user(db, user)

        return {"message": "user deleted"}

    raise HTTPException(404, "user not found")
