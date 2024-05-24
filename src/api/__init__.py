from fastapi              import APIRouter, Depends
from src.core.jwt         import JwtBearer
from src.home             import router as home_router
from src.api.logs         import router as logs_router
from src.api.users        import router as users_router
from src.api.notification import router as notification_router
from src.api.category     import router as category_router
from src.api.blog         import router as blog_router
from src.api.content      import router as content_router
from src.api.image        import router as image_router


router = APIRouter()
router.include_router(home_router,                                    tags=["Home"])
router.include_router(logs_router,         prefix="/api/v1/logs",     tags=["Log"])
router.include_router(users_router,        prefix="/api/v1/users",    tags=["User"])
router.include_router(notification_router, prefix="/api/v1/firebase", tags=["Notification"])
router.include_router(category_router,     prefix="/api/v1/category", tags=["Category"])
router.include_router(blog_router,         prefix="/api/v1/blog",     tags=["Blog"])
router.include_router(content_router,      prefix="/api/v1/content",  tags=["Content"])
router.include_router(image_router,        prefix="/api/v1/image",    tags=["Image"])
# , dependencies=[Depends(JwtBearer())]