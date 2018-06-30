class Config(object):
    """
    base config
    """
    DEBUG = False
    SECRET_KEY = 'hello'
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    ENCODING = 'utf-8'
    CACHE_EXPIRE = 3600 # seconds

class LocalConfig(Config):
    DEBUG = True
    REDIS_SERVER = '127.0.0.1'
    REDIS_PORT = 6379

DefaultConfig = LocalConfig
