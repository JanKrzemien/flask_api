import sqlite3
import click
from flask import current_app, g
from .error_handling.logger import logger

def get_db():
    """connects to database if connection wasn't established yet

    Returns:
        special type g: special object used for db connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db


def close_db(e=None):
    """close connection to db"""
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

@click.command('init-db')
def init_db():
    """create db from sql script file"""
    db = get_db()
    
    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf8'))
    
    logger.info('Initialized the database.')
    

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
