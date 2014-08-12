#-*- coding:utf-8 -*-
# __author__ = 'micheal'

from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String, TIMESTAMP

_metadata = None

if not _metadata:
    _metadata = MetaData()


t_lxuser = Table('lxuser', _metadata,
    Column('id', Integer, primary_key=True),
    Column('bound_task_id', Integer),
    Column('expression_def', String(2048)),
    Column('expression', String(2048)),
    Column('gmt_create', TIMESTAMP),
    Column('gmt_modify', TIMESTAMP),
    mysql_engine='InnoDB',
)