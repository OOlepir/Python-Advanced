"""Add category_id to questions

Revision ID: 388d1b513ce4
Revises: 9a72df2b923c
Create Date: 2025-02-09 22:46:28.578297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '388d1b513ce4'
down_revision = '9a72df2b923c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_questions_category', 'categories', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_questions_category', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')
    # ### end Alembic commands ###
