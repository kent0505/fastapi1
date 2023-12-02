from fastapi             import APIRouter, HTTPException, Depends
from pydantic            import BaseModel
from sqlalchemy          import desc
from sqlalchemy.orm      import Session
from app.auth.jwt_bearer import JwtBearer
from app.database        import *

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

    categories = db.query(Category).order_by(desc(Category.index)).all()

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
    db.add(Category(title=category.title, index=0, type=category.type))
    db.commit()

    return {"message": "category added"}


@router.put("/", dependencies=[Depends(JwtBearer())])
async def update_category(category: CategoryUpdate, db: Session = Depends(get_db)):
    row = db.query(Category).filter(Category.id == category.id).first()

    if row:
        row.title = category.title
        row.index = category.index
        row.type =  category.type
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