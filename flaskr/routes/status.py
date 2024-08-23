from flask import Blueprint, request, jsonify
from ..error_handling.logger import logger

from ..auth import auth_user, check_if_data_is_not_None
from ..error_handling.exceptions import DATA_NOT_FOUND_EXCEPTION, UNAUTHORIZED_EXCEPTION, INTERNAL_ERROR_EXCEPTION
from ..util import json_error, json_request_completed
from ..operations_on_data.get_data import get_data_from_query
from ..operations_on_data.post_data import post_data_using_query

bp = Blueprint('/status', __name__, url_prefix='/status')

@bp.route('/add', methods=['POST'])
def add():
    token = request.json['token']
    color = request.json['color']
    message = request.json['message']
    
    try:
        check_if_data_is_not_None([token, color, message])
        auth_user(token, check_for_admin_privs=False)
        post_data_using_query("INSERT INTO status (message, color) VALUES (?, ?)", (message, color))
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION or INTERNAL_ERROR_EXCEPTION as ex:
        return json_error(ex.error, ex.status_code)
    
    return json_request_completed()
    
    

@bp.route('/get', methods=['GET'])
def get():
    token = request.json['token']
    offset = request.json['offset']
    size = request.json['size']
    
    try:
        check_if_data_is_not_None([token, offset, size])
        auth_user(token, check_for_admin_privs=False)
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION as ex:
        return json_error(ex.error, ex.status_code)
    
    return jsonify(get_data_from_query("SELECT * FROM status ORDER BY id LIMIT %s OFFSET %s;" % (size, offset)))
    