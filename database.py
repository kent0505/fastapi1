from sqlalchemy import  create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id =       Column(Integer, primary_key=True, index=True)
    username = Column(String,  nullable=False)
    password = Column(String,  nullable=False)

class Category(Base):
    __tablename__ = "categories"
    id =    Column(Integer, primary_key=True, index=True)
    title = Column(String,  nullable=False)

class Blog(Base):
    __tablename__ = "blogs"
    id =          Column(Integer, primary_key=True, index=True)
    title =       Column(String,  nullable=False)
    category_id = Column(Integer, nullable=False)

class Content(Base):
    __tablename__ = "contents"
    id =      Column(Integer, primary_key=True, index=True)
    title =   Column(String,  nullable=False)
    image =   Column(Integer, nullable=False)
    blog_id = Column(Integer, nullable=False)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()