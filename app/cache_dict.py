from threading import Condition, RLock
from tornado import gen
from hashlib import md5
from . import workers
import threading
import multiprocessing
import time
from . import udfs
import functools
import logging
import os

logger = logging.getLogger('cache')

encoding='utf-8'

cache = dict()
conditions = dict()

def hash(fname, x):
    return md5('{}{}'.format(fname, x).encode(encoding)).hexdigest()

def get_f(fname, x):
    return cache[hash(fname, x)]

def get(key):
    logger.info('cache hit: {}'.format(key))
    return cache[key]

def set_f(fname, x, value):
    cache[hash(fname, x)] = value

def set(key, value):
    logger.info('set cache: {} -> {}'.format(key, value))
    cache[key] = value

def contains_f(fname, x):
    return hash(fname, x) in cache

def contains(key):
    return key in cache

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
