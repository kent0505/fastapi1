from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    fcmtoken: Mapped[str] = mapped_column(nullable=False)

class Category(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    type:  Mapped[int] = mapped_column(nullable=False)

class Blog(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    date:  Mapped[int] = mapped_column(nullable=False)
    cid:   Mapped[int] = mapped_column(nullable=False) # category id

class Content(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[int] = mapped_column(nullable=False)
    bid:   Mapped[int] = mapped_column(nullable=False) # blog id