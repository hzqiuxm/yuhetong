# -*- coding: utf-8 -*-
# @author: seanwu
# 这个文件是SeanWu写的，现在已经不需要了，请无视他
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
    username = Column(String(80), nullable=False)
    realName = Column(String(80), nullable=False)
    type = Column(String(10), nullable=False)
    passwd = Column(String(50), nullable=False)
    email = Column(String(64), nullable=False)
    phone = Column(String(20))
    parentUserId = Column(Integer, nullable=False)
    companyId = Column(Integer, nullable=False)
    createTime = Column(DateTime, nullable=False, default='0000-00-00 00:00:00')
    modifyTime = Column(DateTime, nullable=False, default=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    signId = Column(String(10))
    status = Column(String(10))

    def __init__(self, username, realName, type, passwd, email, phone,
                 companyId, signId, parentUserId =0 ,createTime = '0000-00-00 00:00:00',
                 modifyTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) ):
        self.username = username
        self.realName = realName
        self.type = type
        self.passwd = hashlib.md5(passwd)
        self.email = email
        self.phone = phone
        self.parentUserId = parentUserId
        self.createTime = createTime
        self.modifyTime = modifyTime
        self.companyId = companyId
        self.signId = signId



