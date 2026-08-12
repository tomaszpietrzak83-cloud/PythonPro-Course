from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class Registry(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def add_registry(self, db: Session, name: str, email: str):
        existing = (
            db
            .query(Registry)
            .filter(Registry.name == name, Registry.email == email)
            .first()
        )

        if existing:
            return "Registry entry already exists"

        self.name = name
        self.email = email

        db.add(self)
        db.commit()
        db.refresh(self)
        return self
