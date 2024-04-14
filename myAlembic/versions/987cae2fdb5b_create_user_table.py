"""create user table

Revision ID: 987cae2fdb5b
Revises:
Create Date: 2024-04-13 00:08:43.275880

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "987cae2fdb5b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(32), nullable=False, unique=True),
        sa.Column("hash_password", sa.String(128), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("delete", sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table("users")
