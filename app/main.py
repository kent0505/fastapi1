from fastapi                 import FastAPI, WebSocket
from fastapi.staticfiles     import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user        import router as user_router
from app.routers.category    import router as category_router
from app.routers.blog        import router as blog_router
from app.routers.content     import router as content_router
from app.routers.image       import router as image_router
from app.home                import router as home_router
from app.config              import *
import os

os.makedirs("static", exist_ok=True)

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

websocket_clients = set()
messages = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    websocket_clients.add(websocket)

    try:
        while True:
            text = await websocket.receive_text()

            messages.append(text)

            for client in websocket_clients:
                # for message in messages:
                #     print(message)
                await client.send_json({"message": messages})
    except Exception as e:
        print(e)
    finally:
        websocket_clients.remove(websocket)


app.include_router(home_router,     prefix="",                 tags=["Home"])
app.include_router(user_router,     prefix="/api/v1/user",     tags=["Users"])
app.include_router(category_router, prefix="/api/v1/category", tags=["Category"])
app.include_router(blog_router,     prefix="/api/v1/blog",     tags=["Blog"])
app.include_router(content_router,  prefix="/api/v1/content",  tags=["Content"])
app.include_router(image_router,    prefix="/api/v1/upload",   tags=["Image"])