# -*- coding: utf-8 -*-
import logging.config, json
from yunapps import app


def init_log():
    logging.config.fileConfig(app.root_path + '/log_config.ini')


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return tuple(o)
        elif isinstance(o, unicode):
            return o.encode('unicode_escape').decode('ascii')
        return super(Encoder, self).default(o)


class StructedMsg(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return '%s >>> %s' % (s, self.message)
