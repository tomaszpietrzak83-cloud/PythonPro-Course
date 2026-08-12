from database import engine
from models import Base, Product

Base.metadata.create_all(bind=engine)
