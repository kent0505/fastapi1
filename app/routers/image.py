from fastapi             import APIRouter, UploadFile, HTTPException, Form, Depends
from app.auth.jwt_bearer import JwtBearer
from sqlalchemy.orm      import Session
from app.database        import *
import time
import os

router = APIRouter(dependencies=[Depends(JwtBearer())])

@router.post("/")
async def upload_file(file: UploadFile, blog_id: int = Form(), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(400, "file not found")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "only image files are allowed")

    row = db.query(Blog).filter(Blog.id == blog_id).first()

    if row:
        unique_filename = f"{int(time.time())}.{file.filename.split('.')[-1]}"
        file_name =       os.path.join("static", unique_filename)

        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())
        
        db.add(Content(title=unique_filename, image=1, blog_id=blog_id))
        db.commit()

        return {"message": "image uploaded successfully"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_file(file: UploadFile, id: int = Form(), db: Session = Depends(get_db)):
    row = db.query(Content).filter(Content.id == id).first()

    if row and row.image == 1:
        try:
            os.remove(f"static/{row.title}")
        except:
            print("not found")

        unique_filename = f"{int(time.time())}.{file.filename.split('.')[-1]}"
        file_name =       os.path.join("static", unique_filename)

        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())

        row.title = unique_filename
        db.commit()

        return {"message": "image updated successfully"}

    raise HTTPException(404, "id not found")