from threading import RLock

udfs = dict()   # user defined function
locks = dict()

def contains(fname):
    return fname in udfs

def register_udf(fname, f, replace=True):
    """
    register udf to udfs, which will be used for executor run
    """
    if (fname in udfs and not replace):
        pass
    else:
        udfs[fname] = f
    if (fname not in locks):
        locks[fname] = RLock()

def default_udf(x):
    """
    handle case which function not registered
    """
    return "no such udf"

register_udf("default", default_udf)
