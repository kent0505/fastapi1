from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import get_db
import app.crud as DB

router = APIRouter()

class CategoryAdd(BaseModel):
    title: str
    index: int
    type:  int

class CategoryUpdate(BaseModel):
    id:    int
    title: str
    index: int
    type:  int

class CategoryDelete(BaseModel):
    id: int


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    categoriesList = []

    categories = DB.get_all_categories(db)

    for category in categories:
        categoriesList.append({
            "id":    category.id,
            "title": category.title,
            "index": category.index,
            "type":  category.type
        })

    return {"category": categoriesList}


@router.post("/", dependencies=[Depends(JwtBearer())])
async def add_category(category: CategoryAdd, db: Session = Depends(get_db)):
    DB.add_category(db, category.title, category.index, category.type)

    return {"message": "category added"}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_category(category: CategoryUpdate, db: Session = Depends(get_db)):
    row = DB.get_category_by_id(db, category.id)

    if row:
        DB.update_category(db, row, category.title, category.index, category.type)

        return {"message": "category updated"}

    raise HTTPException(404, "id not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_category(category: CategoryDelete, db: Session = Depends(get_db)):
    row = DB.get_category_by_id(db, category.id)

    if row:
        DB.delete_category(db, row)

        return {"message": "category deleted"}
    
    raise HTTPException(404, "id not found")