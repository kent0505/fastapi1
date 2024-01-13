from fastapi    import APIRouter, UploadFile, HTTPException
from app.config import *
import os, logging


router = APIRouter()


@router.get("/{password}")
async def admin_status(password: str):
    if password == PASSWORD:
        with open("test.txt", "r") as file:
            status = file.read()
        
        logging.warning(f"STATUS {status}")

        logging.info(f"GET 200 /api/v1/admin/{password}/")
        return {"message": f"{status}"}
    
    logging.error(f"GET 404 /api/v1/admin/{password}/")
    raise HTTPException(404, "Not found")


@router.post("/{password}")
async def admin_image_upload(password: str, file: UploadFile):
    if password == PASSWORD and file.filename == FILENAME:
        with open("test.txt", "w") as txtfile:
            txtfile.write("0")
        logging.warning("STATUS 0")

        try:
            file_name = os.path.join("static", file.filename)

            with open(file_name, "wb") as image_file:
                image_file.write(file.file.read())

            logging.warning("IMAGE ADDED")

            logging.info(f"POST 200 /api/v1/admin/{password}/")
            return {"message": "image uploaded successfully"}
        except Exception as e:
            logging.error(f"POST 400 /api/v1/admin/{password}/")
            raise HTTPException(400, f"Error {e}")

    logging.info(f"POST 400 /api/v1/admin/{password}/")
    raise HTTPException(400, "Error 2")


@router.get("/{password}/{status}")
async def change_admin_status(password: str, status: int):
    if password == PASSWORD:
        with open("test.txt", "w") as file:
            file.write(f"{status}")
        
        logging.warning(f"STATUS {status}")

        logging.info(f"GET 200 /api/v1/admin/{password}/{status}/")
        return {"message": f"{status}"}

    logging.error(f"GET 404 /api/v1/admin/{password}/{status}/")
    raise HTTPException(404, "Not found")