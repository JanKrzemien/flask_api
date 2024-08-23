from flaskr.db import get_db
from ..error_handling.logger import logger

from ..error_handling.exceptions import DATA_NOT_FOUND_EXCEPTION

def sqlite_row_objs_to_list_of_dicts(data: list[any], column_names: list[str]):
    dicts = list()
    
    for row in data:
        row_dict = dict()
        for i, column in enumerate(row):
            row_dict[column_names[i]] = column
        dicts.append(row_dict)
    
    return dicts
            

def get_data_from_query(sql_command):
    db = get_db()
    cursor = db.execute(sql_command)
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    data = sqlite_row_objs_to_list_of_dicts(data, column_names)
    logger.debug(data)
    
    return [] if data is None else data

def get_user_by_username(username: str) -> object:
    """gets user with specific username from database

    Args:
        username (str): users username

    Raises:
        DATA_NOT_FOUND_EXCEPTION: user not found

    Returns:
        object: object with users data
    """
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username, )
    ).fetchone()
    
    if not user:
        raise DATA_NOT_FOUND_EXCEPTION(error=f'Couldn\'t find user with username {username}.')
    
    return user