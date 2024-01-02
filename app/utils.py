from fastapi import UploadFile
import os
import time
import logging
import bcrypt

def add_image(file: UploadFile):
    timestamp =   int(time.time())
    format =      file.filename.split('.')[-1] # jpg/jpeg/png
    unique_name = f"{timestamp}.{format}"
    file_name =   os.path.join("static", unique_name)

    with open(file_name, "wb") as image_file:
        image_file.write(file.file.read())

    return unique_name

def remove_image(title: str):
    try:
        os.remove(f"static/{title}")
    except:
        logging.error("IMAGE NOT FOUND")

def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
    return hashed

def check_password(password1: str, password2: str):
    hashed = bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
    return hashed