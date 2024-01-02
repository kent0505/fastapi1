from fastapi             import APIRouter, UploadFile, HTTPException, Form, Depends
from app.auth.jwt_bearer import JwtBearer
from sqlalchemy.orm      import Session
from app.database        import get_db
from app.utils           import *
import app.crud as DB
import logging

router = APIRouter(dependencies=[Depends(JwtBearer())])


@router.post("/")
async def upload_file(
        file:    UploadFile, 
        index:   int     = Form(), 
        blog_id: int     = Form(), 
        db:      Session = Depends(get_db)
    ):

    if not file.filename and file.content_type.startswith("image/"):
        logging.error("FILE ERROR")
        raise HTTPException(400, "file error")

    row = DB.get_content_by_blog_id(db, blog_id)

    if row:
        unique_name = add_image(file)

        DB.add_content(db, unique_name, index, 1, blog_id)

        return {"message": "image uploaded successfully"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_file(
        file:  UploadFile, 
        id:    int     = Form(), 
        index: int     = Form(), 
        db:    Session = Depends(get_db)
    ):

    row = DB.get_content_by_id(db, id)

    if row:
        remove_image(row.title)

        unique_name = add_image(file)

        DB.update_image(db, row, unique_name, index)

        return {"message": "image updated successfully"}

    raise HTTPException(404, "id not found")