from sqlalchemy     import desc
from sqlalchemy.orm import Session
from app.database   import *
from app.routers.user import *


async def get_all_users(db: Session):
    rows = db.query(User).all()
    return rows


async def get_user_by_id(db: Session, id: int):
    row = db.query(User).filter(User.id == id).first()
    return row


async def get_user_by_username(db: Session, username: str):
    row = db.query(User).filter(User.username == username).first()
    return row


async def add_user(db: Session, username: str, password: str):
    db.add(User(
        username=username, 
        password=password
    ))
    db.commit()


async def update_user(db: Session, user: User, username: str, password: str):
    user.username = username
    user.password = password
    db.commit()


async def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

###

async def get_all_categories(db: Session):
    rows = db.query(Category).order_by(desc(Category.index)).all()
    return rows


async def get_category_by_id(db: Session, id: int):
    row = db.query(Category).filter(Category.id == id).first()
    return row


async def get_category_by_title(db: Session, title: str):
    row = db.query(Category).filter(Category.title == title).first()
    return row


async def add_category(db: Session, title: str, index: int, type: int):
    db.add(Category(
        title = title, 
        index = index, 
        type  = type,
    ))
    db.commit()


async def update_category(db: Session, category: Category, title: str, index: int, type: int):
    category.title = title
    category.index = index
    category.type  = type
    db.commit()

async def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()

###

async def get_all_blogs(db: Session):
    rows = db.query(Blog).order_by(desc(Blog.index)).all()
    return rows


async def get_all_blogs_by_category_id(db: Session, category_id: int):
    rows = db.query(Blog).filter(Blog.category_id == category_id).order_by(desc(Blog.index)).all()
    return rows


async def get_blog_by_id(db: Session, id: int):
    row = db.query(Blog).filter(Blog.id == id).first()
    return row


async def get_blog_by_category_id(db: Session, category_id: int):
    row = db.query(Category).filter(Category.id == category_id, Category.type == 0).first()
    return row

# async def get_blog_by_id(db: Session, id: int):
#     row = db.query(Blog).filter(Blog.id == id, Category.type == 0).first()
#     return row

async def get_blog_by_id(db: Session, id: int):
    row = db.query(Blog).filter(Blog.id == id).first()
    return row


async def add_blog(db: Session, title: str, index: int, date: int, category_id: int):
    db.add(Blog(
        title       = title, 
        index       = index,
        date        = date,
        category_id = category_id,
    ))
    db.commit()


async def update_blog(db: Session, blog: Blog, title: str, index: int, date: int, category_id: int):
    blog.title       = title
    blog.index       = index
    blog.date        = date
    blog.category_id = category_id
    db.commit()


async def delete_blog(db: Session, blog: Blog):
    db.delete(blog)
    db.commit()

###

async def get_all_contents(db: Session):
    rows = db.query(Content).order_by(Content.blog_id).all()
    return rows


async def get_all_contents_by_blog_id(db: Session, blog_id: int):
    rows = db.query(Content).filter(Content.blog_id == blog_id).order_by(desc(Content.index)).all()
    return rows


async def get_content_by_id(db: Session, id: int):
    row = db.query(Content).filter(Content.id == id).first()
    return row


async def get_content_by_blog_id(db: Session, blog_id: int):
    row = db.query(Blog).filter(Blog.id == blog_id).first()
    return row


async def add_content(db: Session, title: str, index: int, image: int, blog_id: int):
    db.add(Content(
        title   = title,
        index   = index,
        image   = image, 
        blog_id = blog_id
    ))
    db.commit()


async def update_content(db: Session, content: Content, title: str, index: int):
    content.title = title
    content.index = index
    db.commit()


async def delete_content(db: Session, content: Content):
    db.delete(content)
    db.commit()


async def update_image(db: Session, content: Content, title: str, index: int):
    content.title = title
    content.index = index
    content.image = 1
    db.commit()