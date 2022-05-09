import logging
import logging.config
import os

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def setup_logging(log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    config = {
        'formatters': {
            'simple': {
                '()': RequestFormatter,
                'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        'handlers': {
            'console': {
                'stream': 'ext://sys.stdout',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'DEBUG'
            },
            'error_file_handler': {
                'encoding': 'utf8',
                'when': 'D',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(log_path, 'error.log'),
                'level': 'ERROR',
                'formatter': 'simple'
            },
            'info_file_handler': {
                'encoding': 'utf8',
                'when': 'D',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(log_path, 'info.log'),
                'level': 'INFO',
                'formatter': 'simple'
            }
        },
        'disable_existing_loggers': False,
        'loggers': {
            'my_module': {
                'propagate': False,
                'handlers': ['console'],
                'level': 'ERROR'
            }
        },
        'root': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler'],
            'level': 'INFO'
        },
        'version': 1
    }

    logging.config.dictConfig(config)
