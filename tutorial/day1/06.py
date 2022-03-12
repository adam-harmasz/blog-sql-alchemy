"""
Najpierw tworzymy klasę bazową Base, możemy to zrobić w dwóch krokach korzystając z registry, lub w jednym kroku korzystając z declarative_base
Następnie wykorzystujemy Base by utworzyć schemat tabel, na podstawie klas User i Address będą utrworzone dwie tabele
które są połączone relacją jeden do wielu.
Na koniec metoda create_all którą posiada Base wysyła zapytanie do bazy danych po czym stworzone zostają tabele

Zadania ORM:
•Połączenie się z bazą danych
•Połączenie zdefiniowanych klas Python’owych z tabelami w bazie danych
•Przygotowywanie zapytań do bazy danych
•Synchronizowanie zmian, które zachodzą na obiektach Python’owych z
ich odpowiednikami w wierszach tabel
"""

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    insert,
    select,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, declarative_base

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
# mapper_registry = registry()
# Base = mapper_registry.generate_base()

Base = declarative_base()  # to jest równoważne do tworzenia Base z mapper_registry


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(
        Integer, ForeignKey("user_account.id")
    )  # Tutaj definiujemy relację z tabelą user_account

    user = relationship(User, back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# Tu tworzymy tabele
Base.metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(
        insert(User),
        [
            {"name": "David", "fullname": "Fincher"},
            {"name": "David", "fullname": "Lynch"},
        ],
    )
    conn.execute(insert(Address).values(email_address="asd@asd.pl", user_id=1))
    conn.execute(insert(Address).values(email_address="email@email.pl", user_id=1))
    conn.commit()

    result = conn.execute(select(User).where(User.id == 1)).one()
    # for user in result:
    #     print(user)
    print(result)


# print(User.__table__)
# print(User.__table__.c.keys())
