from fastapi               import APIRouter, Depends
from src2.core.jwt         import JwtBearer
from src2.api.logs         import router as logs_router
from src2.api.users        import router as users_router
from src2.api.notification import router as notification_router
from src2.api.category     import router as category_router
from src2.api.blog         import router as blog_router
from src2.api.content      import router as content_router
from src2.api.image        import router as image_router


router = APIRouter()
router.include_router(users_router,        prefix="/api/v1/users",    tags=["User"])
router.include_router(logs_router,         prefix="/api/v1/logs",     tags=["Log"],          dependencies=[Depends(JwtBearer())])
router.include_router(notification_router, prefix="/api/v1/firebase", tags=["Notification"], dependencies=[Depends(JwtBearer())])
router.include_router(category_router,     prefix="/api/v1/category", tags=["Category"],     dependencies=[Depends(JwtBearer())])
router.include_router(blog_router,         prefix="/api/v1/blog",     tags=["Blog"],         dependencies=[Depends(JwtBearer())])
router.include_router(content_router,      prefix="/api/v1/content",  tags=["Content"],      dependencies=[Depends(JwtBearer())])
router.include_router(image_router,        prefix="/api/v1/image",    tags=["Image"],        dependencies=[Depends(JwtBearer())])