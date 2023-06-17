import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.enviroment.config import user, password, host, port, schema

Base = declarative_base()


def get_db():
    db = Database.get_instance().Session()
    try:
        yield db
    finally:
        db.close()


class Database:
    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            self.engine = create_engine(
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema}"
            )
            self.Session = sessionmaker(bind=self.engine)
            self.Base = declarative_base()
