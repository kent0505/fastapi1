from fastapi                   import APIRouter, Depends
from src.core.jwt              import JwtBearer
from src.api.blog.users        import router as users_router
from src.api.blog.logs         import router as logs_router
from src.api.blog.notification import router as notification_router
from src.api.blog.category     import router as category_router
from src.api.blog.blog         import router as blog_router
from src.api.blog.content      import router as content_router
from src.api.blog.image        import router as image_router
from src.home                  import router as home_router


router = APIRouter()
router.include_router(home_router,                                    tags=["Home"],         include_in_schema=False)
router.include_router(users_router,        prefix="/api/v1/user",     tags=["User"])
router.include_router(logs_router,         prefix="/api/v1/logs",     tags=["Log"],          dependencies=[Depends(JwtBearer())])
router.include_router(notification_router, prefix="/api/v1/firebase", tags=["Notification"], dependencies=[Depends(JwtBearer())])
router.include_router(category_router,     prefix="/api/v1/category", tags=["Category"],     dependencies=[Depends(JwtBearer())])
router.include_router(blog_router,         prefix="/api/v1/blog",     tags=["Blog"],         dependencies=[Depends(JwtBearer())])
router.include_router(content_router,      prefix="/api/v1/content",  tags=["Content"],      dependencies=[Depends(JwtBearer())])
router.include_router(image_router,        prefix="/api/v1/image",    tags=["Image"],        dependencies=[Depends(JwtBearer())])