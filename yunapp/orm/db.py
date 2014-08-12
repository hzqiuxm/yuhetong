#-*- coding:utf-8 -*-
# __author__ = 'micheal'

import sqlalchemy as sa
from sqlalchemy import MetaData

_metadata = None

if not _metadata:
    _metadata = MetaData()


t_lxuser = sa.Table('lxuser', _metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('bound_task_id', sa.types.Integer),
    sa.Column('expression_def', sa.types.String(2048)),
    sa.Column('expression', sa.types.String(2048)),
    sa.Column('gmt_create', sa.types.TIMESTAMP),
    sa.Column('gmt_modify', sa.types.TIMESTAMP),
    mysql_engine='InnoDB',
)