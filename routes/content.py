from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
from sqlalchemy.orm  import Session
from database        import *
import os

router = APIRouter()

class ContentAdd(BaseModel):
    title:   str
    blog_id: int

class ContentUpdate(BaseModel):
    id:    int
    title: str

class ContentDelete(BaseModel):
    id: int

@router.get("/{blog_id}")
async def get_contents(blog_id: int, db: Session = Depends(get_db)):
    contentList = []

    contents = db.query(Content).filter(Content.blog_id == blog_id).all()

    for content in contents:
        contentList.append({
            "id":      content.id,
            "title":   content.title,
            "image":   content.image,
            "blog_id": content.blog_id
        })

    return {"content": contentList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_content(content: ContentAdd, db: Session = Depends(get_db)):
    row = db.query(Blog).filter(Blog.id == content.blog_id).first()

    if row:
        db.add(Content(title=content.title, image=0, blog_id=content.blog_id))
        db.commit()

        return {"message": "content added"}
    
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_content(content: ContentUpdate, db: Session = Depends(get_db)):
    row = db.query(Content).filter(Content.id == content.id).first()

    if row:
        row.title = content.title
        db.commit()

        return {"message": "content updated"}

    raise HTTPException(404, "id not found")
    

@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_content(content: ContentDelete, db: Session = Depends(get_db)):
    row = db.query(Content).filter(Content.id == content.id).first()

    if row:
        try:
            os.remove(f"static/{row.title}")
        except:
            print("not found")

        db.delete(row)
        db.commit()

        return {"message": "content deleted"}

    raise HTTPException(404, "id not found")