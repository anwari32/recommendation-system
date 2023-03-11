"""init table.

Revision ID: 709917c116e6
Revises: 
Create Date: 2023-02-10 21:13:45.097587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '709917c116e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    op.execute("DROP TABLE category CASCADE")
    op.create_table(
        "category",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("created_date", sa.DateTime),
        sa.Column("name", sa.String),
        sa.Column("desc", sa.String)
        )

    op.execute("DROP TABLE courier CASCADE")
    op.create_table(
        "courier",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("created_date", sa.DateTime),
        sa.Column("name", sa.String)
    )

    op.execute("DROP TABLE item CASCADE")
    op.create_table(
        "item",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("created_date", sa.DateTime),
        sa.Column("name", sa.String),
        sa.Column("cat_id", sa.Integer)
    )

    op.create_foreign_key(
        "fk_item_category",
        "item",
        "category",
        ["cat_id"],
        ["id"]
    )

    op.execute("DROP TABLE session_ref CASCADE")
    op.create_table(
        "session_ref",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("created_date", sa.DateTime)
    )

    op.execute("DROP TABLE session CASCADE")
    op.create_table(
        "session",
        sa.Column("id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("created_date", sa.DateTime),
        sa.Column("session_ref_id", sa.BigInteger),
        sa.Column("item_id", sa.BigInteger),
        sa.Column("price", sa.Integer),
        sa.Column("qty", sa.Integer),
        sa.Column("price_per_qty", sa.Float),
        sa.Column("courier_id", sa.BigInteger),
        sa.Column("insurance", sa.Boolean),
    )

    op.create_foreign_key(
        "fk_session_ref",
        "session",
        "session_ref",
        ["session_ref_id"],
        ["id"]
    )
    
    op.create_foreign_key(
        "fk_item_session",
        "session",
        "item",
        ["item_id"],
        ["id"]
    )

    op.create_foreign_key(
        "fk_courier_session",
        "session",
        "courier",
        ["courier_id"],
        ["id"]
    )

def downgrade() -> None:
    # pass
    op.execute("DROP TABLE session CASCADE")
    op.execute("DROP TABLE session_ref CASCADE")
    op.execute("DROP TABLE item CASCADE")
    op.execute("DROP TABLE courier CASCADE")
    op.execute("DROP TABLE category CASCADE")
