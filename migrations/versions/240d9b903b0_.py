"""empty message

Revision ID: 240d9b903b0
Revises: None
Create Date: 2015-06-01 18:51:59.153944

"""

# revision identifiers, used by Alembic.
revision = '240d9b903b0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    op.create_unique_constraint(None, 'users', ['email'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    ### end Alembic commands ###