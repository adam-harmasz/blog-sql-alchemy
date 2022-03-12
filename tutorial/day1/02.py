"""
TWORZENIE ENGINE

Łączymy się z bazą danych, a następnie tworzymy tabelę po czym dodajemy rekordy i komitujemy zmiany które następnie wyświetlamy

Funkcja create_engine() zwróci nam instancję klasy Engine, który z automatu ma podłączony
odpowiedni dialekt bazodanowy i sterownik.
Dialekt wraz ze sterownikiem opisują sposób komunikacji z bazą danych – informują w jaki sposób
tworzyć poszczególne zapytania, jakim protokołem łączyć się z bazą itp. Dialekt i sterownik jest
różny dla każdej z baz danych.
W naszym przypadku pod obiektem engine zostaną przypisane dane konfiguracyjne i dialekt dla
SQLite. SQLAlchemy odczytuje to z adresu podanego jako argument do funkcji create_engine().

Ważne! Wywołanie funkcji create_engine nie powoduje nawiązania połączenia z bazą danych.

"sqlite+pysqlite:///:memory:" - To jest connection string, tutaj definiujemy z jakiej bazy będziemy korzystać, jaki dielekt, gdzie baza ma być zapisana itp.
"""

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

with engine.connect() as conn:
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
    #
    conn.commit()  # Tutaj commitujemy zmiany do bazy danych
    result = conn.execute(text("SELECT * FROM Users")).all()
    print(result)
    for row in result:
        print(f"name: {row.name}, last_name: {row.last_name}")
