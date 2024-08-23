from flask import current_app
from .error_handling.logger import logger
import jwt
import datetime

from .error_handling.exceptions import INTERNAL_ERROR_EXCEPTION, UNAUTHORIZED_EXCEPTION

def decode_token(token: str, secret_key=None) -> str:
    """decodes jwt token using secret key given in params or default secret key from config

    Args:
        token (str): jwt token
        secret_key (any, optional): secret key used to encrypt jwt token. Defaults to None.

    Raises:
        UNAUTHORIZED_EXCEPTION: raised when couldn't decode jwt token 

    Returns:
        str: decoded jwt token
    """
    if secret_key is None:
        secret_key = current_app.config['SECRET_KEY']
    
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as e:
        logger.error('token not valid\n' + str(e))
        raise UNAUTHORIZED_EXCEPTION(error='Token not valid or expired.')

def is_user_an_admin(token):
    return token['admin'] == 1
def is_access_token(token):
    return token['token_type'] == current_app.config['ACCESS_TOKEN_TYPE']

def get_expiration_date(time_until_expiration):
    return datetime.datetime.now() + datetime.timedelta(seconds=time_until_expiration)

def create_token(username: str, admin_privs: int, token_type: str, secret_key: str, expires: int):
    """creates jwt token with payload consisting of username, admin privilages of user,
    token type, and time until expiration given in seconds

    Args:
        username (string)
        admin_privs (string): 1 or 0 depending on whether user has admin privilages
        token_type (string): is it access token or refresh token
        expires (int): number of seconds until expiration

    Raises:


    Returns:
        correctly encoded jwt token or raises exception
    """
    payload_data = {
                'token_type': token_type,
                'username': username,
                'admin': admin_privs
    }
    if expires is not None:
        payload_data['exp'] = get_expiration_date(expires)
    
    try:   
        return jwt.encode(
                key=secret_key,
                payload=payload_data,
                algorithm="HS256"
        )
    except Exception as e:
        logger.error(f'error while creating jwt token:\n{e}')
        raise INTERNAL_ERROR_EXCEPTION(error='error while creating jwt token.')