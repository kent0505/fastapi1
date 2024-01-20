from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy             import desc, select
from sqlalchemy.engine      import Result
from typing                 import List
from app.database           import *
from app.schemas            import *
from app.utils              import *


router = APIRouter()


class ProductAdd(BaseModel):
    title: str
    price: int
    type:  int


class ProductUpdate(BaseModel):
    id:    int
    title: str
    price: int
    type:  int


async def db_get_all_products(db: AsyncSession):
    result:   Result        = await db.execute(select(Product))
    products: List[Product] = result.scalars().all()
    return products


async def db_get_product_by_id(db: AsyncSession, id: int):
    result:  Result  = await db.execute(select(Product).filter(Product.id == id))
    product: Product = result.scalars().first()
    return product 


# async def db_get_category_by_title(db: AsyncSession, title: str):
#     result:   Result   = await db.execute(select(Category).filter(Category.title == title))
#     category: Category = result.scalars().first()
#     return category


async def db_add_product(db: AsyncSession, product: ProductAdd):
    db.add(Product(
        title = product.title, 
        price = product.price, 
        type  = product.type,
    ))
    await db.commit()


async def db_update_product(db: AsyncSession, row: Product, product: ProductUpdate):
    row.title = product.title
    row.price = product.price
    row.type  = product.type
    await db.commit()


async def db_delete_product(db: AsyncSession, product: Product):
    await db.delete(product)
    await db.commit()


@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):
    productsList = []

    products = await db_get_all_products(db)

    for category in products:
        productsList.append({
            "id":    category.id,
            "title": category.title,
            "price": category.price,
            "type":  category.type
        })

    return {"category": productsList}


@router.post("/")
async def add_product(product: ProductAdd, db: AsyncSession = Depends(get_db)):
    await db_add_product(db, product)

    return {"message": "product added"}


@router.put("/")
async def update_product(product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    row = await db_get_product_by_id(db, product.id)

    if row:
        await db_update_product(db, row, product)

        return {"message": "product updated"}

    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    row = await db_get_product_by_id(db, id)

    if row:
        await db_delete_product(db, row)

        return {"message": "product deleted"}

    raise HTTPException(404, "id not found")