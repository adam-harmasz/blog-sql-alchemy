from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert, text, select, update, bindparam
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
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
       return f"User(id={self.id!r}, name={self.name!r}, fullname={self.name!r} {self.last_name})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))  # Tutaj definiujemy relację z tabelą user_account

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.metadata.create_all(engine)


stmt = insert(User).values(name="Anthony", last_name="Hopkins")

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


session = Session(engine)

john = User(name="John", last_name="Malkovich")
adam = User(name="Adam", last_name="Driver")

session.add(john)
session.add(adam)

# print(adam.id)
# print(john.id)
# print(session.new)
# # session.flush()
# # q = session.query(User).all()
# print(session.new)
# print(adam.id)
session.commit()

adam.name = "Not Adam"
# print(session.dirty)
#
# session.commit()
# print(session.dirty)
print(session.query(User).where(User.name == "Not Adam").first())
session.rollback()
print(session.query(User).where(User.name == "Not Adam").first())

print(session.dirty)
session.execute(
    update(User).
    where(User.name == "Not Adam").
    values(name="Adam")
)
session.commit()
print(session.query(User).where(User.name == "Adam").first())

session.delete(adam)
session.commit()
print(session.query(User).all())