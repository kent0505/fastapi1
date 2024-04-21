from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database           import get_db
from src.schemas            import *
from src.utils              import *
import src.crud             as crud


router = APIRouter()


@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    categoriesList = []

    categories = await crud.get_all_categories(db)

    for category in categories:
        categoriesList.append({
            "id":    category.id,
            "title": category.title,
            "index": category.index,
            "type":  category.type
        })

    return {"category": categoriesList}


@router.post("/")
async def add_category(
    category: CategoryAdd, 
    db:       AsyncSession = Depends(get_db)
):
    await crud.add_category(db, category)

    return {"message": "category added"}


@router.put("/")
async def update_category(
    category: CategoryUpdate, 
    db:       AsyncSession = Depends(get_db)
):
    row = await crud.get_category_by_id(db, category.id)

    if row:
        await crud.update_category(db, row, category)

        return {"message": "category updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_category(
    id: int, 
    db: AsyncSession = Depends(get_db)
):
    row = await crud.get_category_by_id(db, id)

    if row:
        await crud.delete_category(db, row)

        return {"message": "category deleted"}

    raise HTTPException(404, "id not found")