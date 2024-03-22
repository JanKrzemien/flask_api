from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import uuid

bp = Blueprint('/user', __name__, url_prefix='/user')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    #TODO check jwt token and check it for admin == true
    
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        admin = request.json['admin']
        
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not admin:
            error = 'Specify whether this user is admin.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT"
                )
            except:
                pass

@bp.route('remove', methods=['DELETE'])
def remove():
    pass

@bp.route('update', methods=['PATCH'])
def update():
    pass