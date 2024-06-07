"""autogenerated

Revision ID: 7fb89d0d774f
Revises:
Create Date: 2024-06-06 23:59:39.622283

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7fb89d0d774f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "example",
        sa.Column("pk_example", sa.String(length=50), nullable=False),
        sa.Column("string_example", sa.String(length=128), nullable=True),
        sa.Column("string2_example", sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint("pk_example"),
    )
    op.create_index(
        op.f("ix_example_string2_example"),
        "example",
        ["string2_example"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_example_string2_example"), table_name="example")
    op.drop_table("example")
    # ### end Alembic commands ###