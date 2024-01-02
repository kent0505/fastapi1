from fastapi            import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm     import Session
from datetime           import datetime
from app.database       import get_db
from app.config         import *
import app.crud as DB
import markdown
import logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_page(request: Request, db: Session = Depends(get_db)):
    categories = []

    categories = DB.get_all_categories(db)
    
    return templates.TemplateResponse("index.html", {
        "request":    request,
        "title":      "Категории",
        "index":      1,
        "url":        URL,
        "categories": categories,
    })


@router.get("/{category}")
async def blogs_page(request: Request, category: str, db: Session = Depends(get_db)):
    category = category.replace("-", " ")

    blogs = []

    row = DB.get_category_by_title(db, category)

    if row:
        blogs = DB.get_all_blogs_by_category_id(db, row.id)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "title":   category,
            "index":   2,
            "url":     URL,
            "blogs":   blogs,
        })

    logging.warning("CATEGORY NOT FOUND")
    raise HTTPException(404, "Not found")


@router.get("/{category}/{blog}")
async def blogs_page(request: Request, category: str, blog: int, db: Session = Depends(get_db)):
    category = category.replace("-", " ")

    contents = []

    db_category = DB.get_category_by_title(db, category)
    db_blog = DB.get_blog_by_id(db, blog)

    if db_category and db_blog:
        contents = DB.get_all_contents_by_blog_id(db, db_blog.id)

        date = datetime.fromtimestamp(db_blog.date).strftime('%d.%m.%Y')

        text = ""

        for content in contents:
            if content.image == 0:
                text += f"{content.title}<br><br>"
            else:
                text += f"![]({URL}/images/{content.title}/)<br><br>"

        return templates.TemplateResponse("index.html", {
            "request":  request,
            "title":    db_blog.title,
            "date":     date,
            "index":    3,
            "url":      URL,
            "contents": markdown.markdown(text),
        })

    logging.warning("CATEGORY OR BLOG NOT FOUND")
    raise HTTPException(404, "Not found")