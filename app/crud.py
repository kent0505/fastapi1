from sqlalchemy     import desc
from sqlalchemy.orm import Session
from app.database   import *
from app.schemas    import *
import time


async def get_all_users(db: Session):
    return db.query(User).all()


async def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


async def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def add_user(db: Session, user: UserModel):
    db.add(User(
        username=user.username, 
        password=user.password
    ))
    db.commit()


async def update_user(db: Session, row: User, user: UserUpdateModel):
    row.username = user.username
    row.password = user.password
    db.commit()


async def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


###


async def get_all_categories(db: Session):
    return db.query(Category).order_by(desc(Category.index)).all()


async def get_category_by_id(db: Session, id: int):
    return db.query(Category).filter(Category.id == id).first()


async def get_category_by_title(db: Session, title: str):
    return db.query(Category).filter(Category.title == title).first()


async def add_category(db: Session, category: CategoryAdd):
    db.add(Category(
        title = category.title, 
        index = category.index, 
        type  = category.type,
    ))
    db.commit()


async def update_category(db: Session, row: Category, category: CategoryUpdate):
    row.title = category.title
    row.index = category.index
    row.type  = category.type
    db.commit()


async def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()


###


async def get_all_blogs(db: Session):
    return db.query(Blog).order_by(desc(Blog.index)).all()


async def get_all_blogs_by_category_id(db: Session, category_id: int):
    return db.query(Blog).filter(Blog.category_id == category_id).order_by(desc(Blog.index)).all()


async def get_blog_by_id(db: Session, id: int):
    return db.query(Blog).filter(Blog.id == id).first()


async def get_blog_by_category_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.type == 0).first()


async def add_blog(db: Session, blog: BlogAdd):
    db.add(Blog(
        title       = blog.title, 
        index       = blog.index,
        date        = int(time.time()),
        category_id = blog.category_id,
    ))
    db.commit()


async def update_blog(db: Session, row: Blog, blog: BlogUpdate):
    row.title       = blog.title
    row.index       = blog.index
    row.date        = int(time.time())
    row.category_id = blog.category_id
    db.commit()


async def delete_blog(db: Session, blog: Blog):
    db.delete(blog)
    db.commit()


###


async def get_all_contents(db: Session):
    return db.query(Content).order_by(Content.blog_id).all()


async def get_all_contents_by_blog_id(db: Session, blog_id: int):
    return db.query(Content).filter(Content.blog_id == blog_id).order_by(desc(Content.index)).all()


async def get_content_by_id(db: Session, id: int):
    return db.query(Content).filter(Content.id == id).first()


async def get_content_by_blog_id(db: Session, blog_id: int):
    return db.query(Blog).filter(Blog.id == blog_id).first()


async def add_content(db: Session, content: ContentAdd):
    db.add(Content(
        title   = content.title,
        index   = content.index,
        image   = 0, 
        blog_id = content.blog_id
    ))
    db.commit()


async def update_content(db: Session, row: Content, content: ContentUpdate):
    row.title = content.title
    row.index = content.index
    db.commit()


async def delete_content(db: Session, content: Content):
    db.delete(content)
    db.commit()


async def add_image(db: Session, title: str, index: int, blog_id: int):
    db.add(Content(
        title   = title,
        index   = index,
        image   = 1, 
        blog_id = blog_id
    ))
    db.commit()


async def update_image(db: Session, content: Content, title: str, index: int):
    content.title = title
    content.index = index
    content.image = 1
    db.commit()