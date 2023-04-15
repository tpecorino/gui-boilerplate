from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
TABLE_NAME = "characters"


class Character(Base):
    __tablename__ = TABLE_NAME

    id = Column("id", Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    name = Column("name", String(25))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Todo(id={self.id!r}, name={self.name!r},"


def seed_database(db):
    character_1 = Character("Picard")
    character_2 = Character("Riker")
    character_3 = Character("Data")
    character_4 = Character("Worf")

    db.add(character_1)
    db.add(character_2)
    db.add(character_3)
    db.add(character_4)
    db.commit()


def fetch_characters(db):
    return db.query(Character).all()


def fetch_entity_by_id(db, pk):
    return db.query(Character).filter(Character.id == pk).first()


def update_character(db, pk, updated_character):
    db.query(Character).filter(Character.id == pk).update({
        "name": updated_character.name
    })
    db.commit()


def get_database_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    table_exists = inspect(engine).has_table(TABLE_NAME)
    character_data = fetch_characters(session)

    if not character_data:
        seed_database(session)

    for Character in character_data:
        print(f"Character: {Character.name}")
