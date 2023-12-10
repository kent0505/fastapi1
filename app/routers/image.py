from fastapi             import APIRouter, UploadFile, HTTPException, Form, Depends
from app.auth.jwt_bearer import JwtBearer
from sqlalchemy.orm      import Session
from app.database        import *
import time
import os

router = APIRouter(dependencies=[Depends(JwtBearer())])


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
        print("not found")


@router.post("/")
async def upload_file(
        file:    UploadFile, 
        index:   int     = Form(), 
        blog_id: int     = Form(), 
        db:      Session = Depends(get_db)
    ):

    if not file.filename:
        raise HTTPException(400, "file not found")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "only image files are allowed")

    row = db.query(Blog).filter(Blog.id == blog_id).first()

    if row:
        unique_filename = add_image(file)
        
        db.add(Content(
            title   = unique_filename,
            index   = index,
            image   = 1, 
            blog_id = blog_id
        ))
        db.commit()

        return {"message": "image uploaded successfully"}

    raise HTTPException(404, "id not found")


@router.put("/")
async def update_file(
        file:  UploadFile, 
        id:    int     = Form(), 
        index: int     = Form(), 
        db:    Session = Depends(get_db)
    ):

    row = db.query(Content).filter(Content.id == id).first()

    if row:
        remove_image(row.title)

        unique_name = add_image(file)

        row.title = unique_name
        row.index = index
        row.image = 1
        db.commit()

        return {"message": "image updated successfully"}

    raise HTTPException(404, "id not found")