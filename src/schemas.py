from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str


class UserUpdateModel(BaseModel):
    username: str
    password: str
    new_username: str
    new_password: str


class CategoryAdd(BaseModel):
    title: str
    index: int
    type:  int


class CategoryUpdate(BaseModel):
    id:    int
    title: str
    index: int
    type:  int


class BlogAdd(BaseModel):
    title: str
    index: int
    cid:   int


class BlogUpdate(BaseModel):
    id:    int
    title: str
    index: int
    cid:   int


class ContentAdd(BaseModel):
    title: str
    index: int
    bid:   int


class ContentUpdate(BaseModel):
    id:    int
    title: str
    index: int