from fastapi                 import FastAPI
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.home             import router as home_router
from routes.user             import router as user_router
from routes.category         import router as category_router
from routes.blog             import router as blog_router
from routes.content          import router as content_router
from routes.image            import router as image_router
import config
import uvicorn
import os

os.makedirs("static", exist_ok=True)

app = FastAPI()
app.mount("/images", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home_router,     prefix="",              tags=["Home"])
app.include_router(user_router,     prefix="/api/user",     tags=["Users"])
app.include_router(category_router, prefix="/api/category", tags=["Category"])
app.include_router(blog_router,     prefix="/api/blog",     tags=["Blog"])
app.include_router(content_router,  prefix="/api/content",  tags=["Content"])
app.include_router(image_router,    prefix="/api/upload",   tags=["Image"])
    
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# cd desktop/backend/fastapi/test2 & venv\scripts\activate
# uvicorn main:app --reload
# pip install -r requirements.txt
# venv\scripts\activate