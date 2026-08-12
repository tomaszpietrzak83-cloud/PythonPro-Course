from sqlalchemy.orm import Session
from sqlalchemy_app.models import Zadanie


def delete_task(db: Session, id_zadania: int):
    task = db.query(Zadanie).filter(Zadanie.id == id_zadania).first()
    if task:
        db.delete(task)
        db.commit()
        print(f"Zadanie o ID {id_zadania} zostało usunięte.")
    else:
        print("Zadanie o podanym ID nie istnieje.")
