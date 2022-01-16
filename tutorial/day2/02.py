from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert, text, select, update, bindparam, func, Text
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

    reactions = relationship('Reaction', back_populates='post')
    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )
    comments = relationship("Comment", back_populates="post")

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return (
            f"BlogPost(id: {self.id}, headline: {self.headline}, author: {self.author})"
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


Base.metadata.create_all(engine)
