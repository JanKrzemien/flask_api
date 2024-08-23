from werkzeug.security import check_password_hash

from .error_handling.logger import logger
from .jwt_token import decode_token, is_user_an_admin, is_access_token
import string, secrets
from .error_handling.exceptions import DATA_NOT_FOUND_EXCEPTION, UNAUTHORIZED_EXCEPTION

def check_if_data_is_not_None(args: list) -> None:
    """checks if any of the args is None, raises custom exception when is

    Args:
        args (list): list of args to get checked

    Raises:
        DATA_NOT_FOUND_EXCEPTION: Raised with custom error field to indicate that value is None
    """
    
    for arg in args:
        if not arg:
            raise DATA_NOT_FOUND_EXCEPTION(error='Data is None when it shouldn\'t be.')
            

def auth_user(token, check_for_admin_privs: bool) -> None:
    """function checks if jwt token is valid
    and based on check_for_admin_privs whether token has admin privs

    Args:
        token: jwt token
        check_for_admin_privs (bool): whether token should have admin privilages

    Raises:
        DATA_NOT_FOUND_EXCEPTION: token is None and user cannot be authorized
        UNAUTHORIZED_EXCEPTION: error while decoding token, token is not a access token, user doesn't have admin privilages and cannot be authorized
    """
    decoded_token = decode_token(token)
    
    logger.info('decoded token ' + str(decoded_token))
    
    if not token:
        raise DATA_NOT_FOUND_EXCEPTION(error='Token is required.')
    elif not decoded_token:
        raise UNAUTHORIZED_EXCEPTION(error='Token is not valid.')
    elif (check_for_admin_privs and not is_user_an_admin(decoded_token)) or not is_access_token(decoded_token):
        raise UNAUTHORIZED_EXCEPTION(error='User don\'t have permision top perform this operation.')

def generate_random_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def check_if_password_matching_with_hash(passwords_hash: str, password_delivered_by_user: str) -> None:
    if not check_password_hash(passwords_hash, password_delivered_by_user):
        raise UNAUTHORIZED_EXCEPTION(error='Incorrect password.')
    