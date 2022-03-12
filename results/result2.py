import enum

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert, text, select, update, bindparam, func, \
    Text, Enum, Date
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

    def __init__(self, headline, body, author):
        self.headline = headline
        self.body = body
        self.author = author

    def __repr__(self):
        return (
            f"BlogPost(id: {self.id}, headline: {self.headline})"
        )


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

    def __repr__(self):
        return f"Author(id: {self.id}, name: {self.name})"


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey("author.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(Date)

    posts = relationship("BlogPost", back_populates="comments")
    author = relationship("Author", back_populates="comments")
    reactions = relationship("Reaction", back_populates="comments")


class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    comment_id = Column(Integer, ForeignKey("comment.id"))
    type = Column(Enum)

    posts = relationship("BlogPost", back_populates="reactions")
    comments = relationship("Comment", back_populates="reactions")
    author = relationship("Author", back_populates="reactions")


class ReactionEnum(enum.Enum):
    like = "Like"
    unlike = "I don't like"
    super = "<3"


Base.metadata.create_all(engine)

author1 = Author(name="Adam", last_name="Mickiewicz")
post1 = BlogPost(headline="This is headline", body="My first post!", author=author1)
keyword = Keyword(keyword="Earth")
keyword2 = Keyword(keyword="Some keyword")
keyword.posts.append(post1)
post1.keywords.append(keyword2)

with Session(engine) as session:
    session.add_all([post1, keyword, author1])
    session.commit()
    print(keyword.posts)
