"""add categories.

Revision ID: 0a8402945517
Revises: ab82b904a1a1
Create Date: 2023-02-12 16:19:25.686276

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.sql import table, column
import os
from tqdm import tqdm
import pandas as pd
import datetime

# revision identifiers, used by Alembic.
revision = '0a8402945517'
down_revision = 'ab82b904a1a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    op.execute("DELETE FROM category ")
    target_table = table(
        "category",
        column('id', BigInteger),
        column('name', String),
        column('desc', String),
        column('created_date', DateTime)
    )
    bulk_entries = []
    p = os.path.join("rawdata", "all_item_category_ids.csv")
    df = pd.read_csv(p)
    df = df.drop_duplicates()
    for i, r in tqdm(df.iterrows(), total=df.shape[0]):
        bulk_entries.append(
            {
                "id": int(r["category_id"]),
                "name": str(r["category_id"]),
                "desc": str(r["category_id"]),
                "created_date": datetime.datetime.now()
            }
        )

    op.bulk_insert(target_table, bulk_entries)


def downgrade() -> None:
    pass
