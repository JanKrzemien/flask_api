from flask import current_app
from .error_handling.logger import logger
import jwt
import datetime

def is_jwt_valid(token, secret_key=None):
    if secret_key is None:
        secret_key = current_app.config['SECRET_KEY']
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as e:
        logger.error('token not valid\n' + str(e))
        return False, None
    return True, decoded_token 

def is_user_an_admin(token):
    return token['admin'] == 1
def is_access_token(token):
    return token['token_type'] == current_app.config['ACCESS_TOKEN_TYPE']

def create_token(username, admin_privs, token_type, secret_key, expires):
    """creates jwt token with payload consisting of username, admin privilages of user,
    token type, and time until expiration given in seconds

    Args:
        username (string)
        admin_privs (string): 1 or 0 depending on whether user has admin privilages
        token_type (string): is it access token or refresh token
        expires (int): number of seconds until expiration

    Returns:
        either correctly encoded jwt token or string error message
    """
    payload_data = {
                'token_type': token_type,
                'username': username,
                'admin': admin_privs
    }
    if expires is not None:
        payload_data['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=expires)
    
    try:   
        return jwt.encode(
                key=secret_key,
                payload=payload_data,
                algorithm="HS256"
        )
    except Exception as e:
        return str(e)