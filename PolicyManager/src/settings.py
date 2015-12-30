import logging, os
__author__ = 'r2h2'

LOGFILENAME = os.path.abspath(os.path.join('log', __name__ + '.debug'))
LOGGING = dict(
    version = 1,
    formatters = {
        'long': {'format': '%(asctime)s - %(levelname)s  [%(filename)s:%(lineno)s] %(message)s'},
        'short': {'format': '%(levelname)-6s %(message)s'},
        },
    handlers = {
        'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'short',
              'level': logging.INFO
        },
        'file': {
              'class': 'logging.FileHandler',
              'formatter': 'long',
              'level': logging.DEBUG,
              'filename': LOGFILENAME,
              'mode': 'w',
        },
    },
    loggers = {
        '': {'handlers': ['file', 'console'], 'level': logging.DEBUG,}
    },
)
