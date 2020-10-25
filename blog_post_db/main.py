from sqlalchemy import func, text
from sqlalchemy.orm import sessionmaker

from blog_post_db.data import USERS, POSTS, COMMENTS, REACTIONS
from blog_post_db.models import User, engine, Base, Post, Comment, Reaction

Session = sessionmaker(bind=engine)
session: Session = Session()
Base.metadata.create_all(bind=engine)


def create_users(data):
    user_objs = [User(**user_data) for user_data in data]
    session.add_all(user_objs)
    session.commit()


def create_posts(data):
    post_objs = [Post(**post_data) for post_data in data]
    session.add_all(post_objs)
    session.commit()


def create_comments(data):
    comment_objs = [Comment(**comment_data) for comment_data in data]
    session.add_all(comment_objs)
    session.commit()


def create_reactions(data):
    reaction_objs = [Reaction(**reaction_data) for reaction_data in data]
    session.add_all(reaction_objs)
    session.commit()


def create_data():
    create_users(USERS)
    create_posts(POSTS)
    create_comments(COMMENTS)
    create_reactions(REACTIONS)


if __name__ == "__main__":
    create_data()


"""
- Query które zwróci najbardziej komentowany post
- Query które zwróci najbardziej lajkowany post
- Query które zwróci najbardziej lajkowany komentarz
- Query które zwróci usera który dostał najwięcej lajków
- Query które zwróci usera z największą liczbą postów
- Query które zwróci usera z największa liczbą komentarzy
- Na podstawie tego jak były robione dane z innych tabel, zrobić 'fixtury' dla keywords
- Zwrócić post który ma najwięcej liter 'a'
- Zwrócić komentarze które zaczynają się na 'a' (niezależnie od wielkości liter)
"""

q1 = (
    session.query(Post, func.count(Comment.id).label("comment_count"))
    .join(Comment, Comment.user_id == Post.id)
    .group_by(Comment.post_id)
    .order_by(text("comment_count DESC"))
    .first()
)

stmt = (
    session.query(Comment, func.count(Comment.id).label("comment_count"))
    .group_by(Comment.post_id)
    .subquery()
)
q2 = (
    session.query(Post, stmt.c.comment_count)
    .join(Post, Post.id == stmt.c.post_id)
    .order_by(stmt.c.comment_count.desc())
    .first()
)
print(q2)
print(q1)
