# -*- coding:utf-8 -*-

import logging

from flask.ext.login import UserMixin  # UserMixin 封装了 Flask-login里面 用户类的一些基本方法，我们的User类要继承他
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, func, String, Integer, Text, TIMESTAMP
from sqlalchemy.orm import backref, relationship
from yunapp import config
from yunapp.yunapps import app
from yunapp.orm.db_base import LxMixin

logger = logging.getLogger('ORM.MODEL')
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

db = SQLAlchemy(app)


class LxUser(db.Model, UserMixin, LxMixin):
    __tablename__ = 'lxuser'

    cols = ['id', 'type', 'username', 'real_name', 'passwd', 'email',
            'phone', 'idCardNo', 'idCardimg1', 'idCardimg2', 'authorization_img',
            'parent_user_id', 'company_id', 'address', 'sign_id', 'status', ]
    type = Column(Integer)
    username = Column(String(128), nullable=False, unique=True)
    real_name = Column(String(128))
    passwd = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False)
    phone = Column(String(32))
    idCardNo = Column(String(50))
    idCardimg1 = Column(String(100))
    idCardimg2 = Column(String(100))
    authorization_img = Column(String(100))
    address = Column(String(50))
    parent_id = Column(Integer, ForeignKey('lxuser.id'), nullable=True)
    children = relationship("LxUser")

    sign = relationship('LxSign', uselist=False, backref='owner')
    # one to one relationship  LxSign

    company = relationship('LxCompany')
    company_id = Column(Integer, ForeignKey('lxcompany.id'), nullable=True)
    # many to one relationship



class LxCompany(db.Model, LxMixin):
    __tablename__ = 'lxcompany'
    cols = ['id', 'type', 'name', 'organizationNo', 'organizationimg', 'business_license_No',
            'business_license_img', 'legal_person', 'address',
            'gmt_create', 'gmt_modify', 'status', ]
    type = Column(Integer)
    name = Column(String(255), nullable=False)
    organizationNo = Column(String(50))
    organization_img = Column(String(100))
    business_license_No = Column(String(50))
    business_license_img = Column(String(100))
    legal_person = Column(String(10))
    address = Column(String(100))


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
    extension = Column(String(8), nullable=True)
    fpath = Column(String(256), nullable=False)


class LxTempType(db.Model, LxMixin):
    __tablename__ = 'lxtemptype'


    cols = ['id', 'name', 'level', 'parent_id', 'gmt_create', 'gmt_modify',
            'status', 'children']
    level = Column(Integer)
    name = Column(String(64), nullable=False)

    parent_id = Column(Integer, ForeignKey('lxtemptype.id'), nullable=True)
    children = relationship('LxTempType')


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
    cols = ['id', 'eTo', 'eFrom', 'eSubject', 'eContent', 'gmt_create',
            'gmt_modify', 'status']
    eTo = Column(String(50), nullable=False)
    eFrom = Column(String(50), nullable=False)
    eSubject = Column(String(100), nullable=False)
    eContent = Column(Text, nullable=False)

class LxContract(db.Model, LxMixin):
    __tablename__ = 'lxcontract'
    cols = ['id', 'stage', 'name', 'appendix', 'part_num', 'version', 'gmt_expire',
            'take_passwd', 'gmt_create', 'gmt_modify', 'status']
    stage = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)

    appendix = Column(String(256), nullable=False)

    take_passwd = Column(String(256), nullable=True)
    part_num = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False)
    gmt_expire = Column(TIMESTAMP, nullable=True)


    draft_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    draft = relationship('LxFile', foreign_keys='LxContract.draft_fid')
    contract_v1_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    contract_v1 = relationship('LxFile', foreign_keys='LxContract.contract_v1_fid')
    contract_v2_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    contract_v2 = relationship('LxFile', foreign_keys='LxContract.contract_v2_fid')
    contract_v3_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    contract_v3 = relationship('LxFile', foreign_keys='LxContract.contract_v3_fid')
    contract_v4_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    contract_v4 = relationship('LxFile', foreign_keys='LxContract.contract_v4_fid')
    contract_v5_fid = Column(Integer, ForeignKey('lxfile.id'), nullable=True)
    contract_v5 = relationship('LxFile', foreign_keys='LxContract.contract_v5_fid')
    owner_id = Column(Integer, ForeignKey('lxuser.id'))
    owner = relationship("LxUser", foreign_keys='LxContract.owner_id')


class LxContractParticipation(db.Model, LxMixin):
    __tablename__ = 'lxcontractparticipation'
    cols = ['id', 'contract', 'user', 'stage', 'gmt_create',
            'gmt_modify', 'status']
    stage = Column(Integer, nullable=False)
    is_owner = Column(Integer, nullable=False, default=0)
    contract = relationship("LxContract")
    contract_id = Column(Integer, ForeignKey('lxcontract.id'))
    user = relationship("LxUser")
    user_id = Column(Integer, ForeignKey('lxuser.id'))

class LxContractAuthorization(db.Model, LxMixin):
    __tablename__ = 'lxcontractauthorization'
    cols = ['id', 'contract', 'user', 'read_perm', 'write_perm', 'sign_perm',
            'gmt_expire', 'gmt_create', 'gmt_modify', 'status']

    read_perm = Column(Integer, nullable=False, default=0)
    write_perm = Column(Integer, nullable=False, default=0)
    sign_perm = Column(Integer, nullable=False, default=0)
    auth_passwd = Column(String(256), nullable=True)
    gmt_expire = Column(TIMESTAMP, nullable=True)

    contract = relationship("LxContract")
    contract_id = Column(Integer, ForeignKey('lxcontract.id'))
    user = relationship("LxUser", foreign_keys='LxContractAuthorization.user_id')
    user_id = Column(Integer, ForeignKey('lxuser.id'), nullable=True)
    auth_own_user = relationship("LxUser",
                             foreign_keys='LxContractAuthorization.auth_own_user_id')
    auth_own_user_id = Column(Integer, ForeignKey('lxuser.id'))
