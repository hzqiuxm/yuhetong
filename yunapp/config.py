DEBUG = True
SECRET_KEY = 'mysecretkey'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DATABASE_URI = 'mysql://root:Hello1234@127.0.0.1/wenwuTest'

REDIS_HOST = 'localhost'
REDIS_DB = 0
REDIS_PORT = 6379
REDIS_PASS = 'Hello1234'

YOUR_FILE_STORE_FOLDER = '/home/vagrant/filestore'
CONTRACT_STORE_FOLDER = '/mft/mfs/contract'

DB_NAME = 'seanwuTest'
DB_USER = 'root'
DB_HOST = '127.0.0.1'
DB_PASSWD = 'Hello1234'

LOG_DIR = '/var/log/yunapp'
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'yunapp.log'

MD5_SUFFIX='asfkjASF3#@$%$sdFGasd235'
SERVER_NAME = 'my.yunhetong.com'

def get_db_config():
    db_config = {}
    db_config['db_name'] = DB_NAME
    db_config['db_user'] = DB_USER
    db_config['db_host'] = DB_HOST
    db_config['db_password'] = DB_PASSWD
    return db_config
