from fastapi            import APIRouter, Request
from fastapi.templating import Jinja2Templates
import database as DB
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home_page(request: Request):
    await DB.create_tables()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "name":    config.name,
        "surname": config.surname,
    })