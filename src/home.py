from fastapi                import APIRouter, Request, HTTPException, Depends
from fastapi.templating     import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.database           import get_db
from src.utils              import *
from src.config             import *
import src.crud             as crud


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_page(
    request: Request, 
    db:      AsyncSession = Depends(get_db)
):
    categories = []

    categories = await crud.get_all_categories(db)

    return templates.TemplateResponse("index.html", {
        "request":    request,
        "title":      "Категории",
        "url":        URL,
        "index":      1,
        "categories": categories,
    })


@router.get("/{category}")
async def blog_page(
    request:  Request, 
    category: str, 
    db:       AsyncSession = Depends(get_db)
):
    category = remove_dash(category)

    row = await crud.get_category_by_title(db, category)

    if row:
        blogs = await crud.get_all_blogs_by_cid(db, row.id)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   category,
            "url":     URL,
            "index":   2,
            "blogs":   blogs,
        })

    raise HTTPException(404, "Not found")


@router.get("/{category}/{blog}")
async def content_page(
    request:  Request, 
    category: str, 
    blog:     int, 
    db:       AsyncSession = Depends(get_db)
):
    category = remove_dash(category)

    db_category = await crud.get_category_by_title(db, category)
    db_blog     = await crud.get_blog_by_id(db, blog)

    if db_category and db_blog:
        contents = await crud.get_all_contents_by_bid(db, db_blog.id)

        date = format_date(db_blog.date)
        body = create_body(contents)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   db_blog.title,
            "url":     URL,
            "date":    date,
            "index":   3,
            "body":    body,
        })

    raise HTTPException(404, "Not found")
