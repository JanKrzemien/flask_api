from flask import Blueprint, request, jsonify, current_app
from flaskr.db import get_db
from ..error_handling.logger import logger

from ..auth import auth_token, HTTP_STATUS_CODE
from ..getters import get_data_from_query

bp = Blueprint('/status', __name__, url_prefix='/status')

@bp.route('/add', methods=['POST'])
def add():
    pass

@bp.route('/get', methods=['GET'])
def get():
    token = request.json['token']
    offset = request.json['offset']
    size = request.json['size']
    
    error, status_code = auth_token(token, [offset, size], False)
    
    if error is not None:
        return jsonify({
            "code": status_code,
            "error": error
        })
    
    return jsonify(get_data_from_query("SELECT * FROM status ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY;" % (offset, size)))
    