"""
DODAWANIE REKORDÓW PRZY UŻYCIU CORE API

Tak jak wcześniej deklarujemy tabele, a następnie korzystając z funkcji insert, dodajemy wiersze do tabeli, możemy to zrobić na dwa sposoby które podane są niżej
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert, text, select
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Base = declarative_base()  # to jest równoważne do tworzenia Base z mapper_registry


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_name = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
       return f"User(id={self.id}, name={self.name}, fullname={self.name} {self.last_name})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))  # Tutaj definiujemy relację z tabelą user_account

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.metadata.create_all(engine)


stmt = insert(User.__table__).values(name='Anthony', last_name="Hopkins")

with engine.connect() as conn:
    conn.execute(stmt)
    conn.execute(
        insert(User),
        [{"name": "David", "last_name": "Fincher"}, {"name": "David", "last_name": "Lynch"}],
    )

    select_stmt = select(User.__table__.c.id, User.__table__.c.name + "@aol.com")
    insert_stmt = insert(Address.__table__).from_select(["user_id", "email_address"], select_stmt)

    conn.execute(insert_stmt)
    conn.commit()


with Session(engine) as session:
    result = session.query(User).all()
    for row in result:
        print(f"id: {row.id}, name: {row.name}, last_name: {row.last_name}")

    addresses = session.query(Address).all()
    for row in addresses:
        print(f"id: {row.id!r}, email: {row.email_address}, user: {row.user}")
