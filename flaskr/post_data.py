from flaskr.db import get_db

def post_data_using_query(sql_command: str, args: list):
    error = None
    db = get_db()
    try:
        db.execute(sql_command,args)
        db.commit()
    except Exception as e:
        print(e)
        error = 'Error while creating user.'
    return error