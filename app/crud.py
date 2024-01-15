from sqlalchemy             import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine      import Result
from typing                 import List

from app.database           import *
from app.schemas            import *

import time


async def get_all_categories(db: AsyncSession):
    result:             Result = await db.execute(select(Category).order_by(desc(Category.index)))
    categories: List[Category] = result.scalars().all()
    return categories


async def get_category_by_id(db: AsyncSession, id: int):
    result:   Result   = await db.execute(select(Category).filter(Category.id == id))
    category: Category = result.scalars().first()
    return category 


async def get_category_by_title(db: AsyncSession, title: str):
    result:   Result   = await db.execute(select(Category).filter(Category.title == title))
    category: Category = result.scalars().first()
    return category


async def add_category(db: AsyncSession, category: CategoryAdd):
    db.add(Category(
        title = category.title, 
        index = category.index, 
        type  = category.type,
    ))
    await db.commit()


async def update_category(db: AsyncSession, row: Category, category: CategoryUpdate):
    row.title = category.title
    row.index = category.index
    row.type  = category.type
    await db.commit()


async def delete_category(db: AsyncSession, category: Category):
    await db.delete(category)
    await db.commit()


###


async def get_all_blogs(db: AsyncSession):
    result: Result     = await db.execute(select(Blog).order_by(desc(Blog.index)))
    blogs:  List[Blog] = result.scalars().all()
    return blogs


async def get_all_blogs_by_cid(db: AsyncSession, cid: int):
    result: Result     = await db.execute(select(Blog).filter(Blog.cid == cid).order_by(desc(Blog.index)))
    blogs:  List[Blog] = result.scalars().all()
    return blogs


async def get_blog_by_id(db: AsyncSession, id: int):
    result: Result = await db.execute(select(Blog).filter(Blog.id == id))
    blog:   Blog   = result.scalars().first()
    return blog


async def get_blog_by_cid(db: AsyncSession, cid: int):
    result:   Result   = await db.execute(select(Category).filter(Category.id == cid, Category.type == 0))
    category: Category = result.scalars().first()
    return category


async def add_blog(db: AsyncSession, blog: BlogAdd):
    db.add(Blog(
        title = blog.title, 
        index = blog.index,
        date  = int(time.time()),
        cid   = blog.cid,
    ))
    await db.commit()


async def update_blog(db: AsyncSession, row: Blog, blog: BlogUpdate):
    row.title = blog.title
    row.index = blog.index
    row.date  = int(time.time())
    row.cid   = blog.cid
    await db.commit()


async def delete_blog(db: AsyncSession, blog: Blog):
    await db.delete(blog)
    await db.commit()


###


async def get_all_contents(db: AsyncSession):
    result:   Result        = await db.execute(select(Content).order_by(Content.bid))
    contents: List[Content] = result.scalars().all()
    return contents


async def get_all_contents_by_bid(db: AsyncSession, bid: int):
    result:   Result        = await db.execute(select(Content).filter(Content.bid == bid).order_by(desc(Content.index)))
    contents: List[Content] = result.scalars().all()
    return contents


async def get_content_by_id(db: AsyncSession, id: int):
    result:  Result  = await db.execute(select(Content).filter(Content.id == id))
    content: Content = result.scalars().first()
    return content


async def get_content_by_bid(db: AsyncSession, bid: int):
    result: Result = await db.execute(select(Blog).filter(Blog.id == bid))
    blog:   Blog   = result.scalars().first()
    return blog


async def add_content(db: AsyncSession, content: ContentAdd):
    db.add(Content(
        title = content.title,
        index = content.index,
        image = 0, 
        bid   = content.bid
    ))
    await db.commit()


async def update_content(db: AsyncSession, row: Content, content: ContentUpdate):
    row.title = content.title
    row.index = content.index
    await db.commit()


async def delete_content(db: AsyncSession, content: Content):
    await db.delete(content)
    await db.commit()


async def add_image(db: AsyncSession, title: str, index: int, bid: int):
    db.add(Content(
        title = title,
        index = index,
        image = 1, 
        bid   = bid
    ))
    await db.commit()


async def update_image(db: AsyncSession, content: Content, title: str, index: int):
    content.title = title
    content.index = index
    content.image = 1
    await db.commit()


###


# async def get_all_users(db: AsyncSession):
#     result: Result = await db.execute(select(User))
#     user:   User   = result.scalars().all()
#     return user 


# async def get_user_by_id(db: AsyncSession, id: int):
#     result: Result = await db.execute(select(User).filter(User.id == id))
#     user:   User   = result.scalars().first()
#     return user


# async def get_user_by_username(db: AsyncSession, username: str):
#     result: Result = await db.execute(select(User).filter(User.username == username))
#     user:   User   = result.scalars().first()
#     return user


# async def add_user(db: AsyncSession, user: UserModel):
#     db.add(User(
#         username=user.username, 
#         password=user.password,
#     ))
#     await db.commit()


# async def update_user(db: AsyncSession, row: User, user: UserUpdateModel):
#     row.username = user.username
#     row.password = user.password
#     await db.commit()


# async def delete_user(db: AsyncSession, user: User):
#     await db.delete(user)
#     await db.commit()