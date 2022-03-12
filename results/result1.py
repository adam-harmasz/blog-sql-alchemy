import datetime

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
    update,
    bindparam,
    func,
    Text,
    Enum, ForeignKeyConstraint, DateTime, CheckConstraint,

)
import enum
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session, declarative_base

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

Base = declarative_base()

# association table, tabela pośrednia
post_keywords = Table(
    "post_keywords",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)


class ReactionEnum(enum.Enum):
    LIKE = "Like"
    HEART = "Heart"


class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    author_id = Column(Integer, ForeignKey("author.id"))

    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )
    author = relationship("Author", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    reactions = relationship("Reaction", back_populates="post")

    def __init__(self, headline, body, author):
        self.headline = headline
        self.body = body
        self.author = author

    def __repr__(self):
        return f"BlogPost(id: {self.id}, headline: {self.headline})"


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    posts = relationship(
        "BlogPost",
        secondary=post_keywords,
        back_populates="keywords",
    )

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return f"Keyword(id: {self.id}, keyword: {self.keyword})"


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    posts = relationship(BlogPost, back_populates="author")
    reactions = relationship("Reaction", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"Author(id: {self.id}, name: {self.name})"


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    created_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("author.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    reactions = relationship("Reaction", back_populates="comment")
    post = relationship(BlogPost, back_populates="comments")
    author = relationship(Author, back_populates="comments")


class Reaction(Base):
    __tablename__ = "reaction"
    __table_args__ = (
        CheckConstraint(
            "(post_id IS NULL OR comment_id IS NULL) AND NOT (post_id IS NULL AND comment_id IS NULL)", "XOR CONSTRAINT"
        ),
    )

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ReactionEnum))
    comment_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("author.id"))

    comment = relationship("Comment", back_populates="reactions")
    author = relationship("Author", back_populates="reactions")
    post = relationship(BlogPost, back_populates="reactions")


Base.metadata.create_all(engine)


with Session(engine) as session:
    author1 = Author(name="Adam", last_name="Mickiewicz")
    post1 = BlogPost(headline="This is headline", body="My first post!", author=author1)
    keyword = Keyword(keyword="Earth")
    keyword.posts.append(post1)
    session.add_all([post1, keyword, author1])
    session.commit()

    comment1 = Comment(body="body", created_at=datetime.datetime.now(), author=author1, post=post1)
    session.add(comment1)
    session.commit()

    reaction = Reaction(type=ReactionEnum.LIKE, post=post1, comment=comment1, author=author1)

    session.add_all([reaction])
    session.commit()
