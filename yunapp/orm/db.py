# -*- coding:utf-8 -*-
# __author__ = 'micheal'

from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, \
    VARCHAR, INTEGER
import time

_metadata = None

if not _metadata:
    _metadata = MetaData()

t_lxuser = Table('lxuser', _metadata,
                 Column('id', INTEGER, primary_key=True, autoincrement=True),
                 Column('type', TINYINT(10), nullable=False),
                 Column('userName', VARCHAR(64), nullable=False),
                 Column('realName', VARCHAR(64), nullable=False),
                 Column('passwd', VARCHAR(64), nullable=False),
                 Column('email', VARCHAR(64), nullable=False),
                 Column('phone', VARCHAR(32)),
                 Column('parentUserId', INTEGER, nullable=False),
                 Column('companyId', INTEGER, nullable=False),
                 Column('signId', INTEGER, ),
                 Column('status', TINYINT, ),
                 Column('createTime', TIMESTAMP, nullable=False, default='0000-00-00 00:00:00'),
                 Column('modifyTime', TIMESTAMP, nullable=False,
                        default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                 mysql_engine='InnoDB',)

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