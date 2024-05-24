from fastapi         import APIRouter, UploadFile, HTTPException, Form, Depends
from src.core.utils  import check_picked_file, add_image, remove_image
from src.core.models import *


router = APIRouter()


async def db_get_content_by_id(db: AsyncSession, id: int) -> Content | None:
    content = await db.scalar(select(Content).filter(Content.id == id))
    return content
async def db_get_blog_by_bid(db: AsyncSession, bid: int) -> Blog | None:
    blog = await db.scalar(select(Blog).filter(Blog.id == bid))
    return blog
async def db_add_image(db: AsyncSession, title: str, index: int, bid: int):
    db.add(Content(
        title = title,
        index = index,
        image = 1, 
        bid   = bid
    ))
    await db.commit()
async def db_update_image(db: AsyncSession, content: Content, title: str, index: int):
    content.title = title
    content.index = index
    content.image = 1
    await db.commit()


@router.post("/")
async def upload_file(
    file:  UploadFile, 
    bid:   int = Form(), 
    index: int = Form(default=0), 
    db:    AsyncSession = Depends(db_helper.get_db),
):
    valid_file = check_picked_file(file)

    if valid_file:
        row = await db_get_blog_by_bid(db, bid)

        if row:
            unique_name = add_image(file)

            await db_add_image(db, unique_name, index, bid)

            return {"message": "image uploaded successfully"}

        raise HTTPException(404, "id not found")

    raise HTTPException(400, "file error")


@router.put("/")
async def update_file(
    file:  UploadFile, 
    id:    int = Form(), 
    index: int = Form(default=0), 
    db:    AsyncSession = Depends(db_helper.get_db)
):
    valid_file = check_picked_file(file)

    if valid_file:
        row = await db_get_content_by_id(db, id)

        if row:
            remove_image(row.title)

            unique_name = add_image(file)

            await db_update_image(db, row, unique_name, index)

            return {"message": "image updated successfully"}

        raise HTTPException(404, "id not found")

    raise HTTPException(400, "file error")