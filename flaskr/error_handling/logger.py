from logging.config import dictConfig

logger_config = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}

def configure_logger(config):
    try:
        dictConfig(config)
    except ValueError:
        raise ValueError
    except TypeError:
        raise TypeError
    except AttributeError:
        raise AttributeError
    except ImportError:
        raise ImportError
