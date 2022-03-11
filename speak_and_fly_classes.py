from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    Float,
    ForeignKey, create_engine, Date,
)
from sqlalchemy.orm import relationship, declarative_base, Session

Base = declarative_base()
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
session = Session(bind=engine)


class Levels(Base):
    __tablename__ = "levels"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="level")

    def __repr__(self):
        return f"Level(id: {self.id}, name: {self.name})"


class Languages(Base):
    __tablename__ = "languages"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="language")

    def __repr__(self):
        return f"Language(id: {self.id}, name: {self.name})"


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship("Courses", back_populates="category")

    def __repr__(self):
        return f"Category(id: {self.id}, name: {self.name})"


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    nr_of_lessons = Column(Integer, nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)

    language = relationship("Languages", back_populates="courses")
    category = relationship("Categories", back_populates="courses")
    level = relationship("Levels", back_populates="courses")

    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"Course(id: {self.id}, level: {self.level}, lang: {self.language})"


Base.metadata.create_all(bind=engine)

###############################################################

LEVELS_DATA = (
    {"name": "A0"},
    {"name": "A1"},
    {"name": "A2"},
    {"name": "B1"},
    {"name": "B2"},
    {"name": "C1"},
    {"name": "C2"},
)

LANG_DATA = (
    {"name": "English"},
    {"name": "German"},
    {"name": "Spanish"},
    {"name": "Italian"},
)

CATEGORIES_DATA = (
    {"name": "Evening"},
    {"name": "Regular"},
    {"name": "Weekend"},
)

COURSE_DATA = (
    {
        "nr_of_lessons": 56,
        "description": "Very nice",
        "price": 1000,
        "language_id": 1,
        "level_id": 1,
        "category_id": 1,
    },
    {
        "nr_of_lessons": 65,
        "description": "Very very nice",
        "price": 10_000,
        "language_id": 2,
        "level_id": 2,
        "category_id": 2,
    },
    {
        "nr_of_lessons": 560,
        "description": "Very well",
        "price": 100,
        "language_id": 3,
        "level_id": 3,
        "category_id": 3,
    },
    {
        "nr_of_lessons": 5656,
        "description": "Good enough",
        "price": 123,
        "language_id": 1,
        "level_id": 2,
        "category_id": 3,
    },
)


def get_level_objects():
    return [Levels(**level) for level in LEVELS_DATA]


def create_levels():
    session.add_all(get_level_objects())
    session.commit()


def get_lang_objects():
    return [Languages(**lang) for lang in LANG_DATA]


def create_langs():
    session.add_all(get_lang_objects())
    session.commit()


def get_categories_objects():
    return [Categories(**category) for category in CATEGORIES_DATA]


def create_categories():
    session.add_all(get_categories_objects())
    session.commit()


def get_course_objects():
    return [Courses(**course) for course in COURSE_DATA]


def create_courses():
    session.add_all(get_course_objects())
    session.commit()


def create_basic_data():
    create_levels()
    create_langs()
    create_categories()
    create_courses()


create_basic_data()
courses = session.query(Courses).all()
for course in courses:
    print(course)