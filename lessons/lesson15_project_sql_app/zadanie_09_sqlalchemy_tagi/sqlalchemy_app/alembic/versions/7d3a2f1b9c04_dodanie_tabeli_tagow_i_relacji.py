"""Dodanie tabeli tagow i relacji wiele do wielu

Revision ID: 7d3a2f1b9c04
Revises: fb2a817ff693
Create Date: 2026-05-29 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# To identyfikator tej migracji.
revision: str = "7d3a2f1b9c04"
# Ta migracja opiera sie na pierwszej migracji tabeli `zadania`.
down_revision: Union[str, Sequence[str], None] = "fb2a817ff693"
# Nie uzywamy dodatkowych etykiet galezi.
branch_labels: Union[str, Sequence[str], None] = None
# Nie mamy dodatkowych zaleznosci migracyjnych.
depends_on: Union[str, Sequence[str], None] = None


# Funkcja upgrade rozszerza schemat o tagi.
def upgrade() -> None:
    # Tworzymy tabele `tagi`.
    op.create_table(
        "tagi",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nazwa", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nazwa"),
    )
    # Tworzymy tabele posrednia do relacji wiele-do-wielu.
    op.create_table(
        "zadanie_tagi",
        sa.Column("zadanie_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["zadanie_id"], ["zadania.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tagi.id"]),
        sa.PrimaryKeyConstraint("zadanie_id", "tag_id"),
    )


# Funkcja downgrade cofa dodanie tagow.
def downgrade() -> None:
    # Najpierw usuwamy tabele posrednia, bo zalezy od pozostalych.
    op.drop_table("zadanie_tagi")
    # Potem usuwamy sama tabele `tagi`.
    op.drop_table("tagi")
