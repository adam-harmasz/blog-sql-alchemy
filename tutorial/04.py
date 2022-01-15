"""
Tworzymy tabelę jak we wcześniejszych przykłdach, jednak do uzyskania danych z tabeli używamy sesji
"""

from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# Używamy metody begin zamiast connection dzięki czemu na koniec bloku zmiany są komitowane w transakcji
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE Users(id integer primary key autoincrement, name varchar, last_name varchar)"))
    conn.execute(
        text("INSERT INTO Users (name, last_name) VALUES (:name, :last_name)"),
        [{"name": "David", "last_name": "Fincher"}, {"name": "David", "last_name": "Lynch"}]
    )

    result = conn.execute(text("SELECT * FROM Users")).all()
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")


stmt = text("SELECT id, name, last_name FROM Users WHERE id > :y ORDER BY name").bindparams(y=1)
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")


with Session(engine) as session:
    result = session.execute(
        text("UPDATE Users SET name=:name WHERE last_name=:last_name"),
        [{"name": "Adrian", "last_name": "Fincher"}, {"name": "John", "last_name": "Lynch"}]
    )
    session.commit()

    result = session.execute(text("SELECT * FROM Users")).all()
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")
