from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
Database_URL = os.getenv("Database_URL")
engine = create_engine(Database_URL)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    from Backend import models 
    Base.metadata.create_all(bind=engine)