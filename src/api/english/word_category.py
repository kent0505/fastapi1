from fastapi         import APIRouter, HTTPException, Depends
from src.core.models import *


router = APIRouter()


class WordCategoryAdd(BaseModel):
    title: str
class WordCategoryUpdate(BaseModel):
    id:    int
    title: str


async def db_get_all_word_categories(db: AsyncSession) -> List[WordCategory]:
    word_categories = await db.scalars(select(WordCategory))
    return list(word_categories)
async def db_get_word_category_by_id(db: AsyncSession, id: int) -> WordCategory | None:
    word_category = await db.scalar(select(WordCategory).filter(WordCategory.id == id))
    return word_category
async def db_add_word_category(db: AsyncSession, body: WordCategoryAdd) -> None:
    db.add(WordCategory(title = body.title))
    await db.commit()
async def db_update_word_category(db: AsyncSession, word_category: WordCategory, body: WordCategoryUpdate) -> None:
    word_category.title = body.title
    await db.commit()
async def db_delete_word_category(db: AsyncSession, word_category: WordCategory) -> None:
    await db.delete(word_category)
    await db.commit()


@router.get("/")
async def get_word_categories(
    db:  AsyncSession = Depends(db_helper.get_db)
):
    wordsList = []

    words = await db_get_all_word_categories(db)

    for word in words:
        wordsList.append({
            "id":    word.id,
            "title": word.title,
        })

    return {"words": wordsList}


@router.post("/")
async def add_word_category(
    body: WordCategoryAdd, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    await db_add_word_category(db, body)

    return {"message": "word category added"}


@router.put("/")
async def update_word_category(
    body: WordCategoryUpdate, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    word_category = await db_get_word_category_by_id(db, body.id)

    if word_category:
        await db_update_word_category(db, word_category, body)

        return {"message": "word category updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_word_category(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    word_category = await db_get_word_category_by_id(db, id)

    if word_category:
        await db_delete_word_category(db, word_category)

        return {"message": "word category deleted"}

    raise HTTPException(404, "id not found")