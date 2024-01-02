from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import get_db
import app.crud as DB
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

    blogs = DB.get_all_blogs(db)

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
    row = DB.get_blog_by_category_id(db, blog.category_id)

    if row:
        DB.add_blog(db, blog.title, blog.index, int(time.time()), blog.category_id)

        return {"message": "blog added"}
    
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_blog(blog: BlogUpdate, db: Session = Depends(get_db)):
    row = DB.get_blog_by_id(db, blog.id)

    if row:
        DB.update_blog(db, row, blog.title, blog.index, int(time.time()), blog.category_id)

        return {"message": "blog updated"}
    
    raise HTTPException(404, "id not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_blog(blog: BlogDelete, db: Session = Depends(get_db)):
    row = DB.get_blog_by_id(db, blog.id)

    if row:
        DB.delete_blog(db, row)

        return {"message": "blog deleted"}
    
    raise HTTPException(404, "id not found")