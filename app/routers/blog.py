from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import get_db
from app.utils           import get_timestamp
import app.crud as DB
import logging


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

    blogs = await DB.get_all_blogs(db)

    for blog in blogs:
        blogList.append({
            "id":          blog.id,
            "title":       blog.title,
            "index":       blog.index,
            "date":        blog.date,
            "category_id": blog.category_id,
        })

    logging.info("GET 200 /api/v1/blog/")
    return {"blog": blogList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_blog(blog: BlogAdd, db: Session = Depends(get_db)):
    row = await DB.get_blog_by_category_id(db, blog.category_id)

    if row:
        timestamp = get_timestamp()

        await DB.add_blog(db, blog.title, blog.index, timestamp, blog.category_id)

        logging.info("POST 200 /api/v1/blog/")
        return {"message": "blog added"}
    
    logging.error("POST 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_blog(blog: BlogUpdate, db: Session = Depends(get_db)):
    row = await DB.get_blog_by_id(db, blog.id)

    if row:
        timestamp = get_timestamp()

        await DB.update_blog(db, row, blog.title, blog.index, timestamp, blog.category_id)

        logging.info("PUT 200 /api/v1/blog/")
        return {"message": "blog updated"}
    
    logging.error("PUT 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_blog(blog: BlogDelete, db: Session = Depends(get_db)):
    row = await DB.get_blog_by_id(db, blog.id)

    if row:
        await DB.delete_blog(db, row)

        logging.info("DELETE 200 /api/v1/blog/")
        return {"message": "blog deleted"}
    
    logging.error("DELETE 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")