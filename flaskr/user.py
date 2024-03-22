from flask import Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('/user', __name__, url_prefix='/user')

@bp.route('/create', methods=['POST'])
def create():
    pass

@bp.route('remove', methods=['DELETE'])
def remove():
    pass

@bp.route('update', methods=['PATCH'])
def update():
    pass