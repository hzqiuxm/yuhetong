# -*- coding:utf-8 -*-

import datetime, json
from sqlalchemy import orm, sql, and_, or_
from sqlalchemy import  Column, ForeignKey, func, String, \
    Integer, TIMESTAMP, Text


class LxMixin(object):
    id = Column(Integer, primary_key=True,autoincrement=True)
    status = Column(Integer, nullable=False, default=1)
    gmt_modify = Column(TIMESTAMP, nullable=False,
                        default=sql.func.current_timestamp())
    gmt_create = Column(TIMESTAMP, nullable=False,
                        default=sql.func.current_timestamp())
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    def __init__(self, **kargs):
        self.set(**kargs)

    def set(self, **kargs):
        """
        update attributes of self,用在一次设置多个属性的调用场合
        """
        for k, v in kargs.iteritems():
            setattr(self, k, v)

    @staticmethod
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
            # Explicit declare the keys of the object
            # data to serializeable format
            for key in keys:
                item[key] = self.format_obj(getattr(self, key, None))
        else:
            for key in self._sa_class_manager.iterkeys():
                if self.check_col(key):
                    item[key] = self.format_obj(getattr(self, key, None))
        return item

    @staticmethod
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