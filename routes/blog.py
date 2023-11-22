from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
import database as DB

router = APIRouter()

class BlogAdd(BaseModel):
    title:       str
    category_id: int

class BlogUpdate(BaseModel):
    id:          int
    title:       str
    category_id: int

class BlogDelete(BaseModel):
    id: int

@router.get("/")
async def get_blogs():
    blogList = []
    blogs = await DB.get_blogs()
    for blog in blogs:
        blogList.append({
            "id":          blog[0],
            "title":       blog[1],
            "category_id": blog[2],
        })
    return {"blog": blogList}

@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_blog(blog: BlogAdd):
    await DB.add_blog(blog.title, blog.category_id)
    return {"blog": blog}

@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_blog(blog: BlogUpdate):
    row = await DB.get_blog(blog.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.update_blog(blog.id, blog.title, blog.category_id)
    return {"message": "blog updated"}

@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_blog(blog: BlogDelete):
    row = await DB.get_blog(blog.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.delete_blog(blog.id)
    return {"message": "blog deleted"}