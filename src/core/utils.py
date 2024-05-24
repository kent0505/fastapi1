from fastapi                   import FastAPI, UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from http                      import HTTPStatus
from contextlib                import asynccontextmanager
from dotenv                    import load_dotenv
from datetime                  import datetime
from firebase_admin            import credentials
from src.core.models           import db_helper, Base, Content, List
from src.core.config           import settings
import firebase_admin
import markdown
import logging
import time
import os


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        method      = request.method                                       # POST
        url_path    = str(request.url).replace(str(request.base_url), '/') # /api/v1/category/
        status_code = response.status_code                                 # 404
        code_desc   = HTTPStatus(status_code).phrase                       # Not Found

        msg = f"{method} {url_path} {status_code} {code_desc}"

        if "200 OK" in msg:
            logging.info(msg)
        else:
            logging.error(msg)
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()

    os.makedirs(".env",          exist_ok=True)
    os.makedirs("firebase.json", exist_ok=True)

    logging.basicConfig(
        filename = settings.log_filename, 
        level    = settings.log_level, 
        format   = settings.log_format,
        datefmt  = settings.log_datefmt,
    )
    logging.info("STARTUP")

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # shutdown
    logging.info("SHUTDOWN")
    await db_helper.dispose()


def get_current_timestamp() -> int:
   return int(time.time())


def format_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(settings.date_format)


def remove_dash(data: str) -> str:
    return data.replace("-", " ")


def create_body(contents: List[Content]) -> str:
    body = ""
    for content in contents:
        if content.image == 0:
            body += f"{content.title}<br><br>"
        else:
            body += f"![]({settings.url}/{settings.static}/{content.title}/)<br><br>"
    body = markdown.markdown(body)
    return body


def check_picked_file(file:  UploadFile) -> bool:
    if file.filename and str(file.content_type).startswith("image/"):
        return True
    else:
        return False


def remove_image(title: str) -> None:
    try:
        os.remove(f"{settings.static}/{title}")
        logging.warning("IMAGE REMOVED")
    except:
        logging.warning("IMAGE NOT FOUND")


def add_image(file: UploadFile) -> str:
    try:
        timestamp   = get_current_timestamp()           # 1706520261
        format      = str(file.filename).split('.')[-1] # jpg/jpeg/png
        unique_name = f"{timestamp}.{format}"           # 1706520261.png
        file_name   = os.path.join(settings.static, unique_name)

        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())

        logging.warning("IMAGE ADDED")
        return unique_name
    except Exception as e:
        try:
            logging.warning(e)
        finally:
            logging.warning("IMAGE NOT ADDED")
            return ""


def check_firebase_file() -> bool:
    if os.path.exists(settings.firebase_json):
        try:
            firebase_cred = credentials.Certificate(settings.firebase_json)
            firebase_admin.initialize_app(firebase_cred)
            return False
        except:
            return True
    else:
        return True