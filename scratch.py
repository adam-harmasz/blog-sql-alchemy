
from sqlalchemy import create_engine, Integer, String, Date, ForeignKey, Boolean, Column
from sqlalchemy.orm import registry

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("author.id"))
    genre_id = Column(Integer, ForeignKey("genre.id"))
    release_date = Column(Date)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_nr = Column(Integer)


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_nr = Column(Integer)


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    genre = Column(String)


class Borrows(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    book_id = Column(Integer, ForeignKey("book.id"))
    borowerd_date = Column(Date)
    return_date = Column(Date)

    def is_book_available(self, book: Book) -> bool:
        pass


# Base.metadata.create_all(engine)

x = (4)
y = (4,)

print(isinstance(x, int))
print(isinstance(y, tuple))