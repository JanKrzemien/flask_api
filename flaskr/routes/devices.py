from flask import Blueprint, request, jsonify
from ..error_handling.logger import logger

from ..auth import auth_user, check_if_data_is_not_None
from ..error_handling.exceptions import DATA_NOT_FOUND_EXCEPTION, UNAUTHORIZED_EXCEPTION
from ..operations_on_data.get_data import get_data_from_query
from ..operations_on_data.post_data import post_data_using_query
from ..util import json_error, json_request_completed

bp = Blueprint('/devices', __name__, url_prefix='/devices')

@bp.route('/add', methods=['POST'])
def add():
    token = request.json['token']                       # can't be None
    serial_number = request.json['serial_number']       # can't be None
    production_date = request.json['production_date']   # can't be None
    last_serviced = "null" if request.json['last_serviced'] is None else request.json['last_serviced']
    battery = "null" if request.json['battery'] is None else request.json['battery']
    status_id = request.json['status_id']               # can't be None
    other_info = "null" if request.json['other_info'] is None else request.json['other_info']
    latitude = "null" if request.json['latitude'] is None else request.json['latitude']
    longitude = "null" if request.json['longitude'] is None else request.json['longitude']
    
    try:
        check_if_data_is_not_None([token, serial_number, production_date, status_id])
        auth_user(token, check_for_admin_privs=False)
        post_data_using_query("INSERT INTO device (serial_number, production_date, last_serviced, battery, status_id, other_info, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (serial_number, production_date, last_serviced, battery, status_id, other_info, latitude, longitude))
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION as ex:
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
    
    return jsonify(get_data_from_query("SELECT * FROM device ORDER BY serial_number LIMIT %s OFFSET %s;" % (size, offset)))