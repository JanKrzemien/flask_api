from flask import Blueprint, request, jsonify, current_app
from flaskr.db import get_db
from ..error_handling.logger import logger

from ..auth import auth_token, HTTP_STATUS_CODE
from ..get_data import get_data_from_query
from ..post_data import post_data_using_query

bp = Blueprint('/status', __name__, url_prefix='/status')

@bp.route('/add', methods=['POST'])
def add():
    token = request.json['token']
    color = request.json['color']
    message = request.json['message']
    
    error, status_code = auth_token(token, [color, message], False)
    if error is not None:
        return jsonify({
            "code": status_code,
            "error": error
        })
    
    error = post_data_using_query("INSERT INTO status (message, color) VALUES (?, ?)", (message, color))
    
    if error is not None:
        return jsonify({
            "code": HTTP_STATUS_CODE.BAD_REQUEST,
            "error": error
        })
    
    return jsonify({
        'code': HTTP_STATUS_CODE.OK
    })
    
    

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
    
    return jsonify(get_data_from_query("SELECT * FROM status ORDER BY id LIMIT %s OFFSET %s;" % (size, offset)))
    