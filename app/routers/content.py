from fastapi             import APIRouter, HTTPException, Depends
from sqlalchemy.orm      import Session
from app.database        import get_db
from app.schemas         import *
from app.utils           import *
import app.crud as crud
import logging


router = APIRouter()


@router.get("/{blog_id}")
async def get_contents(blog_id: int, db: Session = Depends(get_db)):
    contentList = []

    if blog_id == 0:
        contents = await crud.get_all_contents(db)
    else:
        contents = await crud.get_all_contents_by_blog_id(db, blog_id)

    for content in contents:
        contentList.append({
            "id":      content.id,
            "title":   content.title,
            "index":   content.index,
            "image":   content.image,
            "blog_id": content.blog_id
        })

    logging.info("GET 200 /api/v1/content/")
    return {"content": contentList}


@router.post("/")
async def add_content(content: ContentAdd, db: Session = Depends(get_db)):
    row = await crud.get_content_by_blog_id(db, content.blog_id)

    if row:
        await crud.add_content(db, content)

        logging.info("POST 200 /api/v1/content/")
        return {"message": "content added"}
    
    logging.error("POST 404 /api/v1/content/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.put("/")
async def update_content(content: ContentUpdate, db: Session = Depends(get_db)):
    row = await crud.get_content_by_id(db, content.id)

    if row:
        await crud.update_content(db, row, content)

        logging.info("PUT 200 /api/v1/content/")
        return {"message": "content updated"}

    logging.error("PUT 404 /api/v1/content/ NOT FOUND")
    raise HTTPException(404, "id not found")
    

@router.delete("/")
async def delete_content(content: ContentDelete, db: Session = Depends(get_db)):
    row = await crud.get_content_by_id(db, content.id)

    if row:
        remove_image(row.title)

        await crud.delete_content(db, row)

        logging.info("DELETE 200 /api/v1/content/")
        return {"message": "content deleted"}

    logging.error("DELETE 404 /api/v1/content/ NOT FOUND")
    raise HTTPException(404, "id not found")