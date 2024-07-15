from .error_handling.logger import logger
from .jwt_token import is_jwt_valid, is_user_an_admin, is_access_token
import string, secrets

class HTTP_STATUS_CODE:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    USER_NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

def auth_token(token, args, check_for_admin_privs: bool):
    """function checks if arguments are not None, if jwt token is valid
    and based on check_for_admin_privs whether token has admin privs

    Args:
        token: jwt token
        args: list of arguments
        check_for_admin_privs (bool): whether token should have admin privilages

    Returns:
        error, status_code: error is None, if there is no error
    """
    error = None
    status_code = HTTP_STATUS_CODE.BAD_REQUEST
    
    validation, decoded_token = is_jwt_valid(token)
    
    logger.info('decoded token ' + str(decoded_token))
    
    if not token:
        error = 'Token is required.'
    elif not validation:
        error = 'Token is not valid.'
        status_code = HTTP_STATUS_CODE.UNAUTHORIZED
    elif (check_for_admin_privs and not is_user_an_admin(decoded_token)) or not is_access_token(decoded_token): # user needs to have admin privilages to add user
        error = 'User don\'t have permision top perform this operation.'
        status_code = HTTP_STATUS_CODE.UNAUTHORIZED
    
    for arg in args:
        if not arg:
            error = 'not enough arguments'
    
    return error, status_code

def generate_random_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))