# -*- coding:utf-8 -*-

import datetime, time, json
import logging
from sqlalchemy import orm, sql, and_, or_
from yunapp import config
from yunapp.yunapps import app
from flask.ext.login import UserMixin  # UserMixin 封装了 Flask-login 里面 用户类的一些基本方法，我们的User类要继承他
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, ForeignKey, func, String, \
    Integer, TIMESTAMP, Text
from sqlalchemy.orm import backref, relationship
# from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, VARCHAR, INTEGER


Base = declarative_base()
logger = logging.getLogger('ORM.MODEL')
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

db = SQLAlchemy(app)


class LxMixin(object):
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    gmt_modify = Column(TIMESTAMP, nullable=False, default=func.now())
    gmt_create = Column(TIMESTAMP, nullable=False, default=func.now())
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    def format_obj(self, target):
        if isinstance(target, datetime.datetime):
            return datetime.datetime.strftime(target, '%Y-%m-%d %H:%M:%S')
        elif isinstance(target, long):
            return int(target)
        elif isinstance(target, dict):
            return json.dumps(target)
        else:
            return target
    def check_col(self, col_name):
        return col_name in self.cols

    def serialize(self, keys=None):
        """Return object data in easily serializeable format"""
        item = dict()
        if keys is not None:
            """Explicit declare the keys of the object data to serializeable format"""
            for key in keys:
                item[key] = self.format_obj(getattr(self, key, None))
        else:
            for key in self._sa_class_manager.iterkeys():
                if self.check_col(key):
                    item[key] = self.format_obj(getattr(self, key, None))
        return item

    def validate(self, attrs):
        return True

    def update(self, attrs):
        self.validate(attrs)
        for k, v in attrs.iteritems():
            # if validate ensures keys in attrs are all in self.cols...
            if k in self.cols and getattr(self, k) != v:
                setattr(self, k, v)

        if not self.id:
            self.gmt_create = sql.func.current_timestamp()
            self.gmt_modify = self.gmt_create
        else:
            self.gmt_modify = sql.func.current_timestamp()

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
    company = relationship('LxCompany', uselist=False, backref='owner')

class LxCompany(db.Model, LxMixin):
    __tablename__ = 'lxcompany'

    cols = ['id', 'type', 'name', 'gmt_create',
            'gmt_modify', 'status', ]
    type = Column(Integer)
    name = Column(String(255), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey('lxuser.id'))

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