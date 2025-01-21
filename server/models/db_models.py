import sqlalchemy

metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    'posts',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column('publication_date', sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column('content', sqlalchemy.Text(), nullable=False),
)

comments = sqlalchemy.Table(
    'comments',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column('post_id', sqlalchemy.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('publication_date', sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column('content', sqlalchemy.Text(), nullable=False),
)
