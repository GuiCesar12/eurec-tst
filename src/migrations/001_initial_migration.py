from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('di_publications',
        sa.Column('id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('idOficio', sa.Text(), nullable=True),
        sa.Column('pubName', sa.Text(), nullable=True),
        sa.Column('artType', sa.Text(), nullable=True),
        sa.Column('pubDate', sa.DateTime(), nullable=True),
        sa.Column('artClass', sa.Text(), nullable=True),
        sa.Column('artCategory', sa.Text(), nullable=True),
        sa.Column('artSize', sa.Text(), nullable=True),
        sa.Column('artNotes', sa.Text(), nullable=True),
        sa.Column('numberPage', sa.Text(), nullable=True),
        sa.Column('pdfPage', sa.Text(), nullable=True),
        sa.Column('editionNumber', sa.Text(), nullable=True),
        sa.Column('highlightType', sa.Text(), nullable=True),
        sa.Column('highlightPriority', sa.Text(), nullable=True),
        sa.Column('highlight', sa.Text(), nullable=True),
        sa.Column('highlightimage', sa.Text(), nullable=True),
        sa.Column('highlightimagename', sa.Text(), nullable=True),
        sa.Column('idMateria', sa.Text(), nullable=True),
        sa.Column('body', sa.JSON(), nullable=True),
        sa.Column('midias', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('di_publications')