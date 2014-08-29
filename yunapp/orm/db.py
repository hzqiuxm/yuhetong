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

t_lxcompany = Table('lxcompany', _metadata,
                    Column('id', INTEGER, primary_key=True),
                    Column('type', TINYINT),
                    Column('name', VARCHAR(128)),
                    Column('orzNo', VARCHAR(20)),
                    Column('orzimg', VARCHAR(100)),
                    Column('yyzyNo', VARCHAR(20)),
                    Column('yyzyimg', VARCHAR(100)),
                    Column('legal_person', VARCHAR(80)),
                    Column('create_time', TIMESTAMP),
                    Column('modify_time', TIMESTAMP),
                    Column('status', TINYINT),
                    mysql_engine='InnoDB',
)
t_lxuser = Table('lxuser', _metadata,
                 Column('id', INTEGER, primary_key=True, autoincrement=True),
                 Column('type', TINYINT(10), nullable=False),
                 Column('username', VARCHAR(64), nullable=False, unique=True),
                 Column('real_name', VARCHAR(64)),
                 Column('passwd', VARCHAR(128), nullable=False),
                 Column('email', VARCHAR(64), nullable=False),
                 Column('phone', VARCHAR(32)),
                 Column('idCardNo', VARCHAR(20)),
                 Column('idCardimg1', VARCHAR(100)),
                 Column('idCardimg2', VARCHAR(100)),
                 Column('shouhanimg', VARCHAR(100)),
                 Column('address', VARCHAR(100)),
                 Column('parent_user_id', INTEGER, nullable=False),
                 Column('sign_id', INTEGER ),
                 Column('status', TINYINT ),
                 Column('create_time', TIMESTAMP, nullable=False, default='0000-00-00 00:00:00'),
                 Column('modify_time', TIMESTAMP, nullable=False,
                        default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                 Column('company_id', INTEGER, ForeignKey('lxcompany.id') ),
                 mysql_engine='InnoDB',)

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