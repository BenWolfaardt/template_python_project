"""Instantiation

Revision ID: 970fab8ae7d2
Revises: 
Create Date: 2024-04-01 17:29:34.091985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '970fab8ae7d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('timestamp_created', sa.DateTime(), nullable=False),
    sa.Column('timestamp_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index('idx_id', 'data', ['id'], unique=False)
    op.create_index(op.f('ix_data_id'), 'data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_data_id'), table_name='data')
    op.drop_index('idx_id', table_name='data')
    op.drop_table('data')
    # ### end Alembic commands ###
