from sqlalchemy.orm import sessionmaker

from alembic_getting_started.data import USERS, POSTS, COMMENTS, REACTIONS
from alembic_getting_started.models import User, engine, Base, Post, Comment, Reaction

Session = sessionmaker(bind=engine)
session: Session = Session()
# Base.metadata.create_all(bind=engine)


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
    session.close()
