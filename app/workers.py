from concurrent.futures import ThreadPoolExecutor
from . import udfs
import traceback
import logging

logger = logging.getLogger('workers')

executor = ThreadPoolExecutor(max_workers=20)

def _run(fname, x):
    """
    function to submit to executor
    find function f with fname, calculate f(x)
    """
    func = udfs.udfs.get(fname, udfs.default_udf)
    try:
        res = func(x)
    except:
        res = traceback.format_exc()
    return res
    
def invoke(fname, x):
    """
    open to be called, return future
    """
    future = executor.submit(_run, fname, x)
    return future