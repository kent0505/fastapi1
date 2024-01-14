from fastapi                import APIRouter, Request, HTTPException, Depends
from fastapi.templating     import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database           import get_db
from app.utils              import *
from app.config             import *

import app.crud as crud
import markdown


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_page(request: Request, db: AsyncSession = Depends(get_db)):
    categories = []

    categories = await crud.get_all_categories(db)

    log("GET 200 /")
    return templates.TemplateResponse("index.html", {
        "request":    request,
        "title":      "Категории",
        "index":      1,
        "url":        URL,
        "categories": categories,
    })


@router.get("/{category}")
async def blogs_page(request: Request, category: str, db: AsyncSession = Depends(get_db)):
    category = category.replace("-", " ")

    blogs = []

    row = await crud.get_category_by_title(db, category)

    if row:
        blogs = await crud.get_all_blogs_by_cid(db, row.id)

        log(f"GET 200 /{category}/")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   category,
            "index":   2,
            "url":     URL,
            "blogs":   blogs,
        })

    log(f"GET 404 /{category}/")
    raise HTTPException(404, "Not found")


@router.get("/{category}/{blog}")
async def blogs_page(request: Request, category: str, blog: int, db: AsyncSession = Depends(get_db)):
    category = category.replace("-", " ")

    contents = []

    db_category = await crud.get_category_by_title(db, category)
    db_blog = await crud.get_blog_by_id(db, blog)

    if db_category and db_blog:
        contents = await crud.get_all_contents_by_bid(db, db_blog.id)

        date = formatted_date(db_blog.date)

        body = ""

        for content in contents:
            if content.image == 0:
                body += f"{content.title}<br><br>"
            else:
                body += f"![]({URL}/images/{content.title})<br><br>"

        log(f"GET 200 /{category}/{blog}/")
        return templates.TemplateResponse("index.html", {
            "request":  request,
            "title":    db_blog.title,
            "date":     date,
            "index":    3,
            "url":      URL,
            "contents": markdown.markdown(body),
        })

    log(f"GET 404 /{category}/{blog}/")
    raise HTTPException(404, "Not found")