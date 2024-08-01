from flaskr.db import get_db
from .error_handling.logger import logger

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