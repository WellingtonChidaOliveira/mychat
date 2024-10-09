from .database import Base, engine
from ..domain.user import User  

def init_db():
    Base.metadata.create_all(bind=engine)