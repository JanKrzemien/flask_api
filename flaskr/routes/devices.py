from flask import Blueprint, request, jsonify, current_app
from flaskr.db import get_db
from ..error_handling.logger import logger

from ..auth import auth_token, HTTP_STATUS_CODE

bp = Blueprint('/devices', __name__, url_prefix='/devices')

@bp.route('/add', methods=['POST'])
def add():
    pass

@bp.route('/get', methods=['GET'])
def get():
    pass