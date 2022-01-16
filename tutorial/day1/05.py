"""
Korzystając z obiektu Table tworzymy deklarujemy tabelę user_account, a następnie wykorzystując isntrancję Metadata używamy
metody create_all by przesłać do bazy żądanie stworzenia tabeli user_account
"""

from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

addresses = Table(
    "adresses",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('email', String(30)),
    Column('user', String),
)

print(dir(addresses))
print(addresses.c.keys())

metadata_obj.create_all(engine)
