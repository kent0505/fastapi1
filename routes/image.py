from fastapi         import APIRouter, UploadFile, HTTPException, Form, Depends
from datetime        import datetime
from auth.jwt_bearer import JwtBearer
import database as DB
import os

router = APIRouter()

@router.post("/", dependencies=[Depends(JwtBearer())])
async def upload_file(file: UploadFile, blog_id: str = Form()):
    if not file.filename:
        raise HTTPException(400, "file not found")
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "only image files are allowed")
        
    blog = await DB.get_blog(blog_id)
    if not blog:
        raise HTTPException(404, "id not found")
        
    timestamp =       int(datetime.now().timestamp())
    file_extension =  file.filename.split(".")[-1]
    unique_filename = f"{timestamp}.{file_extension}"
    file_name =       os.path.join("static", unique_filename)

    with open(file_name, "wb") as image_file:
        image_file.write(file.file.read())

    await DB.add_content(unique_filename, 1, blog_id)

    return {"message": "image uploaded successfully"}

@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_file(file: UploadFile, id: str = Form()):
    image = await DB.get_content(id)
    if not image or image[2] == 0:
        raise HTTPException(404, "id not found")
        
    timestamp =       int(datetime.now().timestamp())
    file_extension =  file.filename.split(".")[-1]
    unique_filename = f"{timestamp}.{file_extension}"
    file_name =       os.path.join("static", unique_filename)

    with open(file_name, "wb") as image_file:
        image_file.write(file.file.read())

    await DB.update_content(id, unique_filename)
    try:
        os.remove(f"static/{image[1]}")
    except:
        print("not found")

    return {"message": "image updated successfully"}
    

# background_tasks: BackgroundTasks, 
# background_tasks.add_task(ImageController.save_image, file, blog_id)