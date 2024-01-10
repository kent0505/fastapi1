from fastapi             import APIRouter, HTTPException, Depends
from sqlalchemy.orm      import Session
from app.database        import get_db
from app.schemas         import *
import app.crud as crud
import logging


router = APIRouter()


@router.get("/")
async def get_blogs(db: Session = Depends(get_db)):
    blogList = []

    blogs = await crud.get_all_blogs(db)

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


@router.post("/")
async def add_blog(blog: BlogAdd, db: Session = Depends(get_db)):
    row = await crud.get_blog_by_category_id(db, blog.category_id)

    if row:
        await crud.add_blog(db, blog)

        logging.info("POST 200 /api/v1/blog/")
        return {"message": "blog added"}
    
    logging.error("POST 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.put("/")
async def update_blog(blog: BlogUpdate, db: Session = Depends(get_db)):
    row = await crud.get_blog_by_id(db, blog.id)

    if row:
        await crud.update_blog(db, row, blog)

        logging.info("PUT 200 /api/v1/blog/")
        return {"message": "blog updated"}
    
    logging.error("PUT 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.delete("/")
async def delete_blog(blog: BlogDelete, db: Session = Depends(get_db)):
    row = await crud.get_blog_by_id(db, blog.id)

    if row:
        await crud.delete_blog(db, row)

        logging.info("DELETE 200 /api/v1/blog/")
        return {"message": "blog deleted"}
    
    logging.error("DELETE 404 /api/v1/blog/ NOT FOUND")
    raise HTTPException(404, "id not found")