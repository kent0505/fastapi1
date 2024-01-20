from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database           import get_db
from app.schemas            import *
from app.utils              import *

import app.crud as crud


router = APIRouter()


@router.get("/{bid}")
async def get_contents(bid: int, db: AsyncSession = Depends(get_db)):
    contentList = []

    if bid == 0:
        contents = await crud.get_all_contents(db)
    else:
        contents = await crud.get_all_contents_by_bid(db, bid)

    for content in contents:
        contentList.append({
            "id":    content.id,
            "title": content.title,
            "index": content.index,
            "image": content.image,
            "bid":   content.bid
        })

    return {"content": contentList}


@router.post("/")
async def add_content(content: ContentAdd, db: AsyncSession = Depends(get_db)):
    row = await crud.get_content_by_bid(db, content.bid)

    if row:
        await crud.add_content(db, content)

        return {"message": "content added"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_content(content: ContentUpdate, db: AsyncSession = Depends(get_db)):
    row = await crud.get_content_by_id(db, content.id)

    if row:
        await crud.update_content(db, row, content)

        return {"message": "content updated"}

    raise HTTPException(404, "id not found")
    

@router.delete("/{id}")
async def delete_content(id: int, db: AsyncSession = Depends(get_db)):
    row = await crud.get_content_by_id(db, id)

    if row:
        remove_image(row.title)

        await crud.delete_content(db, row)

        return {"message": "content deleted"}

    raise HTTPException(404, "id not found")