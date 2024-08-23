from flask import jsonify

from .error_handling.exceptions import HTTP_STATUS_CODE

def get_admin_int_value(admin: str) -> int:
    return 1 if admin == 'True' else 0

def json_error(error: str, status_code: int) -> str:
    return jsonify({
        'error': error,
        'status_code': status_code
    })

def json_request_completed() -> str:
    return jsonify({
        "status_code": HTTP_STATUS_CODE.OK
    })