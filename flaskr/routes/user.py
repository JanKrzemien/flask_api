from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from ..error_handling.logger import logger

from ..jwt_token import create_token, decode_token
from ..auth import check_if_data_is_not_None, auth_user, check_if_password_matching_with_hash, generate_random_secret_key
from ..error_handling.exceptions import UNAUTHORIZED_EXCEPTION, DATA_NOT_FOUND_EXCEPTION, INTERNAL_ERROR_EXCEPTION
from ..util import json_error, json_request_completed, get_admin_int_value
from ..operations_on_data.get_data import get_user_by_username
from ..operations_on_data.delete_data import delete_user_by_id
from ..operations_on_data.update_data import update_users_refresh_secret_key
from ..operations_on_data.post_data import post_data_using_query

bp = Blueprint('/user', __name__, url_prefix='/user')

@bp.route('/create', methods=['POST'])
def create():
    token = request.json['token']
    username = request.json['username']
    password = request.json['password']
    admin = request.json['admin']
    
    try:
        check_if_data_is_not_None([token, username, password, admin])
        auth_user(token, check_for_admin_privs=True)
        admin = get_admin_int_value(admin)
        post_data_using_query(
            "INSERT INTO user (username, password, admin, refresh_secret_key) VALUES (?, ?, ?, ?)",
            (username, generate_password_hash(password), admin, generate_random_secret_key())
        )
    except UNAUTHORIZED_EXCEPTION or DATA_NOT_FOUND_EXCEPTION or INTERNAL_ERROR_EXCEPTION as ex:
        logger.error(f'{ex.error}\n{ex}')
        return json_error(ex.error, ex.status_code)
    
    return json_request_completed()

@bp.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    try:
        check_if_data_is_not_None([username, password])
        user = get_user_by_username(username)
        check_if_password_matching_with_hash(user['password'], password)
        token = create_token(user['username'], user['admin'], current_app.config['ACCESS_TOKEN_TYPE'], current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        refresh_token = create_token(user['username'], user['admin'], current_app.config['REFRESH_TOKEN_TYPE'], user['refresh_secret_key'], None)
        logger.info('User logged in. Generating tokens')
        return jsonify({
            'token': token,
            'refresh_token': refresh_token
        })
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION or INTERNAL_ERROR_EXCEPTION as ex:
        return json_error(ex.error, ex.status_code)
        

@bp.route('/remove', methods=['DELETE'])
def remove():
    token = request.json['token']
    username = request.json['username']
    
    try:
        check_if_data_is_not_None([token, username])
        auth_user(token, check_for_admin_privs=True)
        user = get_user_by_username(username)
        delete_user_by_id(user['id'])
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION as ex:
        logger.error(ex.error)
        return json_error(ex.error, ex.status_code)
    
    return json_request_completed()

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json['refresh_token']
    username = request.json['username']
    
    try:
        check_if_data_is_not_None([refresh_token, username])
        user = get_user_by_username(username)
        decode_token(refresh_token, user['refresh_secret_key'])
        new_refresh_secret_key = generate_random_secret_key()
        update_users_refresh_secret_key(new_refresh_secret_key, user['id'])
        new_token = create_token(user['username'], user['admin'], current_app.config['ACCESS_TOKEN_TYPE'], current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        new_refresh_token = create_token(user['username'], user['admin'], current_app.config['REFRESH_TOKEN_TYPE'], new_refresh_secret_key, None)
        return jsonify({
            'token': new_token,
            'refresh_token': new_refresh_token 
        })
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION or INTERNAL_ERROR_EXCEPTION as ex:
        return json_error(ex.error, ex.status_code)

@bp.route('/newsecret', methods=['PATCH'])
def change_secret_key():
    token = request.json['token']
    secret = request.json['secret']
    
    try:
        check_if_data_is_not_None([token, secret])
        auth_user(token, check_for_admin_privs=True)
        current_app.config['SECRET_KEY'] = secret
        logger.info('Global secret key has been changed.')
    except DATA_NOT_FOUND_EXCEPTION or UNAUTHORIZED_EXCEPTION as ex:
        logger.error('Error while changing global secret key.')
        return json_error(ex.error, ex.status_code)