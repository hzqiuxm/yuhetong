#-*- coding:utf-8 -*-

import datetime
import json
import logging
from sqlalchemy import orm, sql, and_, or_
from flask.ext.sqlalchemy import SQLAlchemy
from yunapp import config
from yunapp.yunapps import app
from yunapp.orm  import db, engine

logger = logging.getLogger("ORM.MODEL")
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI


class Base(object):
    def __init__(self, **kargs):
        self.set(**kargs)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
            ' '.join(['%s:%r' %(k, getattr(self, k)) for k in sorted(self.__dict__.keys()) if not k.startswith('_')]), )

    @classmethod
    def create(cls, **kwargs):
        obj = cls()
        obj.update(kwargs)

        return obj

    @classmethod
    def from_json(cls, attrs):
        l = json.loads(attrs)

        return cls.create(**l)

    def format_obj(self,target):
        if isinstance(target, datetime.datetime):
            return datetime.datetime.strftime(target,'%Y-%m-%d %H:%M:%S')
        elif isinstance(target, long):
            return int(target)
        elif isinstance(target, dict):
            return json.dumps(target)
        else:
            return target

    def serialize(self, keys=None):
        """Return object data in easily serializeable format"""
        one = dict()
        if keys is not None:
            """Explicit declare the keys of the object data to serializeable format"""
            for key in keys:
                one[key] = self.format_obj(getattr(self,key,None))
        else:
            for key in self._sa_class_manager.iterkeys():
                if self.check_col(key):
                    one[key] = self.format_obj(getattr(self,key,None))
        return one

    def update(self, attrs):
        self.validate(attrs)
        for k,v in attrs.iteritems():
            # if validate ensures keys in attrs are all in self.cols...
            if k in self.cols and getattr(self, k) != v:
                setattr(self, k, v)

        if not self.id:
            self.gmt_create = sql.func.current_timestamp()
            self.gmt_modify = self.gmt_create
        else:
            self.gmt_modify = sql.func.current_timestamp()

    def validate(self, attrs):
        return True

    def check_col(self, col_name):
        return col_name in self.cols

    def load_options(self):
        if getattr(self, '_opts', None) is None:
            if not self.options: self._opts = {}
            else: self._opts = json.loads(self.options)

    def get_option(self, name):
        if getattr(self, '_opts', None) is None: self.load_options()
        return self._opts.get(name)

    def set_option(self, name, value):
        if getattr(self, '_opts', None) is None: self.load_options()
        self._opts[name] = value
        # not very optimized, encodes options every time an option is set.
        self.options = json.dumps(self._opts)

    @classmethod
    def load(cls, *args, **kargs):
        '''
        load an instance of cls from db by indicated conditions,返回一个处于persistent state的instance
        注意：load()的参数里面没法指定类似 Cls.column != xxx的条件,如果需要请使用load_by()
        @param args: 指定primary key(s)对应的值,当主键多于1个时，args内部的顺序按照table定义的次序匹配
        @param kargs: 指定属性的(key,value)
        @exception: 当按照指定的条件在db中无法找到或找到多个对应记录时，throws ObjectNotFoundException
        '''
        if args:
            instance = engine.session.query(cls).get(args)
            if instance is None:
                # raise ObjectNotFoundException('failed to load %s(%r)' % (cls.__name__, args))
                pass
            return instance
        try:
            instance = engine.session.query(cls).filter_by(**kargs).one()
        except orm.exc.NoResultFound:
            # raise ObjectNotFoundException('failed to load %s(%s)' % (cls.__name__, ' '.join(['%s:%r' % (k, kargs[k]) for k in kargs])))
            pass
        except orm.exc.MultipleResultsFound:
            # raise ObjectNotFoundException('failed to load %s(%s), more than one found.' % (cls.__name__, ' '.join(['%s:%r' % (k, kargs[k]) for k in kargs])))
            pass

        return instance

    @classmethod
    def load_by(cls, filter_clause=None, **kwargs):
        '''
        返回a list of cls instance
        @filter_clause: ClauseElement，用来传递 Cls.column!=xxx之类的条件
        @param kwargs:
            _order_by: kwargs.get('_order_by', None);
                 eg.: sa.asc(cls.stamp1) / [sa.asc(cls.stamp1), sa.desc(cls.stamp2)...]
            _limit: kwargs.get('_limit', None), int
            _offst: kwargs.get('_offset', None), int
            other: k=v
        eg.:
            GuiSession.load_by(and_(GuiSession.id!=10, GuiSession.gid==10), _limit=1, _offset=10, proto='rdp', status=0)
        '''
        q = engine.session.query(cls)
        if filter_clause is not None: q = q.filter(filter_clause)
        if kwargs:
            order_by = kwargs.pop('_order_by', None)
            #if order_by is not None: q = q.order_by(order_by)#deprecated by sa
            if order_by is not None:
                if isinstance(order_by, list):
                    q = q.order_by(*order_by)
                else:
                    q = q.order_by(order_by)

            limit = kwargs.pop('_limit', None)
            offset = kwargs.pop('_offset', None)

            if kwargs: q = q.filter_by(**kwargs)
            if limit: q = q.limit(limit)
            if offset: q = q.offset(offset)

        return q.all()

    @classmethod
    def load_all(cls):
        return dict([(x.id,x) for x in cls.load_by()])

    def reload(self):
        '''
        重新查询数据库，加载self
        '''
        engine.session.refresh(self)

    def set(self, **kargs):
        '''
        update attributes of self,用在一次设置多个属性的调用场合
        '''
        for k,v in kargs.iteritems():
            setattr(self, k, v)

    def save(self, flush=False):
        '''
        INSERT/UPDATE self to db on the next flush operation;
        如果self是cls.load()返回的，可以不用调用save();
        如果self是CLASS()或create()来的，务必调用save().
        '''
        engine.session.add(self)
        if flush: engine.session.flush()
