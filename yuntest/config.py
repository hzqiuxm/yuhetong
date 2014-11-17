DEBUG = True
SECRET_KEY = 'mysecretkey'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DATABASE_URI = 'mysql://root:Hello1234@127.0.0.1/wenwu_unittest'


DB_NAME = 'wenwu_test_unittest'
DB_USER = 'root'
DB_HOST = '127.0.0.1'
DB_PASSWD = 'Hello1234'

LOG_DIR = '/home/wenwu/yunhetong/yunapp/log'
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'yunapp.log'

MD5_XXXX='asfkjASF3#@$%$sdFGasd235'

def get_db_config():
    db_config = dict()
    db_config['db_name'] = DB_NAME
    db_config['db_user'] = DB_USER
    db_config['db_host'] = DB_HOST
    db_config['db_password'] = DB_PASSWD
    return db_config
