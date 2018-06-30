import redis
from threading import Condition, RLock
from tornado import gen
from hashlib import md5
import sys
from . import udfs
from . import workers
from werkzeug.utils import import_string
import threading
import multiprocessing
import time
import functools
import logging
import os

logger = logging.getLogger('cache_redis')
config_obj = os.environ.get('CONFIG', 'config.DefaultConfig')
config_obj = import_string(config_obj)
encoding = config_obj.ENCODING
ex = config_obj.CACHE_EXPIRE    # expire time in seconds
conn_pool = redis.ConnectionPool(host=config_obj.REDIS_SERVER, port=config_obj.REDIS_PORT)
cache = redis.Redis(connection_pool=conn_pool)

conditions = dict()

def hash(fname, x):
    return md5('{}{}'.format(fname, x).encode(encoding)).hexdigest()

def get_f(fname, x):
    return cache.get(hash(fname, x))

def get(key):
    logger.info('cache hit: {}'.format(key))
    return cache.get(key)

def set_f(fname, x, value):
    cache.setex(hash(fname, x), value, ex)

def set(key, value):
    logger.info('set cache: {} -> {}'.format(key, value))
    cache.setex(key, value, ex)

def contains_f(fname, x):
    return cache.exists(hash(fname, x))

def contains(key):
    return cache.exists(key)

def get_with_set(fname, x):
    """
    fname: function, x: arguments
    get if cache contains, else request and update cache
    """
    key = hash(fname, x)
    if (contains(key)):
        return get(key)
    elif (not udfs.contains(fname)):
        return udfs.default_udf(x)
    else:
        with udfs.locks[fname]:
            if (key not in conditions):
                logger.info('lock {}#{} by {}{}'.format(fname, x, process_str(), thread_str()))
                time.sleep(3)
                conditions[key] = Condition()
                future = workers.invoke(fname, x)
                future.add_done_callback(functools.partial(update_cache, key = key))
        with conditions[key]:
            if (not contains(key)):
                logger.info('wait {}#{} by {}{}'.format(fname, x, process_str(), thread_str()))
                conditions[key].wait()
        return get(key)

@gen.coroutine
def update_cache(future, key):
    """
    as callback to update cache while future ready
    """
    result = yield future
    logger.info('callback with result: {}'.format(result))
    set(key, result)
    with conditions[key]:
        conditions[key].notify_all()

def thread_str():
    """
    get current thread representation by thread id and name
    for test case, log to debug
    """
    return '{}#{}'.format(threading.current_thread().ident, threading.current_thread().name)

def process_str():
    return '{}#{}'.format(multiprocessing.current_process().ident, multiprocessing.current_process().name)
