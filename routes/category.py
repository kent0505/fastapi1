from fastapi         import APIRouter, HTTPException, Depends
from pydantic        import BaseModel
from auth.jwt_bearer import JwtBearer
from sqlalchemy.orm  import Session
from database        import *

router = APIRouter()

class CategoryAdd(BaseModel):
    title: str

class CategoryUpdate(BaseModel):
    id:    int
    title: str

class CategoryDelete(BaseModel):
    id: int


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    categoriesList = []

    categories = db.query(Category).all()

    for category in categories:
        categoriesList.append({
            "id":    category.id,
            "title": category.title,
        })

    return {"category": categoriesList}


@router.post("/")
async def add_category(category: CategoryAdd, db: Session = Depends(get_db)):
    db.add(Category(title=category.title))
    db.commit()

    return {"message": "category added"}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_category(category: CategoryUpdate, db: Session = Depends(get_db)):
    row = db.query(Category).filter(Category.id == category.id).first()

    if row:
        row.title = category.title
        db.commit()

        return {"message": "category updated"}

    raise HTTPException(404, "id not found")


@router.delete("/", dependencies=[Depends(JwtBearer())])
async def delete_category(category: CategoryDelete, db: Session = Depends(get_db)):
    row = db.query(Category).filter(Category.id == category.id).first()

    if row:
        db.delete(row)
        db.commit()

        return {"message": "category deleted"}
    
    raise HTTPException(404, "id not found")