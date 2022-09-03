import logging
import sys
from functools import wraps
from flask import abort, jsonify, make_response, render_template
from app.settings import PROJECT_ID

log = logging.getLogger(__name__)

IS_DEV = False

def init(debug):
    global IS_DEV
    IS_DEV = debug
    if debug:
        if not log.handlers:
            log.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(module)s: %(message)s", datefmt="%H:%M:%S")
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)

            log.addHandler(handler)

# https://cloud.google.com/apis/design/errors#http_mapping
def json_abort(status_code, message, details=None):
    data = {
        'error': {
            'code': status_code,
            'message': message
        }
    }
    if details:
        data['error']['details'] = details
    response = jsonify(data)
    response.status_code = status_code
    abort(response)

def html_abort(status_code, message):
    response = make_response(render_template('abort.html', message=message, TITLE='Error'), status_code)
    # response.status_code = status_code
    abort(response)
