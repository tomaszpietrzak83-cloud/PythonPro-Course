# Importujemy datetime, aby ustawic czas utworzenia zadania.
from datetime import datetime

# Importujemy elementy potrzebne do zdefiniowania kolumn i tabel.
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)

# Importujemy deklaratywna baze i relacje ORM.
from sqlalchemy.orm import declarative_base, relationship

# Tworzymy wspolna baze dla wszystkich modeli.
Base = declarative_base()


# Tabela posrednia zapisuje same powiazania miedzy zadaniami i tagami.
zadanie_tagi = Table(
    # Nazwa tabeli w bazie danych.
    "zadanie_tagi",
    # MetaData pochodzi z Base i zbiera wszystkie definicje tabel.
    Base.metadata,
    # Kolumna przechowuje ID zadania.
    Column("zadanie_id", Integer, ForeignKey("zadania.id"), primary_key=True),
    # Kolumna przechowuje ID taga.
    Column("tag_id", Integer, ForeignKey("tagi.id"), primary_key=True),
)


# Model Zadanie odwzorowuje tabele `zadania`.
class Zadanie(Base):
    # Okreslamy nazwe tabeli.
    __tablename__ = "zadania"

    # Klucz glowny rekordu.
    id = Column(Integer, primary_key=True)
    # Opis zadania jest wymagany.
    opis = Column(String, nullable=False)
    # Status wykonania ma domyslnie wartosc False.
    zrobione = Column(Boolean, default=False, nullable=False)
    # Zapisujemy czas utworzenia rekordu bez mikrosekund.
    creation_time = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    # Definiujemy relacje wiele-do-wielu do modelu Tag.
    tagi = relationship("Tag", secondary=zadanie_tagi, back_populates="zadania")

    # Reprezentacja tekstowa pomaga w debugowaniu.
    def __repr__(self) -> str:
        # Zwracamy czytelny napis z najwazniejszymi polami.
        return f"<Zadanie(id={self.id}, opis='{self.opis}', zrobione={self.zrobione})>"


# Model Tag odwzorowuje tabele `tagi`.
class Tag(Base):
    # Okreslamy nazwe tabeli.
    __tablename__ = "tagi"

    # Klucz glowny taga.
    id = Column(Integer, primary_key=True)
    # Nazwa taga ma byc wymagana i unikalna.
    nazwa = Column(String, nullable=False, unique=True)
    # Definiujemy relacje zwrotna do modelu Zadanie.
    zadania = relationship(
        "Zadanie", secondary=zadanie_tagi, back_populates="tagi"
    )

    # Reprezentacja tekstowa pomaga przy debugowaniu.
    def __repr__(self) -> str:
        # Zwracamy krotki opis obiektu.
        return f"<Tag(id={self.id}, nazwa='{self.nazwa}')>"
