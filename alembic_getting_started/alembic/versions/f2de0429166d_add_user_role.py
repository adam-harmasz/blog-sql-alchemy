"""add user role

Revision ID: f2de0429166d
Revises: 464743aed61b
Create Date: 2022-01-21 23:32:48.608404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f2de0429166d"
down_revision = "464743aed61b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("role", sa.Enum("author", "reader"), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")
    # ### end Alembic commands ###
