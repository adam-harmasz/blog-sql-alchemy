from sqlalchemy import Column, Integer, String, ForeignKey, select, func, create_engine
from sqlalchemy.orm import relationship, Session, declarative_base

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

Base = declarative_base()


"""
Book
    id Integer PK
    title String
    author_id Integer FK 
    availability Boolean
    release_date Date
    isbn String
    genre String

User
    id Integer PK
    first_name String
    last_name String
    
Author
    id Integer PK
    first_name String
    last_name String

Borrow
    id Integer PK
    borrow_date Date
    return_date Date
    book_id Integer FK
    user_id Integer FK
"""


