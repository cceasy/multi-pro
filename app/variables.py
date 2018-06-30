# -*- encoding:utf-8 -*-
from flask import Blueprint
import logging
from . import demo
import traceback

mod = Blueprint('variables', __name__)

logger = logging.getLogger('variables')

@mod.route('/<string:variable>', methods=["GET"], endpoint='friend')
def calculate_variable(variable):
    logger.info('request {}'.format(variable))
    res = "NO SUCH VARIABLE"
    if variable in demo.test_variables:
        res = demo.test_variables[variable]()
    return res, 200
