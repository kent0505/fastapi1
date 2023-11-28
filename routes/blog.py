from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
from sqlalchemy.orm  import Session
from database        import *

router = APIRouter()

class BlogAdd(BaseModel):
    title:       str
    category_id: int

class BlogUpdate(BaseModel):
    id:          int
    title:       str
    category_id: int

class BlogDelete(BaseModel):
    id: int


@router.get("/")
async def get_blogs(db: Session = Depends(get_db)):
    blogList = []

    blogs = db.query(Blog).all()

    for blog in blogs:
        blogList.append({
            "id":          blog.id,
            "title":       blog.title,
            "category_id": blog.category_id,
        })

    return {"blog": blogList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_blog(blog: BlogAdd, db: Session = Depends(get_db)):
    row = db.query(Category).filter(Category.id == blog.category_id).first()

    if row:
        db.add(Blog(title=blog.title, category_id=blog.category_id))
        db.commit()

        return {"blog": blog}
    
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_blog(blog: BlogUpdate, db: Session = Depends(get_db)):
    row = db.query(Blog).filter(Blog.id == blog.id).first()

    if row:
        row.title =       blog.title
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