""" this file contains application factory
and tells python that flaskr directory
should be treated as a package
"""
import os

from flask import Flask
from logging.config import fileConfig

def create_app(test_config=None):
    # configure logger
    from .error_handling.logger import logger_config, configure_logger
    configure_logger(logger_config)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance config folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from .routes import auth
    app.register_blueprint(auth.bp)
    
    from .routes import user
    app.register_blueprint(user.bp)
    
    return app
