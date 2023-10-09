from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

variables = dotenv_values('.env')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{variables.get('USERNAME')}:{variables.get('PASSWORD')}@{variables.get('SERVER')}/{variables.get('DATABASE')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

class ConectDatabase:
    __instance: sessionLocal = None

    @staticmethod
    def getInstance():
        if ConectDatabase.__instance == None:
            ConectDatabase()
        return ConectDatabase.__instance
    def __init__(self):
        if ConectDatabase.__instance != None:
            raise Exception("ConnectDatabase exists already")
        else:
            ConectDatabase.__instance = sessionLocal()