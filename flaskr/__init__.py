""" this file contains application factory
and tells python that flaskr directory
should be treated as a package
"""
import os

from flask import Flask

def create_app(test_config=None):
    # configure logger
    from .error_handling.logger import configure_logger, logger
    configure_logger()
 
    logger.info('Logger configured.')

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    logger.info('App created.')
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        logger.info('Loaded configuration.')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        logger.info('Loaded test configuration.')
    
    # ensure the instance config folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from .routes import user
    app.register_blueprint(user.bp)
    
    logger.info('Registered blueprints.')
    
    return app
