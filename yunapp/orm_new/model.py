# -*- coding:utf-8 -*-

import datetime, time, json
import logging
from sqlalchemy import orm, sql, and_, or_
from yunapp import config
from yunapp.yunapps import app
from yunapp.orm import db, engine
from flask.ext.login import UserMixin  # UserMixin 封装了 Flask-login 里面 用户类的一些基本方法，我们的User类要继承他
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TEXT, TINYINT, VARCHAR, INTEGER


Base = declarative_base()
logger = logging.getLogger("ORM.MODEL")
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

class LxUser(Base, UserMixin):
    __tablename__ = 'LxUser'
    id = Column(INTEGER, primary_key=True)
    type = Column(TINYINT(10))
    username = Column(VARCHAR(128))
    real_name = Column(VARCHAR(128))
    passwd = Column(VARCHAR(128), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    phone = Column(VARCHAR(32))
    parent_user_id = Column(INTEGER)
    sign_id = Column(INTEGER)
    company_id = Column(INTEGER)
    gmt_create = Column(TIMESTAMP, nullable=False, default='0000-00-00 00:00:00')
    gmt_modify = Column(TIMESTAMP, nullable=False, default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


