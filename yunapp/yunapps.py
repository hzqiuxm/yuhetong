# -*- coding: utf-8 -*-
import redis
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from yunapp import config

app = Flask('yunhetong')

# Init Redis
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT,
                            db=config.REDIS_DB, password=config.REDIS_PASS)
yun_redis = redis.Redis(connection_pool=pool)

bcrypt = Bcrypt(app)