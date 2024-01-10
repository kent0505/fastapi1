from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str


class UserUpdateModel(BaseModel):
    id:       int
    username: str
    password: str


class UserDeleteModel(BaseModel):
    id: int


class CategoryAdd(BaseModel):
    title: str
    index: int
    type:  int


class CategoryUpdate(BaseModel):
    id:    int
    title: str
    index: int
    type:  int


class CategoryDelete(BaseModel):
    id: int


class BlogAdd(BaseModel):
    title:       str
    index:       int
    category_id: int


class BlogUpdate(BaseModel):
    id:          int
    title:       str
    index:       int
    category_id: int


class BlogDelete(BaseModel):
    id: int


class ContentAdd(BaseModel):
    title:   str
    index:   int
    blog_id: int


class ContentUpdate(BaseModel):
    id:    int
    title: str
    index: int


class ContentDelete(BaseModel):
    id: int