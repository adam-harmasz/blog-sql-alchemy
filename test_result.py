from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, relationship, declarative_base

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()


class Courses(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True)
    lessons = Column(String)
    description = Column(String)
    language_id = Column(Integer, ForeignKey("Languages.id"))
    category_id = Column(Integer, ForeignKey("Categories.id"))
    level_id = Column(Integer, ForeignKey("Levels.id"))
    start_date = Column(String)
    end_date = Column(String)
    price = Column(Integer)

    Levels = relationship("Levels", back_populates="courses")
    Languages = relationship("Languages", back_populates="courses")
    Categories = relationship("Categories", back_populates="courses")

    def __repr__(self):
        return (
            f"User(id={self.id!r}, lessons={self.lessons!r}, description={self.description!r},"
            f"start_date={self.start_date!r}, end_date={self.end_date!r}, price={self.pricen!r})"
        )


class Levels(Base):
    __tablename__ = "Levels"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    courses = relationship(Courses, back_populates="Levels")

    def __repr__(self):
        return f"Levels(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Languages(Base):
    __tablename__ = "Languages"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship(Courses, back_populates="Languages")

    def __repr__(self):
        return f"Languages(id={self.id!r}, name={self.name!r})"


class Categories(Base):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship(Courses, back_populates="Categories")

    def __repr__(self):
        return f"Categories(id={self.id!r}, name={self.name!r})"


Base.metadata.create_all(engine)

print(Courses.__table__.c.keys())
