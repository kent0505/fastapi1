from fastapi             import APIRouter, UploadFile, HTTPException, Form, Depends
from sqlalchemy.orm      import Session
from app.database        import get_db
from app.utils           import *
from app.schemas         import *
import app.crud as crud
import logging


router = APIRouter()


@router.post("/")
async def upload_file(
        file:    UploadFile, 
        index:   int     = Form(), 
        blog_id: int     = Form(), 
        db:      Session = Depends(get_db),
    ):

    if file.filename and file.content_type.startswith("image/"):
        row = await crud.get_content_by_blog_id(db, blog_id)

        if row:
            unique_name = add_image(file)

            await crud.add_image(db, unique_name, index, blog_id)

            logging.info("POST 200 /api/v1/upload/")
            return {"message": "image uploaded successfully"}

        logging.error(f"POST 404 /api/v1/upload/ NOT FOUND")
        raise HTTPException(404, "id not found")

    logging.error("POST 400 /api/v1/upload/ FILE ERROR")
    raise HTTPException(400, "file error")


@router.put("/")
async def update_file(
        file:  UploadFile, 
        id:    int     = Form(), 
        index: int     = Form(), 
        db:    Session = Depends(get_db)
    ):

    if file.filename and file.content_type.startswith("image/"):
        row = await crud.get_content_by_id(db, id)

        if row:
            remove_image(row.title)

            unique_name = add_image(file)

            await crud.update_image(db, row, unique_name, index)

            logging.info("PUT 200 /api/v1/upload/")
            return {"message": "image updated successfully"}

        logging.error(f"PUT 404 /api/v1/upload/ NOT FOUND")
        raise HTTPException(404, "id not found")

    logging.error("PUT 400 /api/v1/upload/ FILE ERROR")
    raise HTTPException(400, "file error")