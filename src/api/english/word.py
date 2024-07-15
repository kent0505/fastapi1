from fastapi         import APIRouter, HTTPException, Depends
from src.core.models import *


router = APIRouter()


class WordAdd(BaseModel):
    en:  str
    ru:  str
    cid: int
class WordUpdate(BaseModel):
    id:  int
    en:  str
    ru:  str
    cid: int


async def db_get_all_words(db: AsyncSession, cid: int) -> List[Word]:
    words = await db.scalars(select(Word).filter(Word.cid == cid))
    return list(words)
async def db_get_word_by_id(db: AsyncSession, id: int) -> Word | None:
    word = await db.scalar(select(Word).filter(Word.id == id))
    return word
async def db_get_word_by_cid(db: AsyncSession, cid: int) -> Word | None:
    word = await db.scalar(select(WordCategory).filter(WordCategory.id == cid))
    return word
async def db_add_word(db: AsyncSession, body: WordAdd) -> None:
    db.add(Word(
        en  = body.en, 
        ru  = body.ru,
        cid = body.cid,
    ))
    await db.commit()
async def db_update_word(db: AsyncSession, word: Word, body: WordUpdate) -> None:
    word.en  = body.en
    word.ru  = body.ru
    word.cid = body.cid
    await db.commit()
async def db_delete_word(db: AsyncSession, word: Word) -> None:
    await db.delete(word)
    await db.commit()


@router.get("/{cid}")
async def get_words(
    cid: int, 
    db:  AsyncSession = Depends(db_helper.get_db)
):
    wordsList = []

    words = await db_get_all_words(db, cid)

    for word in words:
        wordsList.append({
            "id":  word.id,
            "en":  word.en,
            "ru":  word.ru,
            "cid": word.cid,
        })

    return {"words": wordsList}


@router.post("/")
async def add_word(
    body: WordAdd, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    word = await db_get_word_by_cid(db, body.cid)

    if word:
        await db_add_word(db, body)

        return {"message": "word added"}

    raise HTTPException(404, "cid not found")

@router.put("/")
async def update_word(
    body: WordUpdate, 
    db:   AsyncSession = Depends(db_helper.get_db)
):
    word = await db_get_word_by_id(db, body.id)

    if word:
        await db_update_word(db, word, body)

        return {"message": "word updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_word(
    id: int, 
    db: AsyncSession = Depends(db_helper.get_db)
):
    word = await db_get_word_by_id(db, id)

    if word:
        await db_delete_word(db, word)

        return {"message": "word deleted"}

    raise HTTPException(404, "id not found")