from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
import database as DB

router = APIRouter()

class CategoryAdd(BaseModel):
    title: str

class CategoryUpdate(BaseModel):
    id:    int
    title: str

class CategoryDelete(BaseModel):
    id: int

@router.get("/")
async def get_categories():
    categoriesList = []
    categories = await DB.get_categories()
    for category in categories:
        categoriesList.append({
            "id":    category[0],
            "title": category[1],
        })
    return {"category": categoriesList}

@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_category(category: CategoryAdd):
    await DB.add_category(category.title)
    return {"category": category}
    
@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_category(category: CategoryUpdate):
    row = await DB.get_category(category.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.update_category(category.id, category.title)
    return {"category": "category updated"}
    
@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_category(category: CategoryDelete):
    row = await DB.get_category(category.id)
    if not row:
        raise HTTPException(404, "id not found")
    await DB.delete_category(category.id)
    return {"category": "category deleted"}