from sqlalchemy.orm import Session
from sqlalchemy_app.models import Zadanie


def search_phraze(db: Session, phrase: str):

    results = db.query(Zadanie).filter(Zadanie.opis.like(f"%{phrase}%")).all()
    return results
