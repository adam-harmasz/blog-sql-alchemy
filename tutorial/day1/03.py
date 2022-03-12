"""
WSTĘP DO TWORZENIA TABELI

Łączymy się z bazą danych, a następnie tworzymy tabelę po czym dodajemy rekordy i komitujemy zmiany które następnie wyświetlamy
"""

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# Używamy metody begin zamiast connection dzięki czemu na koniec bloku zmiany są komitowane w transakcji
with engine.begin() as conn:
    conn.execute(
        text(
            "CREATE TABLE Users(id integer primary key autoincrement, name varchar, last_name varchar)"
        )
    )
    conn.execute(
        text("INSERT INTO Users (name, last_name) VALUES (:name, :last_name)"),
        [
            {"name": "David", "last_name": "Fincher"},
            {"name": "David", "last_name": "Lynch"},
        ],
    )

    result = conn.execute(text("SELECT * FROM Users")).all()
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")

# Chcemy uzyskać rekordy z id większym niż 1 przekazując do metody execute statement, metoda bindparams pozwala nam korzystać z zmiennych w zapytaniu
stmt = text(
    "SELECT id, name, last_name FROM Users WHERE id > :y ORDER BY id"
).bindparams(y=1)
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")
