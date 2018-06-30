from concurrent.futures import ThreadPoolExecutor
import threading
import time
from tornado import gen
from threading import RLock

executor = ThreadPoolExecutor(max_workers=10)
lock = RLock()

def getId():
    return '{}#{}'.format(threading.current_thread().ident, threading.current_thread().name)

def run(lock):
    lock.acquire()
    r = getId()
    print('run', r)
    time.sleep(3)
    return r

def test():
    print('test', getId())
    future = executor.submit(run, lock)
    future.add_done_callback(test_r)

@gen.coroutine
def test_r(future):
    print('r', getId())
    result = yield future
    print(getId())
    print(result)
    lock.release()
    print('release')
    

if __name__ == '__main__':
    print(getId())
    thread = threading.Thread(target=test)
    thread.start()
    thread.join()
    time.sleep(3)
    