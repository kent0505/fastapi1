from sqlalchemy.orm         import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine("sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id:       Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

class Category(Base):
    __tablename__ = "categories"
    id:    Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    type:  Mapped[int] = mapped_column(nullable=False)

class Blog(Base):
    __tablename__ = "blogs"
    id:    Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    date:  Mapped[int] = mapped_column(nullable=False)
    cid:   Mapped[int] = mapped_column(nullable=False) # category id

class Content(Base):
    __tablename__ = "contents"
    id:    Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[int] = mapped_column(nullable=False)
    bid:   Mapped[int] = mapped_column(nullable=False) # blog id

class Product(Base):
    __tablename__ = "products"
    id:    Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    type:  Mapped[int] = mapped_column(nullable=False)
    group: Mapped[int] = mapped_column(nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id:    Mapped[int] = mapped_column(primary_key=True)
    uid:   Mapped[int] = mapped_column(nullable=False) # user id
    oid:   Mapped[int] = mapped_column(nullable=False) # order id
    count: Mapped[int] = mapped_column(nullable=False)
    date:  Mapped[int] = mapped_column(nullable=False)
    lat:   Mapped[int] = mapped_column(nullable=False)
    lon:   Mapped[int] = mapped_column(nullable=False)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()