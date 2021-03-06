"""empty message

Revision ID: 86a9d56883b9
Revises: 9701a1860e6a
Create Date: 2019-04-05 01:40:06.049366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86a9d56883b9'
down_revision = '9701a1860e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SubjectExperts',
    sa.Column('FileId', sa.BigInteger(), nullable=False),
    sa.Column('AuthorId', sa.BigInteger(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['AuthorId'], ['Authors.AuthorId'], ),
    sa.ForeignKeyConstraint(['FileId'], ['Files.FileId'], ),
    sa.PrimaryKeyConstraint('AuthorId', 'FileId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('SubjectExperts')
    # ### end Alembic commands ###
