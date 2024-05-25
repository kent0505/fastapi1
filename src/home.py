from fastapi            import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from src.core.config    import settings
from src.core.utils     import *
from src.core.models    import *


router = APIRouter()
templates = Jinja2Templates(directory=settings.templates)


async def db_get_all_categories(db: AsyncSession) -> List[Category]:
    categories = await db.scalars(select(Category).order_by(desc(Category.index)))
    return list(categories)
async def db_get_category_by_title(db: AsyncSession, title: str) -> Category | None:
    category = await db.scalar(select(Category).filter(Category.title == title))
    return category
async def db_get_all_blogs_by_cid(db: AsyncSession, cid: int) -> List[Blog]:
    blogs = await db.scalars(select(Blog).filter(Blog.cid == cid).order_by(desc(Blog.index)))
    return list(blogs)
async def db_get_blog_by_bid(db: AsyncSession, bid: int) -> Blog | None:
    blog = await db.scalar(select(Blog).filter(Blog.id == bid))
    return blog
async def db_get_blog_by_id(db: AsyncSession, id: int) -> Blog | None:
    blog = await db.scalar(select(Blog).filter(Blog.id == id))
    return blog
async def db_get_all_contents_by_bid(db: AsyncSession, bid: int) -> List[Content]:
    contents = await db.scalars(select(Content).filter(Content.bid == bid).order_by(desc(Content.index)))
    return list(contents)


@router.get("/")
@limiter.limit(settings.limit)
async def home_page(
    request: Request, 
    db:      AsyncSession = Depends(db_helper.get_db)
):
    categories = []

    categories = await db_get_all_categories(db)

    return templates.TemplateResponse("index.html", {
        "request":    request,
        "title":      "Категории",
        "url":        settings.url,
        "index":      1,
        "categories": categories,
    })


@router.get("/{category}")
@limiter.limit(settings.limit)
async def blog_page(
    request:  Request, 
    category: str, 
    db:       AsyncSession = Depends(db_helper.get_db)
):
    category = remove_dash(category)

    row = await db_get_category_by_title(db, category)

    if row:
        blogs = await db_get_all_blogs_by_cid(db, row.id)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   category,
            "url":     settings.url,
            "index":   2,
            "blogs":   blogs,
        })

    raise HTTPException(404, "Not found")


@router.get("/{title}/{id}")
@limiter.limit(settings.limit)
async def content_page(
    request: Request, 
    title:   str, 
    id:      int, 
    db:      AsyncSession = Depends(db_helper.get_db)
):
    title = remove_dash(title)

    category = await db_get_category_by_title(db, title)
    blog     = await db_get_blog_by_id(db, id)

    if category and blog:
        contents = await db_get_all_contents_by_bid(db, blog.id)

        date = format_date(blog.date)
        body = create_body(contents)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   blog.title,
            "url":     settings.url,
            "date":    date,
            "index":   3,
            "body":    body,
        })

    raise HTTPException(404, "Not found")
