import datetime as dt
import enum
import random
from typing import Type

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    insert,
    text,
    select,
    Enum,
    func,
    Date, exists,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session, declarative_base

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
Base = declarative_base()  # to jest równoważne do tworzenia Base z mapper_registry


class GenreEnum(enum.Enum):
    FANTASY = "Fantasy"
    THRILLER = "Thriller"
    SCIENCE_FICTION = "Science-fiction"
    ACTION = "Action"
    ADVENTURE = "Adventure"
    COMIC = "Comic"
    HORROR = "Horror"
    MYSTERY = "Mystery"


class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    isbn = Column(String(13), nullable=False)
    publication_year = Column(Integer)
    genre = Column(Enum(GenreEnum))
    author_id = Column(Integer, ForeignKey("Authors.id"))

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")

    def __repr__(self) -> str:
        return f"Book(id: {self.id}, title: {self.title}, author: {self.author})"


class Author(Base):
    __tablename__ = "Authors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    books = relationship(Book, back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Author(id: {self.id}, name: {self.fullname})"

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    borrows = relationship("Borrow", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id: {self.id}, name: {self.fullname})"

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Borrow(Base):
    __tablename__ = "Borrows"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    user = relationship(User, back_populates="borrows")
    book = relationship(Book, back_populates="borrows")

    def __init__(self, book_id: int, user_id: int) -> None:
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = dt.date.today()


Base.metadata.create_all(engine)


def get_users() -> list[User]:
    anthony = User(first_name="Anthony", last_name="Hopkins")
    matthew = User(first_name="Matthew", last_name="McConaughey")

    return [anthony, matthew]


def get_authors() -> list[Author]:
    lee_child = Author(first_name="Lee", last_name="Child")
    stephen_king = Author(first_name="Stephen", last_name="King")
    drew_karpyshyn = Author(first_name="Drew", last_name="Karpyshyn")

    return [lee_child, stephen_king, drew_karpyshyn]


def get_books() -> list[Book]:
    killing_floor = Book(
        title="Killing Floor",
        isbn=_get_isbn(),
        publication_year=1997,
        author_id=1,
        genre=random_genre(GenreEnum),
    )
    die_trying = Book(
        title="Die Trying",
        isbn=_get_isbn(),
        publication_year=1999,
        author_id=1,
        genre=random_genre(GenreEnum),
    )
    rule_of_two = Book(
        title="Rule of two",
        isbn=_get_isbn(),
        publication_year=2007,
        author_id=3,
        genre=random_genre(GenreEnum),
    )
    shining = Book(
        title="The Shining",
        isbn=_get_isbn(),
        publication_year=1977,
        author_id=2,
        genre=random_genre(GenreEnum),
    )
    gunslinger = Book(
        title="The Gunslinger",
        isbn=_get_isbn(),
        publication_year=1982,
        author_id=2,
        genre=random_genre(GenreEnum),
    )
    return [
        gunslinger, rule_of_two, shining, killing_floor, die_trying
    ]


def populate_db() -> None:
    with Session(engine) as session:
        session.add_all(get_users())
        session.commit()

        session.add_all(get_authors())
        session.commit()

        session.add_all(get_books())
        session.commit()

def _get_isbn() -> str:
    return str(random.randrange(start=1_000_000_000_000, stop=9999999999999, step=1))


def random_genre(genre_enum: Type[GenreEnum]) -> "GenreEnum":
    return random.choice(
        [
            genre_enum.FANTASY,
            genre_enum.THRILLER,
            genre_enum.SCIENCE_FICTION,
            genre_enum.ACTION,
            genre_enum.ADVENTURE,
            genre_enum.COMIC,
            genre_enum.HORROR,
            genre_enum.MYSTERY,
        ]
    )

populate_db()


def list_books() -> None:
    with Session(engine) as session:
        books = session.execute(select(Book)).scalars().all()
        for book in books:
            print(book)


def list_authors() -> None:
    with Session(engine) as session:
        authors = session.execute(select(Book)).scalars().all()
        for author in authors:
            print(author)


def list_users() -> None:
    with Session(engine) as session:
        users = session.execute(select(User)).scalars().all()
        for user in users:
            print(user)


def borrow_book(book_id: int, user_id: int) -> None:
    with Session(engine) as session:
        session.add(
            Borrow(book_id=book_id, user_id=user_id)
        )
        session.commit()


def list_borrowed_books():
    with Session(engine) as session:
        books = session.execute(select(Book, func.count(Borrow.id)).join(Borrow).group_by(Book.id)).all()
        for book, count in books:
            print(f"title: {book.title}, currently borrowed copies: {count}")


borrow_book(1, 1)
borrow_book(2, 2)
borrow_book(2, 2)
list_borrowed_books()
