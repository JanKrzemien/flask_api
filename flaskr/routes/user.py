from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from ..error_handling.logger import logger

import jwt

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
            print(e)
            error = 'Error while creating user.'
        else:
            logger.info("Created user {username}.")
            return jsonify({'username': username})
    
    logger.error('Error while creating user.')
    return jsonify({
        "code": 400,
        "error": error
    })

def create_token(username, admin_privs, token_type, expires = None):
    payload_data = {
                'token_type': token_type,
                'username': username,
                'admin': admin_privs
    }
    if expires is not None:
        payload_data['expires'] = expires
    return jwt.encode(
            key=current_app.config['SECRET_KEY'],
            payload=payload_data
    )

@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    error = None
    
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username, )
    ).fetchone()
    
    if user is None:
        error = f'User with username {username} doesn\'t exist.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'
    
    if error is None:
        logger.info('User logged in. Generating tokens')
        return jsonify({
            'token': create_token(user['username'], user['admin'], current_app.config['ACCESS_TOKEN_TYPE'], current_app.config['TOKEN_EXPIRATION']),
            'refresh_token': create_token(user['username'], user['admin'], current_app.config['REFRESH_TOKEN_TYPE'])
        })
    
    logger.info('User failed to log in.')
    
    return jsonify({
        "code": 400,
        "error": error
    })
        

@bp.route('/remove', methods=['DELETE'])
def remove():
    #TODO add jwt authorization with admin privilages
    
    username = request.json['username']
    
    logger.info('username: ' + username)
    
    error = None
    
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username, )
    ).fetchone()

    if user is None:
        error = f'User with username {username} doesn\'t exists.'
    
    if error is None:
        try:
            db.execute(
                "DELETE FROM user WHERE id = ?",
                (user['id'], )
            )
            db.commit()
        except Exception as e:
            logger.error(e)
            error = f"Error while deleting user with username {username}."
        else:
            return jsonify({'username': username})
    
    return jsonify({
        "code": 400,
        "error": error
    })
    

@bp.route('/update', methods=['PATCH'])
def update():
    pass

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    pass

@bp.route('/newsecret', method=['PATCH'])
def change_secret_key():
    pass