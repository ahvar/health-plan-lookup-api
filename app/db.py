import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


class Model(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


def _resolve_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///health_plans.db")


engine = create_engine(_resolve_database_url())
Session = sessionmaker(bind=engine)
