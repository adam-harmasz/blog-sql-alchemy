"""
ORM DATA MANIPULATION
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, insert, text, select, update, bindparam, func, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, Session, declarative_base, aliased

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_name = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
       return f"User(id={self.id!r}, name={self.name!r}, fullname={self.name!r} {self.last_name!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))  # Tutaj definiujemy relację z tabelą user_account

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.metadata.create_all(engine)

adam = User(name="Adam", last_name="Driver", addresses=[Address(email_address="abc@gmail.com")])
david = User(name="David", last_name="Fincher", addresses=[])
sergio = User(name="Sergio", last_name="Leone", addresses=[Address(email_address="sergio@gmail.com"), Address(email_address="sergio@yahoo.com")])
robert = User(name="Robert", last_name="De Niro", addresses=[Address(email_address="robert@gmail.com")])


def populate_db(users: list[User]) -> None:
    with Session(engine) as session:
        session.add_all(users)
        session.commit()


populate_db([adam, david, sergio, robert])
session = Session(engine)

# Select all users and sort them by id in ascending order
# for user in session.query(User).order_by(User.id):
#     print(user)
# print("###")
# for user in session.execute(select(User).order_by(User.id)).scalars().all():
#     print(user)


# Select all users and sort them by id in descending order
# for user in session.query(User).order_by(User.id.desc()):
#     print(user)
#
# for user in session.execute(select(User).order_by(User.id.desc())).scalars().all():
#     print(user)

# Select user with id = 1
# for user in session.query(User).filter(User.id==1):
#     print(user)

# print(session.execute(select(User).filter(User.id == 1)).one())
#
#
# # Another way to select a user with id = 1
# for user in session.query(User).filter_by(id=1):
#     print(user)

# print(session.execute(select(User).filter_by(id=1)).one())

## JOIN ##

# for row in session.execute(select(User.name, Address.email_address)).all():
#     print(row)

# print(
#     session.execute(select(User.name, Address.email_address).join_from(User, Address)).all()
# )
#
# # JOIN, PODAJEMY TABELĘ KTÓRA MA ZOSTAĆ DOŁĄCZONA, A TA DO KTÓREJ MA BYĆ DOŁĄCZENIE JEST WYWNIOSKOWANE PRZEZ BIBLIOTEKĘ
# print(
#     session.execute(select(User.name, Address.email_address).join(Address)).all()
# )
#
# # JOIN W KTÓRYM PODAJEMY WPROST KTÓRA TABELA MA BYĆ JOINOWANA DO KTÓREJ
# print(
#     session.execute(select(User.name, Address.email_address).select_from(User).join(Address)).all()
# )
#
# # FUNKCJA ZLICZA ILOSĆ USERÓW
# print(
#     session.execute(select(func.count('*')).select_from(User)).all()
# )
#
# # FUNKCJA ZLICZA ILOŚĆ USERÓW DLA DANEGO USERA
# for row in session.execute(select(User.name, func.count(User.id)).group_by(User)).all():
#     print(row)

# for row in session.execute(select(User.name, func.count(Address.user_id)).join(Address).group_by(User.all():
#     print(row)


# LABELE, ALIASY
# stmt = select(
#         Address.user_id,
#         func.count(Address.id).label('num_addresses')).\
#         group_by("user_id").order_by(desc("num_addresses"))
# print(session.execute(stmt).all())
#
# # # Przykład użycia aliasów
# user_alias_1 = User.__table__.alias()
# user_alias_2 = User.__table__.alias()
# print(
#     session.execute(select(user_alias_1.c.id, user_alias_2.c.id).
#     join_from(user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id)).all()
# )

# user_alias_1 = aliased(User)
# user_alias_2 = aliased(User)
# print(
#     session.execute(select(user_alias_1.id, user_alias_2.id).
#     join_from(user_alias_1, user_alias_2, user_alias_1.id > user_alias_2.id)).all()
# )
#
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)
stmt = (
    select(User).
    join_from(User, address_alias_1).
    where(address_alias_1.email_address == 'sergio@yahoo.com').
    join_from(User, address_alias_2).
    where(address_alias_2.email_address == 'sergio@gmail.com')
)

print(session.execute(stmt).all())
