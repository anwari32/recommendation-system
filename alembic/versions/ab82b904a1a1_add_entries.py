"""add entries.

Revision ID: ab82b904a1a1
Revises: 709917c116e6
Create Date: 2023-02-11 19:28:19.087777

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, BigInteger, Integer, DateTime
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'ab82b904a1a1'
down_revision = '709917c116e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    # add session id entries.
    import pandas as pd
    import os
    from datetime import datetime
    from tqdm import tqdm

    session_ref_table = table(
        "session_ref",
        column('id', BigInteger),
        column('created_date', DateTime)
    )
    bulk_entries = []
    p = os.path.join("rawdata", "all_session.csv")
    all_session_ids_df = pd.read_csv(p)
    for i, r in tqdm(all_session_ids_df.iterrows(), total=all_session_ids_df.shape[0]):
        bulk_entries.append(
            {
                "id": int(r["session_id"]),
                "created_date": datetime.now()
            }
        )

    op.bulk_insert(session_ref_table, bulk_entries)


def downgrade() -> None:
    pass
