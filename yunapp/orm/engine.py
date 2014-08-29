# -*- coding:utf-8 -*-
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from yunapp import config

logger = logging.getLogger('ORM.ENGINE')

G = globals()
G['db_engine'] = None
G['session_maker'] = None


def get_engine(host='master', port=None, name=None, echo=False, **kwargs):
    db_config = config.get_db_config()

    if name is None:
        name = db_config.get('db_name')
    if host == 'master':
        host = db_config.get('db_host')
    if host is None:
        host = ''
    if port:
        host += ':%d' % port
    db_user = db_config.get('db_user')
    db_password = db_config.get('db_password')

    url = 'mysql://%s:%s@%s/%s?charset=utf8' % (db_user, db_password, host, name)
    if 'pool_size' not in kwargs:
        kwargs['pool_size'] = 10
    if 'max_overflow' not in kwargs:
        kwargs['max_overflow'] = 5
    if 'pool_recycle' not in kwargs:
        kwargs['pool_recycle'] = 600
    return create_engine(url, encoding='utf-8', echo=echo, **kwargs)


@contextmanager
def with_session(transaction=False):
    sess = session_maker()
    sess._model_changes = {}
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise


def get_session(host='master', port=None, name=None, echo=False, **kwargs):
    logger.debug('get_session(), host is %s, port is %s, echo is %s, kwargs are %s', host, port, echo, kwargs)
    global db_engine, session_maker

    if not db_engine or not session_maker:
        db_engine = get_engine(host, port, name, echo, **kwargs)
        session_maker = scoped_session(sessionmaker(bind=db_engine,
                                                    expire_on_commit=True))
        G = globals()
        G['db_engine'] = db_engine
        G['session_maker'] = session_maker
        G['session'] = session_maker()

    return session_maker()

s = get_session(echo=False)
