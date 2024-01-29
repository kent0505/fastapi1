from fastapi                 import FastAPI, Depends
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.utils               import LogMiddleware, init
from src.auth.jwt_bearer     import JwtBearer
from src.home                import router as home_router
from src.routers.user        import router as user_router
from src.routers.category    import router as category_router
from src.routers.blog        import router as blog_router
from src.routers.content     import router as content_router
from src.routers.image       import router as image_router
from src.routers.logs        import router as logs_router
from src.config              import *

init()

app = FastAPI(docs_url=DOCS_URL, redoc_url=None)

app.mount(path="/images",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")
app.add_middleware(middleware_class=CORSMiddleware, allow_origins=ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(LogMiddleware)

app.include_router(home_router,                                tags=["Home"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JwtBearer())])
app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"],     dependencies=[Depends(JwtBearer())])
app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"],  dependencies=[Depends(JwtBearer())])
app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"],    dependencies=[Depends(JwtBearer())])
app.include_router(logs_router,     prefix="/api/v1/logs",     tags=["Logs"],     dependencies=[Depends(JwtBearer())])


# from fastapi.exceptions      import RequestValidationError
# app.add_exception_handler(RequestValidationError, validation_exception_handler)

# dependencies=[Depends(JwtBearer())]
# pip install -r requirements.txt
# cd Desktop/backend/fastapi/test2 && source venv/bin/activate
# uvicorn src.main:app --reload
# sudo lsof -t -i tcp:8000 | xargs kill -9