from flaskr.db import get_db

def get_data_from_query(sql_command):
    db = get_db()
    data = db.execute(sql_command).fetchall()
    
    return [] if data is None else data