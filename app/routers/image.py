from fastapi                import APIRouter, UploadFile, HTTPException, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database           import get_db
from app.schemas            import *
from app.utils              import *

import app.crud as crud


router = APIRouter()


@router.post("/")
async def upload_file(
        file:  UploadFile, 
        index: int = Form(), 
        bid:   int = Form(), 
        db:    AsyncSession = Depends(get_db),
    ):

    if file.filename and file.content_type.startswith("image/"):
        row = await crud.get_content_by_bid(db, bid)

        if row:
            unique_name = add_image(file)

            await crud.add_image(db, unique_name, index, bid)

            log(f"POST 200 /api/v1/upload/ {bid}")
            return {"message": "image uploaded successfully"}

        log(f"POST 404 /api/v1/upload/ {bid}")
        raise HTTPException(404, "id not found")

    log("POST 400 /api/v1/upload/ FILE ERROR")
    raise HTTPException(400, "file error")


@router.put("/")
async def update_file(
        file:  UploadFile, 
        id:    int = Form(), 
        index: int = Form(), 
        db:    AsyncSession = Depends(get_db)
    ):

    if file.filename and file.content_type.startswith("image/"):
        row = await crud.get_content_by_id(db, id)

        if row:
            remove_image(row.title)

            unique_name = add_image(file)

            await crud.update_image(db, row, unique_name, index)

            log(f"PUT 200 /api/v1/upload/ {id}")
            return {"message": "image updated successfully"}

        log(f"PUT 404 /api/v1/upload/ {id}")
        raise HTTPException(404, "id not found")

    log("PUT 400 /api/v1/upload/ FILE ERROR")
    raise HTTPException(400, "file error")