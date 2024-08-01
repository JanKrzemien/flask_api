from flask import Blueprint, request, jsonify, current_app
from flaskr.db import get_db
from ..error_handling.logger import logger

from ..auth import auth_token, HTTP_STATUS_CODE
from ..get_data import get_data_from_query
from ..post_data import post_data_using_query

bp = Blueprint('/devices', __name__, url_prefix='/devices')

@bp.route('/add', methods=['POST'])
def add():
    token = request.json['token']
    serial_number = request.json['serial_number']       # can't be null
    production_date = request.json['production_date']   # can't be null
    last_serviced = "null" if request.json['last_serviced'] is None else request.json['last_serviced']
    battery = "null" if request.json['battery'] is None else request.json['battery']
    status_id = request.json['status_id']               # can't be null
    other_info = "null" if request.json['other_info'] is None else request.json['other_info']
    latitude = "null" if request.json['latitude'] is None else request.json['latitude']
    longitude = "null" if request.json['longitude'] is None else request.json['longitude']
    
    error, status_code = auth_token(token, [serial_number, production_date, last_serviced, battery, status_id, other_info, latitude, longitude], False)
    
    if error is not None:
        return jsonify({
            "code": status_code,
            "error": error
        })
    
    error = post_data_using_query("INSERT INTO device (serial_number, production_date, last_serviced, battery, status_id, other_info, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (serial_number, production_date, last_serviced, battery, status_id, other_info, latitude, longitude))
    
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
    
    return jsonify(get_data_from_query("SELECT * FROM device ORDER BY serial_number LIMIT %s OFFSET %s;" % (size, offset)))