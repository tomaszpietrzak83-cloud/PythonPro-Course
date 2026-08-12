"""Utworzenie tabeli zadan

Revision ID: fb2a817ff693
Revises:
Create Date: 2026-05-29 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# To unikalny identyfikator tej migracji.
revision: str = "fb2a817ff693"
# Pierwsza migracja nie ma poprzednika.
down_revision: Union[str, Sequence[str], None] = None
# Dodatkowe etykiety galezi nie sa tu potrzebne.
branch_labels: Union[str, Sequence[str], None] = None
# Ta migracja nie zalezy od innych migracji.
depends_on: Union[str, Sequence[str], None] = None


# Funkcja upgrade tworzy poczatkowy schemat bazy.
def upgrade() -> None:
    # Tworzymy tabele `zadania`.
    op.create_table(
        "zadania",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opis", sa.String(), nullable=False),
        sa.Column("zrobione", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("creation_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


# Funkcja downgrade odwraca to, co zrobil upgrade.
def downgrade() -> None:
    # Usuwamy tabele `zadania`.
    op.drop_table("zadania")
