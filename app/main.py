from fastapi                 import FastAPI, Depends
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.auth.jwt_bearer     import JwtBearer

from app.routers.user        import router as user_router
from app.routers.category    import router as category_router
from app.routers.blog        import router as blog_router
from app.routers.content     import router as content_router
from app.routers.image       import router as image_router
from app.routers.logs        import router as logs_router
from app.home                import router as home_router
from app.config              import *

import os
import logging


os.makedirs("static", exist_ok=True)

logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

app = FastAPI(docs_url=DOCS_URL, redoc_url=None)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount(path="/images",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

app.include_router(home_router,                                tags=["Home"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JwtBearer())])
app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"],     dependencies=[Depends(JwtBearer())])
app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"],  dependencies=[Depends(JwtBearer())])
app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"],    dependencies=[Depends(JwtBearer())])
app.include_router(logs_router,     prefix="/api/v1/logs",     tags=["Logs"],     dependencies=[Depends(JwtBearer())])


# app.include_router(category_router, prefix="/api/v1/category", tags=["Category"])
# app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"])
# app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"])
# app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"])
# app.include_router(logs_router,     prefix="/api/v1/logs",     tags=["Logs"])
# cd desktop/backend/fastapi/test2 & venv\scripts\activate
# uvicorn app.main:app --reload