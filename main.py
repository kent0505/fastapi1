from fastapi                 import FastAPI
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.home             import router as home_router
from routes.user             import router as user_router
from routes.category         import router as category_router
from routes.blog             import router as blog_router
from routes.content          import router as content_router
from routes.image            import router as image_router
from database                import *
import config
import os

os.makedirs("static", exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=config.DOCS_URL, redoc_url=None)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount(path="/images",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")

app.include_router(home_router,     prefix="",                 tags=["Home"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["Users"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"])
app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"])
app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"])
app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"])