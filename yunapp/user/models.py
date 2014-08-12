# -*- coding: utf-8 -*-
# @author: seanwu
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from yunapp import config
import time, hashlib

engine = create_engine(config.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'lxuser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True)
    realName = Column(String(80), unique=True)
    type = Column(String(10), unique=True)
    passwd = Column(String(50), unique=True)
    email = Column(String(64), unique=True)
    phone = Column(String(20))
    parentUserId = Column(String(64), unique=True)
    companyId = Column(String(10), unique=True)
    createTime = Column(DateTime, unique=True, default='0000-00-00 00:00:00')
    modifyTime = Column(DateTime, unique=True, default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    signId = Column(String(10))
    status = Column(String(10))

    def __init__(self, username, realName, type, passwd, email, phone, parentUserId,
                 companyId, signId):
        self.username = username
        self.realName = realName
        self.type = type
        self.passwd = hashlib.md5(passwd)
        self.email = email
        self.phone = phone
        self.parentUserId = parentUserId
        self.companyId = companyId
        self.signId = signId



