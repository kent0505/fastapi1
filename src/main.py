from fastapi                 import FastAPI, Depends
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions      import RequestValidationError
from src.auth.jwt_bearer     import JwtBearer
from src.home                import router as home_router
from src.routers.user        import router as user_router
from src.routers.category    import router as category_router
from src.routers.blog        import router as blog_router
from src.routers.content     import router as content_router
from src.routers.image       import router as image_router
from src.routers.logs        import router as logs_router
from src.middleware.log      import *
from src.config              import *
import logging
import os


os.makedirs("static", exist_ok=True)
logging.basicConfig(filename=FILENAME, level=LEVEL, format=FORMAT, datefmt=DATEFMT)

app = FastAPI(docs_url=DOCS_URL, redoc_url=None)

app.mount(path="/images",    app=StaticFiles(directory="static"),    name="static")
app.mount(path="/templates", app=StaticFiles(directory="templates"), name="templates")
app.add_middleware(middleware_class=CORSMiddleware, allow_origins=ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(LogMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(home_router,                                tags=["Home"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["User"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"], dependencies=[Depends(JwtBearer())])
app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"],     dependencies=[Depends(JwtBearer())])
app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"],  dependencies=[Depends(JwtBearer())])
app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"],    dependencies=[Depends(JwtBearer())])
app.include_router(logs_router,     prefix="/api/v1/logs",     tags=["Logs"],     dependencies=[Depends(JwtBearer())])

# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request: Request, exc):
#     raise HTTPException(422, "Validation error")

# @app.middleware("http")
# async def get_request_url(request: Request, call_next):
#     url = str(request.url).replace(URL, '')
#     print(f"{request.method} {url}")
#     response = await call_next(request)
#     return response

# dependencies=[Depends(JwtBearer())]
# pip install -r requirements.txt
# cd Desktop/backend/fastapi/test2 && source venv/bin/activate
# uvicorn src.main:app --reload
# sudo lsof -t -i tcp:8000 | xargs kill -9