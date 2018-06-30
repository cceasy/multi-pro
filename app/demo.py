from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import random
from . import udfs
import functools
# from . import cache_dict as cache
from . import cache_redis as cache
from itertools import product
import multiprocessing
import logging

logger = logging.getLogger('demo')

def fake_register():
    def f1(x):
        time.sleep(2)
        return "fake_result_f1#{}".format(x)
    def f2(x):
        time.sleep(2)
        return "fake_result_f2#{}".format(x)
    def f3(x):
        time.sleep(2)
        return "fake_result_f3#{}".format(x)
    udfs.register_udf('f1', f1)
    udfs.register_udf('f2', f2)
    udfs.register_udf('f3', f3)

fake_register()

def fake_variable(num):
    """
    fake variable calculate process
    """
    for _ in range(num):
       cache.get_with_set(random.choice(test_f), random.choice(test_x))
    return 'fake_success_result'

n = 30  # fake variables count
test_f = ['f1', 'f2', 'f3']
test_x = ['a', 'b', 'c']
test_variables = dict() # fake variables
fake_nums = [random.randint(1, 4) for _ in range(n)]
for i in range(n):
    variable = 'v{}'.format(i)
    test_variables[variable] = functools.partial(fake_variable, num = fake_nums[i])

if __name__ == '__main__': 
    """
    fake pressure test alone
    """
    logger.info('fake variables: {}'.format(test_variables))
    pool = ThreadPoolExecutor(n)
    pool.map(fake_variable, fake_nums)
    pool.shutdown()
    logger.info('main process end')
