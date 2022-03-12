"""
LOADING TECHNIQUES

LAZY LOADING - Gdy robimy zapytanie o obiekt np. User który ma też przypisane poprzez relacje inne obiekty to sql alchemy wyśle zapytanie dotyczące usera,
ale nie będą pobrane obiekty z relacji i zostaną "dociągnięte" dodatkowym zapytaniem w momencie, gdy do takiego obiektu odwołamy się w kodzie

EAGER LOADING - Gdy robimy zapytanie o obiekt np. User który ma też przypisane poprzez relacje inne obiekty to sql alchemy wyśle zapytanie dotyczące usera,
i pobierze obiekty z relacji

NO LOADING - Technika która zapewnia brak zapytań o obiekty z relacji
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
    update,
    bindparam,
    func,
    desc,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    registry,
    relationship,
    Session,
    declarative_base,
    aliased,
    joinedload,
    selectinload,
    contains_eager,
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_name = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.name!r} {self.last_name!r})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(
        Integer, ForeignKey("user_account.id")
    )  # Tutaj definiujemy relację z tabelą user_account

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


Base.metadata.create_all(engine)

adam = User(
    name="Adam", last_name="Driver", addresses=[Address(email_address="abc@gmail.com")]
)
david = User(name="David", last_name="Fincher", addresses=[])
sergio = User(
    name="Sergio",
    last_name="Leone",
    addresses=[
        Address(email_address="sergio@gmail.com"),
        Address(email_address="sergio@yahoo.com"),
    ],
)
robert = User(
    name="Robert",
    last_name="De Niro",
    addresses=[Address(email_address="robert@gmail.com")],
)


def populate_db(users: list[User]) -> None:
    with Session(engine) as session:
        session.add_all(users)
        session.commit()


populate_db([adam, david, sergio, robert])

session = Session(engine)

# LAZY
# user = session.execute(select(User).where(User.id == 3)).scalar_one()
# print("\n\n# # # #\n\n")
# for address in user.addresses:
#     print("\n\n# # # #\n\n")
#     print(address)
#     print("\n\n# # # #\n\n")

# addresses = session.execute(select(Address)).scalars()
# print("\n\n# # # #\n\n")
# for address in addresses:
#     print("\n\n# # # #\n\n")
#     print(address.user)
#     print("\n\n# # # #\n\n")


# EAGER
# users = session.execute(select(User).options(selectinload(User.addresses))).scalars()
# print("\n\n# # # #\n\n")
# for user in users:
#     print("\n\n# # # #\n\n")
#     print(user.addresses)
#     print("\n\n# # # #\n\n")


# addresses = session.execute(select(Address).options(joinedload(Address.user))).scalars()
# print("\n\n# # # #\n\n")
# for address in addresses:
#     print("\n\n# # # #\n\n")
#     print(address.user)
#     print("\n\n# # # #\n\n")

#
# addresses = session.execute(select(Address).join(Address.user).where(Address.id == 1).options(contains_eager(Address.user))).scalars()
# print("\n\n# # # #\n\n")
# for address in addresses:
#     print("\n\n# # # #\n\n")
#     print(address.user.name)
#     print("\n\n# # # #\n\n")
