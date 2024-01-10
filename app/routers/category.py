from fastapi             import APIRouter, HTTPException, Depends
from sqlalchemy.orm      import Session
from app.database        import get_db
from app.schemas         import *
import app.crud as crud
import logging


router = APIRouter()


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    categoriesList = []

    categories = await crud.get_all_categories(db)

    for category in categories:
        categoriesList.append({
            "id":    category.id,
            "title": category.title,
            "index": category.index,
            "type":  category.type
        })

    logging.info("GET 200 /api/v1/category/")
    return {"category": categoriesList}


@router.post("/")
async def add_category(category: CategoryAdd, db: Session = Depends(get_db)):
    await crud.add_category(db, category)

    logging.info("POST 200 /api/v1/category/")
    return {"message": "category added"}


@router.put("/")
async def update_category(category: CategoryUpdate, db: Session = Depends(get_db)):
    row = await crud.get_category_by_id(db, category.id)

    if row:
        await crud.update_category(db, row, category)

        logging.info("PUT 200 /api/v1/category/")
        return {"message": "category updated"}

    logging.error("PUT 404 /api/v1/category/ NOT FOUND")
    raise HTTPException(404, "id not found")


@router.delete("/")
async def delete_category(category: CategoryDelete, db: Session = Depends(get_db)):
    row = await crud.get_category_by_id(db, category.id)

    if row:
        await crud.delete_category(db, row)

        logging.info("DELETE 200 /api/v1/category/")
        return {"message": "category deleted"}
    
    logging.error("DELETE 200 /api/v1/category/ NOT FOUND")
    raise HTTPException(404, "id not found")