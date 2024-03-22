from flask import Blueprint, request, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import uuid
import logging

bp = Blueprint('/user', __name__, url_prefix='/user')

@bp.route('/create', methods=['POST'])
def create():
    #TODO add jwt authorization with admin privilages
    
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
        admin = 1 if admin == 'True' else 0
        
        try:
            db.execute(
                "INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), admin)
            )
            db.commit()
        except Exception as e:
            logging.error('Error while creating user.')
            print(e)
            error = 'Error while creating user.'
        else:
            logging.info("Created user {username}.")
            return jsonify({'username': username})
    
    abort(400, description=error)

@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    error = None
    
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username)
    ).fetchone()
    
    if user is None:
        error = f'User with username {username} doesn\'t exist.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'
    
    if error is None:
        #TODO generate JWT with given priviliges
        pass
    
    abort(400, description=error)
        

@bp.route('/remove', methods=['DELETE'])
def remove():
    #TODO add jwt authorization with admin privilages
    pass
    

@bp.route('/update', methods=['PATCH'])
def update():
    pass