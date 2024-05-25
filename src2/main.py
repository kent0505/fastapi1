from fastapi                 import FastAPI
from fastapi.responses       import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles     import StaticFiles
from src2.core.utils         import LogMiddleware, lifespan
from src2.core.config        import settings
from src2.api                import router as api_router


app = FastAPI(
    lifespan               = lifespan,
    default_response_class = ORJSONResponse, 
    swagger_ui_parameters  = settings.swagger_ui,
)
app.add_middleware(LogMiddleware)
app.add_middleware(
    middleware_class  = CORSMiddleware, 
    allow_origins     = settings.allow_origins, 
    allow_credentials = settings.allow_creds, 
    allow_methods     = settings.allow_methods, 
    allow_headers     = settings.allow_headers,
)
app.mount(
    app  = StaticFiles(directory=settings.static),
    path = settings.static_path,
)
app.mount(
    app  = StaticFiles(directory=settings.templates),
    path = settings.templates_path,
)
app.include_router(api_router)


# pip install -r requirements.txt
# cd Desktop/admin/test2 && source venv/bin/activate
# uvicorn src2.main:app --reload
# sudo lsof -t -i tcp:8000 | xargs kill -9