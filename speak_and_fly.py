from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# Używamy metody begin zamiast connection dzięki czemu na koniec bloku zmiany są komitowane w transakcji
with engine.begin() as conn:
    levels = """
    CREATE TABLE levels (
        id integer not null primary key autoincrement, 
        name varchar,
        description varchar
    );
    """

    languages = """
    CREATE TABLE languages (
        id integer not null primary key autoincrement, 
        name varchar
    );
    """

    categories = """
    CREATE TABLE categories (
        id integer not null primary key autoincrement, 
        name varchar
    );
    """

    courses = """
    CREATE TABLE courses (
        id integer not null primary key autoincrement, 
        lessons integer,
        description varchar,
        language_id integer, 
        category_id integer, 
        level_id integer,
        foreign key (language_id) references languages(id),
        foreign key (category_id) references categories(id),
        foreign key (lavel_id) references levels(id)
    );
    """

    conn.execute(text(levels))
    conn.execute(text(languages))
    conn.execute(text(categories))
    conn.execute(text(courses))
    conn.execute(
        text("INSERT INTO levels (name) VALUES (:name)"),
        [{"name": "A1"}, {"name": "B2"}],
    )


with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM levels")).all()
    for row in result:
        print(f"id: {row.id}, name: {row.name}")
