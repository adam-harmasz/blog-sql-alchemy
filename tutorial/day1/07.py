"""
DODAWANIE REKORDÓW PRZY UŻYCIU CORE API

Tak jak wcześniej deklarujemy tabele, a następnie korzystając z funkcji insert, dodajemy wiersze do tabeli, możemy to zrobić na dwa sposoby które podane są niżej
"""

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    insert,
    text,
    select,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Base = declarative_base()  # to jest równoważne do tworzenia Base z mapper_registry


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_name = Column(String)

    addresses = relationship("Address", back_populates="user")
    emails = relationship("EmailAddress", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.name} {self.last_name})"


class EmailAddress(Base):
    __tablename__ = "email_address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(
        Integer, ForeignKey("user_account.id")
    )  # Tutaj definiujemy relację z tabelą user_account

    user = relationship("User", back_populates="emails")

    def __repr__(self):
        return f"Email(id={self.id!r}, email_address={self.email_address!r})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    city = Column(String(50))
    postal_code = Column(String(6))
    street = Column(String(50))
    house_number = Column(String(10))
    flat_number = Column(String(10))
    country = Column(String(50))

    user = relationship(User, back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(country={self.country}, city={self.city}, street={self.street}, house nr={self.house_number})"


Base.metadata.create_all(engine)


stmt = insert(User).values(name="Anthony", last_name="Hopkins")

with engine.connect() as conn:
    conn.execute(stmt)
    conn.execute(
        insert(User),
        [
            {"name": "David", "last_name": "Fincher"},
            {"name": "David", "last_name": "Lynch"},
        ],
    )

    select_stmt = select(User.__table__.c.id, User.__table__.c.name + "@aol.com")
    insert_stmt = insert(EmailAddress.__table__).from_select(
        ["user_id", "email_address"], select_stmt
    )

    address_stmt = insert(Address).values(
        country="Polska",
        city="Pasikoniki Dolne",
        street="Długa",
        house_number="11",
        flat_number="11",
        postal_code="12-123",
        user_id=1,
    )
    conn.execute(address_stmt)
    conn.execute(insert_stmt)
    conn.commit()


with Session(engine) as session:
    result = session.query(User).all()
    for user in result:
        print(f"id: {user.id}, name: {user.name}, last_name: {user.last_name}")
        if user.id == 1:
            print("Hello Anthony")
            print(user.emails)

    emails = session.query(EmailAddress).all()
    for email in emails:
        print(f"id: {email.id!r}, email: {email.email_address}, user: {email.user}")
