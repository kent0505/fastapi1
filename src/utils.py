from fastapi                   import UploadFile, Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing                    import List
from http                      import HTTPStatus
from datetime                  import datetime
from src.database              import Content
import os
import time
import logging
import bcrypt
import markdown


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


def init():
    os.makedirs("static", exist_ok=True)
    logging.basicConfig(
        filename="logfile.log", 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S" # 29-01-2024 14:19:28
    )
    logging.info("STARTUP")


def get_timestamp():
    return int(time.time())


def format_date(timestamp: int):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y') # 29.01.2024


def remove_dash(data: str):
    return data.replace("-", " ")


def create_body(request: Request, contents: List[Content]):
    body = ""
    for content in contents:
        if content.image == 0:
            body += f"{content.title}<br><br>"
        else:
            body += f"![]({request.base_url}images/{content.title}/)<br><br>"
    body = markdown.markdown(body)
    return body


def add_image(file: UploadFile):
    try:
        timestamp   = get_timestamp()              # 1706520261
        format      = file.filename.split('.')[-1] # jpg/jpeg/png
        unique_name = f"{timestamp}.{format}"      # 1706520261.png
        file_name   = os.path.join("static", unique_name)

        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())

        logging.warning("IMAGE ADDED")
        return unique_name
    except Exception as e:
        try:
            logging.warning(e)
        finally:
            logging.warning("IMAGE NOT ADDED")


def remove_image(title: str):
    try:
        os.remove(f"static/{title}")
        logging.warning("IMAGE REMOVED")
    except:
        logging.warning("IMAGE NOT FOUND")


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
    return hashed


def check_password(password1: str, password2: str):
    try:
        hashed = bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
        return hashed
    except:
        return False


# def validation_exception_handler(request: Request, exc):
#     raise HTTPException(422, "Validation error")