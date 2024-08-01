from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from ..error_handling.logger import logger

from ..jwt_token import create_token, is_jwt_valid
from ..auth import auth_token, HTTP_STATUS_CODE, generate_random_secret_key

from ..post_data import post_data_using_query

bp = Blueprint('/user', __name__, url_prefix='/user')

@bp.route('/create', methods=['POST'])
def create():
    token = request.json['token']
    username = request.json['username']
    password = request.json['password']
    admin = request.json['admin']
    
    error, status_code = auth_token(token, [username, password, admin], True)
    
    if error is None:
        admin = 1 if admin == 'True' else 0
        
        error = post_data_using_query(
            "INSERT INTO user (username, password, admin, refresh_secret_key) VALUES (?, ?, ?, ?)",
            (username, generate_password_hash(password), admin, generate_random_secret_key())
        )
        if error is None:
            logger.info("Created user {username}.")
            return jsonify({'username': username})
    
    logger.error('Error while creating user.')
    return jsonify({
        "code": status_code,
        "error": error
    })

@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    error = None
    status_code = HTTP_STATUS_CODE.BAD_REQUEST
    
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
            'token': create_token(user['username'], user['admin'], current_app.config['ACCESS_TOKEN_TYPE'], current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION']),
            'refresh_token': create_token(user['username'], user['admin'], current_app.config['REFRESH_TOKEN_TYPE'], user['refresh_secret_key'], None)
        })
    else:
        logger.info('User failed to log in.')
        return jsonify({
            "code": status_code,
            "error": error
        })
        

@bp.route('/remove', methods=['DELETE'])
def remove():
    token = request.json['token']
    username = request.json['username']
        
    error, status_code = auth_token(token, [username], True)
    
    if error is not None:
        return jsonify({
            "code": status_code,
            "error": error
        })
    
    logger.info('removing user ' + username)
        
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username, )
    ).fetchone()

    if user is None:
        error = f'User with username {username} doesn\'t exists.'
        status_code = HTTP_STATUS_CODE.USER_NOT_FOUND
    
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
        "code": status_code,
        "error": error
    })

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json['refresh_token']
    username = request.json['username']
    
    if not username or not refresh_token:
        return jsonify({
            "code": HTTP_STATUS_CODE.BAD_REQUEST,
            "error": "not enough arguments"
        })
    
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username, )
    ).fetchone()
    
    validation, decoded_token = is_jwt_valid(refresh_token, user['refresh_secret_key'])
    
    if not validation:
        return jsonify({
            "code": HTTP_STATUS_CODE.UNAUTHORIZED,
            "error": "token not valid or expired"
        })
    
    new_refresh_secret_key = generate_random_secret_key()
    try:
        db.execute(
            "UPDATE user SET refresh_secret_key = ? WHERE id = ?",
            (new_refresh_secret_key, user['id'])
        )
        db.commit()
    except Exception as e:
        logger.error(e)
        return jsonify({
            "code": HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR,
            "error": f"Error while updating user with username {username}."
        })
    else:
        return jsonify({
            'token': create_token(user['username'], user['admin'], current_app.config['ACCESS_TOKEN_TYPE'], current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION']),
            'refresh_token': create_token(user['username'], user['admin'], current_app.config['REFRESH_TOKEN_TYPE'], new_refresh_secret_key, None)
        })    

@bp.route('/newsecret', methods=['PATCH'])
def change_secret_key():
    token = request.json['token']
    secret = request.json['secret']
    
    error, status_code = auth_token(token, [secret], True)
    
    if error is not None:
        return jsonify({
            "code": status_code,
            "error": error
        })
    
    current_app.config['SECRET_KEY'] = secret