"""Initialize tables

Revision ID: ff31a6e15363
Revises: 
Create Date: 2024-05-28 12:45:59.441339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff31a6e15363'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)

    op.create_table(
        "file",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("access_key", sa.String(), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_unique_constraint("ix_file_access_key", "file", ["access_key"])

def downgrade() -> None:
    op.drop_constraint(constraint_name="ix_file_access_key", table_name='file', type_='unique')
    op.drop_table("file")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
