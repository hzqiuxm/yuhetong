#-*- coding:utf-8 -*-
# __author__ = 'micheal'

from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, \
    VARCHAR, INTEGER

_metadata = None

if not _metadata:
    _metadata = MetaData()


t_lxuser = Table('lxuser', _metadata,
    Column('id', INTEGER, primary_key=True),
    Column('type', TINYINT),
    Column('userName', VARCHAR(64)),
    Column('realName', VARCHAR(64)),
    Column('passwd', VARCHAR(64)),
    Column('email', VARCHAR(64)),
    Column('phone', VARCHAR(32)),
    Column('parentUserId', INTEGER),
    Column('companyId', INTEGER),
    Column('signId', INTEGER),
    Column('status', TINYINT),
    Column('createTime', TIMESTAMP),
    Column('modifyTime', TIMESTAMP),
    mysql_engine='InnoDB',
)

t_lxfile = Table('lxfile', _metadata,
    Column('id', INTEGER, primary_key=True),
    Column('fuuid', VARCHAR(32)),
    Column('type', TINYINT),
    Column('name', VARCHAR(64)),
    Column('status', TINYINT),
    Column('createTime', TIMESTAMP),
    Column('modifyTime', TIMESTAMP),
    mysql_engine='InnoDB',
)