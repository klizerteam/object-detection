from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

Database_URL ="postgresql://analyzer_user:analyzer123@localhost:5432/Object_detection"

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
    import models 
    Base.metadata.create_all(bind=engine)