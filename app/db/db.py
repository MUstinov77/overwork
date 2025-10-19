from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from fastapi.params import Depends

from app.db._base import Base


engine = create_engine("sqlite:///overwork.db")


def create_session():
    session = sessionmaker(engine)
    with session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def session_provider(session: Session = Depends(create_session)):
    return session


def init_db():
    Base.metadata.create_all(engine)

def destroy_db():
    Base.metadata.drop_all(engine)