from sqlalchemy                 import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker


engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
# engine = create_engine("postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String,  nullable=False)
    password = Column(String,  nullable=False)


class Category(Base):
    __tablename__ = "categories"
    id    = Column(Integer, primary_key=True, index=True)
    title = Column(String,  nullable=False)
    index = Column(Integer, nullable=False)
    type  = Column(Integer, nullable=False)


class Blog(Base):
    __tablename__ = "blogs"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String,  nullable=False)
    index       = Column(Integer, nullable=False)
    date        = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)


class Content(Base):
    __tablename__ = "contents"
    id      = Column(Integer, primary_key=True, index=True)
    title   = Column(String,  nullable=False)
    index   = Column(Integer, nullable=False)
    image   = Column(Integer, nullable=False)
    blog_id = Column(Integer, nullable=False)


SessionLocal = sessionmaker(autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()