from fastapi         import APIRouter, HTTPException, Depends
from src.core.models import *


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


async def db_get_all_categories(db: AsyncSession) -> List[Category]:
    categories = await db.scalars(select(Category).order_by(desc(Category.index)))
    return list(categories)
async def db_get_category_by_id(db: AsyncSession, id: int) -> Category | None:
    category = await db.scalar(select(Category).filter(Category.id == id))
    return category 
async def db_get_category_by_title(db: AsyncSession, title: str) -> Category | None:
    category = await db.scalar(select(Category).filter(Category.title == title))
    return category
async def db_add_category(db: AsyncSession, body: CategoryAdd) -> None:
    db.add(Category(
        title = body.title, 
        index = body.index, 
        type  = body.type,
    ))
    await db.commit()
async def db_update_category(db: AsyncSession, category: Category, body: CategoryUpdate) -> None:
    category.title = body.title
    category.index = body.index
    category.type  = body.type
    await db.commit()
async def db_delete_category(db: AsyncSession, category: Category) -> None:
    await db.delete(category)
    await db.commit()


@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(db_helper.get_db)
):
    categoriesList = []

    categories = await db_get_all_categories(db)

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
    body: CategoryAdd, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    await db_add_category(db, body)

    return {"message": "category added"}


@router.put("/")
async def update_category(
    body: CategoryUpdate, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    category = await db_get_category_by_id(db, body.id)

    if category:
        await db_update_category(db, category, body)

        return {"message": "category updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_category(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    category = await db_get_category_by_id(db, id)

    if category:
        await db_delete_category(db, category)

        return {"message": "category deleted"}

    raise HTTPException(404, "id not found")