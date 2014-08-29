# -*- coding:utf-8 -*-
# __author__ = 'micheal'

from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, \
    VARCHAR, INTEGER
import time

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

_metadata = None

if not _metadata:
    _metadata = MetaData()



t_lxfile = Table('lxfile', _metadata,

                 Column('fuuid', VARCHAR(32)),
                 Column('type', TINYINT),
                 Column('name', VARCHAR(64)),
                 Column('extension', VARCHAR(8)),
                 Column('fpath', VARCHAR(256)),

                 mysql_engine='InnoDB',
)


t_lxtemptype = Table('lxtemptype', _metadata,

                 Column('name', VARCHAR(64)),
                 Column('level', TINYINT),
                 Column('status', TINYINT),

                 Column('parent_id', INTEGER, ForeignKey('lxtemptype.id') ),
                 mysql_engine='InnoDB',
)

t_lxtemplate = Table('lxtemplate', _metadata,
                 Column('id', INTEGER, primary_key=True),
                 Column('name', VARCHAR(64)),
                 Column('content', TEXT),
                 Column('status', TINYINT),
                 Column('gmt_create', TIMESTAMP, nullable=False,default=current_time),
                 Column('gmt_modify', TIMESTAMP, nullable=False,default=current_time),
                 Column('type_id', INTEGER, ForeignKey('lxtemptype.id') ),
                 Column('owner_id', INTEGER, ForeignKey('lxuser.id') ),
                 mysql_engine='InnoDB',
)

t_lxemial =Table('lxemail',_metadata,
                 Column('id', INTEGER, primary_key=True),
                 Column('eFrom', VARCHAR(50),nullable=False),
                 Column('eTo', VARCHAR(50),nullable=False),
                 Column('eSubject', VARCHAR(50),nullable=False),
                 Column('eContent', VARCHAR(50),nullable=False),
                 Column('eSentTime',TIMESTAMP,nullable=False,default=current_time),
)