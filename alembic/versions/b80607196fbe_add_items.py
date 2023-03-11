"""add items.

Revision ID: b80607196fbe
Revises: 0a8402945517
Create Date: 2023-02-12 16:58:08.954070

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import BigInteger, Integer, String, table, column, DateTime
import pandas as pd
from tqdm import tqdm
import datetime
import os


# revision identifiers, used by Alembic.
revision = 'b80607196fbe'
down_revision = '0a8402945517'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    op.execute("DELETE FROM item ")
    target_table = table(
        "item",
        column('id', BigInteger),
        column('name', String),
        column('price_per_qty', String),
        column('created_date', DateTime),
        column('cat_id', BigInteger)
    )
    bulk_entries = []
    p = os.path.join("rawdata", "all_item_ids.csv")
    df = pd.read_csv(p)
    df = df.drop_duplicates()
    for i, r in tqdm(df.iterrows(), total=df.shape[0]):
        bulk_entries.append(
            {
                "id": int(r["item_id"]),
                "name": str(r["item_id"]),
                "price_per_qty": 0,
                "created_date": datetime.datetime.now(),
                "cat_id": int(r["cat_id"])
            }
        )

    op.bulk_insert(target_table, bulk_entries)


def downgrade() -> None:
    pass
