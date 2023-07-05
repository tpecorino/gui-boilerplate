from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/db.sqlite"
TABLE_NAME = "graphs"


class Graph(Base):
    __tablename__ = TABLE_NAME

    id = Column("id", Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    title = Column("title", String(25))
    x_axis_label = Column("x_axis_label", String(25))
    y_axis_label = Column("y_axis_label", String(25))
    x_axis_values = Column("x_axis_values", String(250))
    y_axis_values = Column("y_axis_values", String(250))

    def __init__(self, title, x_axis_label, y_axis_label, x_axis_values, y_axis_values):
        self.title = title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.x_axis_values = x_axis_values
        self.y_axis_values = y_axis_values

    def __repr__(self):
        return f"Graph" \
               f"(id={self.id!r}, " \
               f"title={self.title!r}, " \
               f"x_axis_label={self.x_axis_label!r}, " \
               f"y_axis_label={self.y_axis_label!r}," \
               f"x_axis_label={self.x_axis_values!r}," \
               f"y_axis_label={self.y_axis_values!r},"


# def seed_database(db):
#     character_1 = Graph("Graph 1", 'amount', 'months')
#
#     db.add(character_1)
#     db.commit()


def fetch_graphs(db):
    return db.query(Graph).all()


def fetch_entity_by_id(db, pk):
    return db.query(Graph).filter(Graph.id == pk).first()


def update_graph(db, pk, updated_character):
    db.query(Graph).filter(Graph.id == pk).update(updated_character)
    db.commit()


def save_graph(db, graph):
    graph = Graph(graph["title"], graph["x_axis_label"], graph["y_axis_label"], graph["x_axis_values"],
                  graph["y_axis_values"])
    db.add(graph)
    db.commit()
    return graph


def delete_graph(db, graph_id):
    db.query(Graph).filter(Graph.id == graph_id).delete()
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
    graph_data = fetch_graphs(session)

    # if not graph_data:
    #     seed_database(session)

    for Graph in graph_data:
        print(f"Graph: {Graph.name}")
