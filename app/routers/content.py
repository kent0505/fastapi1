from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import get_db
from app.utils           import *
import app.crud as DB

router = APIRouter()

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


@router.get("/{blog_id}")
async def get_contents(blog_id: int, db: Session = Depends(get_db)):
    contentList = []

    if blog_id == 0:
        contents = DB.get_all_contents(db)
    else:
        contents = DB.get_all_contents_by_blog_id(db, blog_id)

    for content in contents:
        contentList.append({
            "id":      content.id,
            "title":   content.title,
            "index":   content.index,
            "image":   content.image,
            "blog_id": content.blog_id
        })

    return {"content": contentList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_content(content: ContentAdd, db: Session = Depends(get_db)):
    row = DB.get_content_by_blog_id(db, content.blog_id)

    if row:
        DB.add_content(db, content.title, content.index, 0, content.blog_id)

        return {"message": "content added"}
    
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_content(content: ContentUpdate, db: Session = Depends(get_db)):
    row = DB.get_content_by_id(db, content.id)

    if row:
        DB.update_content(db, row, content.title, content.index)

        return {"message": "content updated"}

    raise HTTPException(404, "id not found")
    

@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_content(content: ContentDelete, db: Session = Depends(get_db)):
    row = DB.get_content_by_id(db, content.id)

    if row:
        remove_image(row.title)

        DB.delete_content(db, row)

        return {"message": "content deleted"}

    raise HTTPException(404, "id not found")