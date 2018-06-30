import os
from app import app
import flup.server.fcgi

os.chdir(os.path.dirname(__file__))

if __name__ == '__main__':
    flup.server.fcgi.WSGIServer(app).run()
