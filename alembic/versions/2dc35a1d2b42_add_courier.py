"""add courier.

Revision ID: 2dc35a1d2b42
Revises: b80607196fbe
Create Date: 2023-02-12 19:30:13.997451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, BigInteger, Integer, String, DateTime
from tqdm import tqdm
import os
import pandas as pd
import datetime


# revision identifiers, used by Alembic.
revision = '2dc35a1d2b42'
down_revision = 'b80607196fbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    # pass
    op.execute("DELETE FROM courier ")
    target_table = table(
        "courier",
        column('id', BigInteger),
        column('name', String),
        column('created_date', DateTime),
    )
    bulk_entries = []
    p = os.path.join("rawdata", "all_courier_ids.csv")
    df = pd.read_csv(p)
    df = df.drop_duplicates()
    for i, r in tqdm(df.iterrows(), total=df.shape[0]):
        bulk_entries.append(
            {
                "id": int(r["courier_id"]),
                "name": str(r["courier_name"]),
                "created_date": datetime.datetime.now(),
            }
        )

    op.bulk_insert(target_table, bulk_entries)



def downgrade() -> None:
    pass
