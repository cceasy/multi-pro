from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import random
import requests
import traceback
from app.demo import test_variables

m = 50  # fake pressure test
url_prefix = 'http://127.0.0.1:5000/variables/'
variables = list(test_variables.keys())
urls = ['{}{}'.format(url_prefix, random.choice(variables)) for _ in range(m)]

def req(url):
    try:
        resp = requests.get(url, timeout = 60)
        res = resp.text
    except:
        res = traceback.format_exc()
    return res

if __name__ == '__main__':
    print('urls', urls)
    with ProcessPoolExecutor(m) as pool:
        for r in pool.map(req, urls):
            print(r)
    print('main process end')