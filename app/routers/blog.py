from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy          import desc
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import *
import time

router = APIRouter()

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


@router.get("/")
async def get_blogs(db: Session = Depends(get_db)):
    blogList = []

    blogs = db.query(Blog).order_by(desc(Blog.index)).all()

    for blog in blogs:
        blogList.append({
            "id":          blog.id,
            "title":       blog.title,
            "index":       blog.index,
            "date":        blog.date,
            "category_id": blog.category_id,
        })

    return {"blog": blogList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_blog(blog: BlogAdd, db: Session = Depends(get_db)):
    row = db.query(Category).filter(Category.id == blog.category_id, Category.type == 0).first()

    if row:
        db.add(Blog(
            title       = blog.title, 
            index       = blog.index,
            date        = int(time.time()),
            category_id = blog.category_id,
        ))
        db.commit()

        return {"message": "blog added"}
    
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_blog(blog: BlogUpdate, db: Session = Depends(get_db)):
    row = db.query(Blog).filter(Blog.id == blog.id, Category.type == 0).first()

    if row:
        row.title       = blog.title
        row.index       = blog.index
        row.date        = int(time.time())
        row.category_id = blog.category_id
        db.commit()

        return {"message": "blog updated"}
    
    raise HTTPException(404, "id not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_blog(blog: BlogDelete, db: Session = Depends(get_db)):
    row = db.query(Blog).filter(Blog.id == blog.id).first()

    if row:
        db.delete(row)
        db.commit()

        return {"message": "blog deleted"}
    
    raise HTTPException(404, "id not found")