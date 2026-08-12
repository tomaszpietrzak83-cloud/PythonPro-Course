from database import engine
from models import Base, Registry

Base.metadata.create_all(bind=engine)
