# -*- coding:utf-8 -*-

import logging
from yunapp import config
from yunapp.yunapps import app
from flask.ext.login import UserMixin  # UserMixin 封装了 Flask-login 里面 用户类的一些基本方法，我们的User类要继承他
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import  Column, ForeignKey, func, String, Integer,  Text
from sqlalchemy.orm import backref, relationship
# from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, VARCHAR, INTEGER
from yunapp.orm.db_base import LxMixin

logger = logging.getLogger('ORM.MODEL')
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

db = SQLAlchemy(app)


class LxUser(db.Model, UserMixin, LxMixin):
    __tablename__ = 'lxuser'

    cols = ['id', 'type', 'username', 'real_name', 'passwd', 'email',
            'phone', 'parent_user_id', 'company', 'gmt_create',
            'gmt_modify', 'sign_id', 'status', ]
    type = Column(Integer)
    username = Column(String(128), nullable=False, unique=True)
    real_name = Column(String(128))
    passwd = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False)
    phone = Column(String(32))

    parent_id = Column(Integer, ForeignKey('lxuser.id'), nullable=True)
    parent = relationship('LxUser', remote_side='LxUser.id')

    sign = relationship('LxSign', uselist=False, backref='owner')
    # one to one relationship

    company = relationship('LxCompany')
    company_id = Column(Integer, ForeignKey('lxcompany.id'), nullable=True)
    # many to one relationship

class LxCompany(db.Model, LxMixin):
    __tablename__ = 'lxcompany'

    cols = ['id', 'type', 'name', 'gmt_create',
            'gmt_modify', 'status', ]
    type = Column(Integer)
    name = Column(String(255), nullable=False, unique=True)
    # owner_id = Column(Integer, ForeignKey('lxuser.id'))

class LxSign(db.Model, LxMixin):
    __tablename__ = 'lxsign'
    owner_id = Column(Integer, ForeignKey('lxuser.id'))

class LxFile(db.Model, LxMixin):
    __tablename__ = 'lxfile'

    cols = ['id', 'fuuid', 'type', 'name', 'gmt_create', 'gmt_modify',
            'status', ]
    type = Column(Integer)
    fuuid = Column(String(64), nullable=False, unique=True)
    name = Column(String(64), nullable=False)
    extension = Column(String(8), nullable=False)
    fpath = Column(String(256), nullable=False)

class LxTempType(db.Model, LxMixin):
    __tablename__ = 'lxtemptype'

    cols = ['id', 'name', 'level', 'parent', 'gmt_create', 'gmt_modify',
            'status']
    level = Column(Integer)
    name = Column(String(64), nullable=False)

    parent_id = Column(Integer, ForeignKey('lxtemptype.id'), nullable=True)
    parent = relationship('LxTempType', remote_side='LxTempType.id')

class LxTemplate(db.Model, LxMixin):
    __tablename__ = 'lxtemplate'

    cols = ['id', 'name', 'type', 'owner', 'content', 'gmt_create',
            'gmt_modify', 'status']
    name = Column(String(64), nullable=False)
    content = Column(Text)

    owner = relationship("LxUser")
    owner_id = Column(Integer, ForeignKey('lxuser.id'))

    type = relationship('LxTempType')
    type_id = Column(Integer, ForeignKey('lxtemptype.id'))