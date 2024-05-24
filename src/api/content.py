from fastapi         import APIRouter, HTTPException, Depends
from src.core.utils  import remove_image
from src.core.models import *

router = APIRouter()


class ContentAdd(BaseModel):
    title: str
    index: int
    bid:   int


class ContentUpdate(BaseModel):
    id:    int
    title: str
    index: int


async def db_get_all_contents(db: AsyncSession, offset: int) -> List[Content]:
    contents = await db.scalars(select(Content).order_by(Content.bid).offset(offset).limit(50))
    return list(contents)
async def db_get_all_contents_by_bid(db: AsyncSession, bid: int) -> List[Content]:
    contents = await db.scalars(select(Content).filter(Content.bid == bid).order_by(desc(Content.index)))
    return list(contents)
async def db_get_content_by_id(db: AsyncSession, id: int) -> Content | None:
    content = await db.scalar(select(Content).filter(Content.id == id))
    return content
async def db_get_blog_by_bid(db: AsyncSession, bid: int) -> Blog | None:
    blog = await db.scalar(select(Blog).filter(Blog.id == bid))
    return blog
async def db_add_content(db: AsyncSession, body: ContentAdd):
    db.add(Content(
        title = body.title,
        index = body.index,
        image = 0, 
        bid   = body.bid
    ))
    await db.commit()
async def db_update_content(db: AsyncSession, content: Content, body: ContentUpdate):
    content.title = body.title
    content.index = body.index
    await db.commit()
async def db_delete_content(db: AsyncSession, content: Content):
    await db.delete(content)
    await db.commit()


@router.get("/")
async def get_contents(
    bid:    int,
    offset: int,
    db:     AsyncSession = Depends(db_helper.get_db)
):
    contentList = []

    if bid == 0:
        contents = await db_get_all_contents(db, offset)
    else:
        contents = await db_get_all_contents_by_bid(db, bid)

    for content in contents:
        contentList.append({
            "id"   : content.id,
            "title": content.title,
            "index": content.index,
            "image": content.image,
            "bid"  : content.bid
        })

    return {"content": contentList}


@router.post("/")
async def add_content(
    body: ContentAdd, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    blog = await db_get_blog_by_bid(db, body.bid)

    if blog:
        await db_add_content(db, body)

        return {"message": "content added"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_content(
    body: ContentUpdate, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    content = await db_get_content_by_id(db, body.id)

    if content:
        await db_update_content(db, content, body)

        return {"message": "content updated"}

    raise HTTPException(404, "id not found")
    

@router.delete("/{id}")
async def delete_content(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    content = await db_get_content_by_id(db, id)

    if content:
        remove_image(content.title)

        await db_delete_content(db, content)

        return {"message": "content deleted"}

    raise HTTPException(404, "id not found")


# async def db_get_all_contents(db: AsyncSession) -> List[Content]:
#     contents = await db.scalars(select(Content).order_by(Content.bid))
#     return list(contents)