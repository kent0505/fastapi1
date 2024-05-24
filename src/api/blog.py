from fastapi         import APIRouter, HTTPException, Depends
from src.core.utils  import get_current_timestamp
from src.core.models import *


router = APIRouter()


class BlogAdd(BaseModel):
    title: str
    index: int
    cid:   int


class BlogUpdate(BaseModel):
    id:    int
    title: str
    index: int
    cid:   int


async def db_get_all_blogs(db: AsyncSession) -> List[Blog]:
    blogs = await db.scalars(select(Blog).order_by(desc(Blog.index)))
    return list(blogs)
async def db_get_all_blogs_by_cid(db: AsyncSession, cid: int) -> List[Blog]:
    blogs = await db.scalars(select(Blog).filter(Blog.cid == cid).order_by(desc(Blog.index)))
    return list(blogs)
async def db_get_blog_by_id(db: AsyncSession, id: int) -> Blog | None:
    blog = await db.scalar(select(Blog).filter(Blog.id == id))
    return blog
async def db_get_category_by_cid(db: AsyncSession, cid: int) -> Category | None:
    category = await db.scalar(select(Category).filter(Category.id == cid, Category.type == 0))
    return category
async def db_add_blog(db: AsyncSession, body: BlogAdd) -> None:
    db.add(Blog(
        title = body.title, 
        index = body.index,
        date  = get_current_timestamp(),
        cid   = body.cid,
    ))
    await db.commit()
async def db_update_blog(db: AsyncSession, blog: Blog, body: BlogUpdate) -> None:
    blog.title = body.title
    blog.index = body.index
    blog.date  = get_current_timestamp()
    blog.cid   = body.cid
    await db.commit()
async def db_delete_blog(db: AsyncSession, blog: Blog) -> None:
    await db.delete(blog)
    await db.commit()


@router.get("/")
async def get_blogs(
    db: AsyncSession = Depends(db_helper.get_db)
):
    blogList = []

    blogs = await db_get_all_blogs(db)

    for blog in blogs:
        blogList.append({
            "id":    blog.id,
            "title": blog.title,
            "index": blog.index,
            "date":  blog.date,
            "cid":   blog.cid,
        })

    return {"blog": blogList}


@router.post("/")
async def add_blog(
    body: BlogAdd, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    category = await db_get_category_by_cid(db, body.cid)

    if category:
        await db_add_blog(db, body)

        return {"message": "blog added"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_blog(
    body: BlogUpdate, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    blog = await db_get_blog_by_id(db, body.id)

    if blog:
        await db_update_blog(db, blog, body)

        return {"message": "blog updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_blog(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    blog = await db_get_blog_by_id(db, id)

    if blog:
        await db_delete_blog(db, blog)

        return {"message": "blog deleted"}

    raise HTTPException(404, "id not found")