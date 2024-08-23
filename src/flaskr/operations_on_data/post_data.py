from flaskr.db import get_db
from ..error_handling.logger import logger

from ..error_handling.exceptions import INTERNAL_ERROR_EXCEPTION

def post_data_using_query(sql_command: str, args: list) -> None:
    """executes sql command and posts data to db

    Args:
        sql_command (str): sql command to be executed
        args (list): args to be used in sql command

    Raises:
        INTERNAL_ERROR_EXCEPTION: error while working with db
    """
    db = get_db()
    try:
        db.execute(sql_command,args)
        db.commit()
    except Exception as e:
        logger.error(f'Error while posting data.\n{e}')
        raise INTERNAL_ERROR_EXCEPTION(error='Error while posting data.')