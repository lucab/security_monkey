"""populate association table

Revision ID: 2829e0a7d726
Revises: 595e27f36454
Create Date: 2015-02-23 15:11:18.758140

"""

# revision identifiers, used by Alembic.
revision = '2829e0a7d726'
down_revision = '595e27f36454'

import logging
logger = logging.getLogger("alembic")
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


association_table = table('association',
                             column('user_id', sa.Integer, sa.ForeignKey('user.id')),
                             column('account_id', sa.Integer, sa.ForeignKey('account.id'))
)


def upgrade():
    conn = op.get_bind()

    q1 = conn.execute("select count(*) from association")
    rows = q1.fetchall()
    if rows[0][0] > 0:
        logger.info("Table already contains %d associations, not touching it" % rows[0][0])
        return

    q2 = conn.execute("select id, email from \"user\" where active=true")
    users = q2.fetchall()
    q3 = conn.execute("select id from account")
    accounts = q3.fetchall()
    if not users or not accounts:
        logger.info("No user/account to associate, skipping")
        return

    assoc = []
    for u in users:
        logger.info("Assigning %d account(s) to user '%s'" % (len(accounts), u[1]))
        for a in accounts:
            assoc.append({'user_id': int(u[0]), 'account_id': int(a[0])})
    op.bulk_insert(association_table, assoc)


def downgrade():
    pass
