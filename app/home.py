from fastapi            import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm     import Session
from sqlalchemy         import desc
from datetime           import datetime
from app.database       import *
from app.config         import *
import markdown
import logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_page(request: Request, db: Session = Depends(get_db)):
    categories = []

    categories = db.query(Category).order_by(desc(Category.index)).all()
    
    return templates.TemplateResponse("index.html", {
        "request":    request,
        "title":      "MYCHIMERA - Категории",
        "index":      1,
        "url":        URL,
        "categories": categories,
    })


@router.get("/{category}")
async def blogs_page(request: Request, category: str, db: Session = Depends(get_db)):
    category = category.replace("-", " ")

    blogs = []

    row = db.query(Category).filter(Category.title == category).first()

    if row:
        blogs = db.query(Blog).filter(Blog.category_id == row.id).order_by(desc(Blog.index)).all()

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
    
    db_category = db.query(Category).filter(Category.title == category).first()
    db_blog = db.query(Blog).filter(Blog.id == blog).first()

    if db_category and db_blog:
        contents = db.query(Content).filter(Content.blog_id == db_blog.id).order_by(desc(Content.index)).all()

        date = datetime.fromtimestamp(db_blog.date).strftime('%d.%m.%Y')

        text = ""

        for content in contents:
            if content.image == 0:
                text += f"{content.title}<br><br>"
            else:
                text += f"![]({URL}/images/{content.title})<br><br>"

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