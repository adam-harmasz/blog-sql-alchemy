from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Sequence,
    text,
    func,
    ForeignKey,
    exists,
    Table,
    Text, CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    aliased,
    relationship,
    selectinload,
    joinedload,
    contains_eager,
)

engine = create_engine("sqlite:///:memory:", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# association table
post_keywords = Table(
    "post_keywords",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    posts = relationship("BlogPost", back_populates="author", lazy="dynamic")
    comments = relationship("Comment", back_populates="author")
    reactions = relationship("Reaction", back_populates="user")

    def __repr__(self):
        return f"User(id: {self.id}, name: {self.name})"


class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    reactions = relationship('Reaction', back_populates='post')
    keywords = relationship(
        "Keyword",
        secondary=post_keywords,
        back_populates="posts",
    )
    author = relationship(User, back_populates="posts")
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


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    title = Column(String(40))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    post = relationship('BlogPost', back_populates='comments')
    author = relationship('User', back_populates='comments')
    reactions = relationship('Reaction', back_populates='comment')

    def __repr__(self):
        return f"Comment(id: {self.id}, author: {self.author})"


class Reaction(Base):
    """This is 'like' same as it is in facebook but I didn't want to mix it with SQL keyword 'like' """

    __tablename__ = "reactions"
    __table_args__ = (
        CheckConstraint(
            "(post_id IS NULL OR comment_id IS NULL) AND NOT (post_id IS NULL AND comment_id IS NULL)", name="check constraint"
        ),
    )

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    comment = relationship(Comment, back_populates="reactions")
    post = relationship(BlogPost, back_populates="reactions")
    user = relationship(User, back_populates="reactions")

    def __repr__(self):
        return f"Reaction(id={self.id}, name: {self.user.name})"


Base.metadata.create_all(engine)

adam = User(name="Adam", fullname="Adam Driver", nickname="Taxi driver")
john = User(name="John", fullname="Johnny Bravo", nickname="Bravo")
post = BlogPost(headline="Adam's first post", body="Very nice post", author=adam)
session.add(post)
session.commit()

post.keywords.append(Keyword("very"))
post.keywords.append(Keyword("adam"))
session.commit()

comment = Comment(title="Title", content="Content", post=post, author=john)
session.add(comment)
session.commit()

# comment.reactions.append(Reaction(user=john))
# post.reactions.append(Reaction(user=adam))
reaction = Reaction(comment=comment, post=post, user=adam)
session.add(reaction)
session.commit()

# print(post.reactions)
# print(comment.reactions)
# print(len(comment.reactions))
print(session.query(Reaction).all())