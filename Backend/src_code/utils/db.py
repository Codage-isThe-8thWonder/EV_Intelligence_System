from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src_code.utils.settings import settings

Base = declarative_base()

engine = create_engine(settings.DB_CONNECTION)

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()