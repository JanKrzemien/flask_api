from .error_handling.logger import logger
from .jwt_token import is_jwt_valid, is_user_an_admin, is_access_token
import string, secrets

class HTTP_STATUS_CODE:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    USER_NOT_FOUND = 404

def auth_token_with_admin_privs(token, args):
    error = None
    status_code = HTTP_STATUS_CODE.BAD_REQUEST
    
    validation, decoded_token = is_jwt_valid(token)
    
    logger.info('decoded token ' + str(decoded_token))
    
    if not token:
        error = 'Token is required.'
    elif not validation:
        error = 'Token is not valid.'
        status_code = HTTP_STATUS_CODE.UNAUTHORIZED
    elif not is_user_an_admin(decoded_token) or not is_access_token(decoded_token): # user needs to have admin privilages to add user
        error = 'User don\'t have permision top perform this operation.'
        status_code = HTTP_STATUS_CODE.UNAUTHORIZED
    
    for arg in args:
        if not arg:
            error = 'not enough arguments'
    
    return error, status_code

def generate_random_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))