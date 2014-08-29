# -*- coding:utf-8 -*-

import logging
from yunapp import config
from yunapp.yunapps import app
from flask.ext.login import UserMixin  # UserMixin 封装了 Flask-login 里面 用户类的一些基本方法，我们的User类要继承他
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Column, ForeignKey, func, String, Integer, Text
from sqlalchemy.orm import backref, relationship
from yunapp.orm.db_base import LxMixin

logger = logging.getLogger('ORM.MODEL')
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

db = SQLAlchemy(app)


class LxUser(db.Model, UserMixin, LxMixin):
    __tablename__ = 'lxuser'

    cols = ['id', 'type', 'username', 'real_name', 'passwd', 'email',
            'phone', 'idCardNo', 'idCardimg1', 'idCardimg2', 'shouhanimg', 'parent_user_id', 'company_id',
            'address', 'sign_id', 'status', ]
    type = Column(Integer)
    username = Column(String(128), nullable=False, unique=True)
    real_name = Column(String(128))
    passwd = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False)
    phone = Column(String(32))
    idCardNo = Column(String(50))
    idCardimg1 = Column(String(100))
    idCardimg2 = Column(String(100))
    shouhanimg = Column(String(100))
    address = Column(String(50))
    status = Column(Integer)
    parent_id = Column(Integer, ForeignKey('lxuser.id'), nullable=True)
    parent = relationship('lxuser', remote_side='lxuser.id')
    sign_id = Column(Integer, ForeignKey('lxsign.id'))
    sign = relationship('lxsign', uselist=False, backref='owner')
    commpany_id = Column(Integer, ForeignKey('lxcompany.id'), nullable=False)
    company = relationship('lxcompany', uselist=False, backref='owner')


class LxCompany(db.Model, LxMixin):
    __tablename__ = 'lxcompany'
    cols = ['id', 'type', 'name', 'orzNo', 'orzimg', 'yyzyNo', 'yyzyimg', 'legal_person', 'address',
            'gmt_create', 'gmt_modify', 'status', ]
    type = Column(Integer)
    name = Column(String(255), nullable=False, unique=True)
    shouhanimg = Column(String(100))
    orzNo = Column(String(50))
    orzimg = Column(String(100))
    yyzyNo = Column(String(50))
    yyzyimg = Column(String(100))
    legal_person = Column(String(10))
    address = Column(String(100))
    status = Column(Integer)
    owner_id = Column(Integer, ForeignKey('lxuser.id'))


class LxSign(db.Model, LxMixin):
    __tablename__ = 'lxsign'
    cols = ['id', 'gmt_create', 'gmt_modify', 'status', ]
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


class LxEmail(db.Model, LxMixin):
    __tablename__ = 'lxemail'
    cols = ['id', 'eTo', 'eFrom', 'eSubject', 'eContent']
    eTo = Column(String(50), nullable=False)
    eFrom = Column(String(50), nullable=False)
    eSubject = Column(String(100), nullable=False)
    eContent = Column(Text, nullable=False)


