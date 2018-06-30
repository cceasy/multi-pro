import os
from flask import Flask
import logging.config

app = Flask(__name__)
config_obj = os.environ.get('CONFIG', 'config.DefaultConfig')
app.config.from_object(config_obj)

logging.config.fileConfig('log.conf')
logger = logging.getLogger('root')
logger.info('init finished')

from . import variables, error_handler

app.register_blueprint(variables.mod, url_prefix='/variables')
for code_or_exception, f in error_handler.error_handlers.items():
    app.register_error_handler(code_or_exception, f)
