import datetime

from sqlalchemy import create_engine, Integer, String, Date, ForeignKey, Boolean, Column
from sqlalchemy.orm import registry, relationship

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

    borrows = relationship("Borrows", back_populates="book")


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
    borrowed_date = Column(Date, default=datetime.date.today())
    return_date = Column(Date, default=None, nullable=True)

    book = relationship(Book, back_populates="borrows")
    user = relationship(User, back_populates="books")

    def is_book_available(self, book: Book) -> bool:
        pass