from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

@event.listens_for(engine, "connect")
def _enable_fks(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_tables():
    import app.models
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
