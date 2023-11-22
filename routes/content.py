from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
import database as DB
import os

router = APIRouter()

class Body(BaseModel):
    title: str

class ContentAdd(BaseModel):
    title:   str
    blog_id: int

class ContentUpdate(BaseModel):
    id:    int
    title: str

class ContentDelete(BaseModel):
    id: int

@router.get("/{blog_id}")
async def get_contents(blog_id: int):
    contentList = []
    contents = await DB.get_contents(blog_id)
    for content in contents:
        contentList.append({
            "id":      content[0],
            "title":   content[1],
            "blog_id": content[2],
        })
    return {"content": contentList}

@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_content(content: ContentAdd):
    blog = await DB.get_blog(content.blog_id)
    if not blog:
        raise HTTPException(404, "id not found")
    await DB.add_content(content.title, 0, content.blog_id)
    return {"content": content}

@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_content(content: ContentUpdate):
    row = await DB.get_content(content.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.update_content(content.id, content.title)
    return {"message": "content updated"}

@router.delete("/")
async def delete_content(content: ContentDelete):
    row = await DB.get_content(content.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.delete_content(content.id)
    try:
        os.remove(f"static/{row[1]}")
    except:
        print("not found")
    return {"message": "content deleted"}