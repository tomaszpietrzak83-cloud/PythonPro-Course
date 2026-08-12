from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True)
    opis = Column(String, nullable=False)
    zrobione = Column(Boolean, default=False, nullable=False)
    # Domyślnie zapisz lokalny czas utworzenia bez mikrosekund.
    # Używamy `datetime.now()` (lokalny, naive) i usuwamy microsecond,
    # aby w DB były tylko: rok-miesiąc-dzień godzina:minuta:sekunda.
    creation_time = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
    )

    def __repr__(self):
        return f"<Zadanie(id={self.id}, opis='{self.opis}', zrobione={self.zrobione})>"
