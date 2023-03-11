"""added sessions.

Revision ID: a28db9d8a52f
Revises: 2dc35a1d2b42
Create Date: 2023-02-12 22:34:09.047965

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, BigInteger, String, DateTime, Integer, Float, Boolean
from tqdm import tqdm
import os
import pandas as pd
import datetime


# revision identifiers, used by Alembic.
revision = 'a28db9d8a52f'
down_revision = '2dc35a1d2b42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    op.execute("DELETE FROM session ")
    target_table = table(
        "session",
        column('id', BigInteger),
        column("session_ref_id", BigInteger),
        column("item_id", BigInteger),
        column("courier_id", BigInteger),
        column("price", Integer),
        column("qty", Integer),
        column("price_per_qty", Float),
        column("insurance", Boolean),
        column('created_date', DateTime),
    )
    bulk_entries = []
    p = os.path.join("rawdata", "all_buy_session.csv")
    df = pd.read_csv(p)
    df = df.drop_duplicates()
    for i, r in tqdm(df.iterrows(), total=df.shape[0]):
        bulk_entries.append(
            {
                "id": i + 1,
                "session_ref_id": int(r["session_id"]),
                "item_id": int(r["item_id"]),
                "courier_id": int(r["courier_id"]),
                "price": int(r["price"]),
                "qty": int(r["quantity"]),
                "price_per_qty": float(r["price_per_qty"]),
                "insurance": int(r["insurance"]),
                "created_date": datetime.datetime.strptime(str(r["timestamp"]), '%Y-%m-%dT%H:%M:%S.%fZ'),
            }
        )

    op.bulk_insert(target_table, bulk_entries)


def downgrade() -> None:
    pass
