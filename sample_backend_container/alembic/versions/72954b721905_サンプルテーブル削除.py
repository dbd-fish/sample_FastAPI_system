"""サンプルテーブル削除

Revision ID: 72954b721905
Revises: 8f8b96d4714d
Create Date: 2024-11-13 14:08:07.313058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72954b721905'
down_revision: Union[str, None] = '8f8b96d4714d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sample_table2およびsample_table3に依存するsample_tableを削除
    op.execute("DROP TABLE IF EXISTS sample_table2 CASCADE")
    op.execute("DROP TABLE IF EXISTS sample_table3 CASCADE")
    op.execute("DROP TABLE IF EXISTS sample_table CASCADE")


def downgrade() -> None:
    # 各テーブルの再作成
    op.create_table('sample_table2',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('related_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['related_id'], ['sample_table.id'], name='sample_table2_related_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='sample_table2_pkey')
    )
    op.create_index('ix_sample_table2_id', 'sample_table2', ['id'], unique=False)
    
    op.create_table('sample_table3',
        sa.Column('idsss', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('namesss', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('descriptionsss', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('idsss', name='sample_table3_pkey')
    )
    op.create_index('ix_sample_table3_namesss', 'sample_table3', ['namesss'], unique=False)
    op.create_index('ix_sample_table3_idsss', 'sample_table3', ['idsss'], unique=False)
    
    op.create_table('sample_table',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='sample_table_pkey')
    )
    op.create_index('ix_sample_table_name', 'sample_table', ['name'], unique=False)
    op.create_index('ix_sample_table_id', 'sample_table', ['id'], unique=False)
