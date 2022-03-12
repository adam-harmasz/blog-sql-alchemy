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



"""
Comment
    id Integer PK
    body Text
    created_at DateTime
    author_id Integer FK
    post_id Integer FK
    

Reaction
    id Integer PK
    type Enum    
    comment_id Integer FK
    post_id Integer FK
    author_id Integer FK
    
    
* Zrobić taki mechanizm po stronie bazy danych, aby nie dało się jednocześnie dać reakcji dla postu i komentarza (constraint)
"""
