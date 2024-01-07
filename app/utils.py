from fastapi  import UploadFile
from datetime import datetime
import os, time, logging, bcrypt


def get_timestamp():
    return int(time.time())


def formatted_date(timestamp: int):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y')


def add_image(file: UploadFile):
    try:
        timestamp   = get_timestamp()
        format      = file.filename.split('.')[-1] # jpg/jpeg/png
        unique_name = f"{timestamp}.{format}"
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
    hashed = bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
    return hashed