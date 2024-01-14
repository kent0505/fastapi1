from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database           import get_db
from app.schemas            import *
from app.utils              import *

import app.crud as crud


router = APIRouter()


@router.get("/")
async def get_blogs(db: AsyncSession = Depends(get_db)):
    blogList = []

    blogs = await crud.get_all_blogs(db)

    for blog in blogs:
        blogList.append({
            "id":    blog.id,
            "title": blog.title,
            "index": blog.index,
            "date":  blog.date,
            "cid":   blog.cid,
        })

    log("GET 200 /api/v1/blog/")
    return {"blog": blogList}


@router.post("/")
async def add_blog(blog: BlogAdd, db: AsyncSession = Depends(get_db)):
    row = await crud.get_blog_by_cid(db, blog.cid)

    if row:
        await crud.add_blog(db, blog)

        log(f"POST 200 /api/v1/blog/ {blog.cid}")
        return {"message": "blog added"}
    
    log(f"POST 404 /api/v1/blog/ {blog.cid}")
    raise HTTPException(404, "id not found")


@router.put("/")
async def update_blog(blog: BlogUpdate, db: AsyncSession = Depends(get_db)):
    row = await crud.get_blog_by_id(db, blog.id)

    if row:
        await crud.update_blog(db, row, blog)

        log(f"PUT 200 /api/v1/blog/ {blog.id}")
        return {"message": "blog updated"}
    
    log(f"PUT 404 /api/v1/blog/ {blog.id}")
    raise HTTPException(404, "id not found")


@router.delete("/")
async def delete_blog(blog: BlogDelete, db: AsyncSession = Depends(get_db)):
    row = await crud.get_blog_by_id(db, blog.id)

    if row:
        await crud.delete_blog(db, row)

        log(f"DELETE 200 /api/v1/blog/ {blog.id}")
        return {"message": "blog deleted"}
    
    log(f"DELETE 404 /api/v1/blog/ {blog.id}")
    raise HTTPException(404, "id not found")