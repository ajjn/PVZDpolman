import simplejson as json
import logging
import os
import shutil

class ConfigReader:
    """
    Read confing from home directory, or from defaults if there is not config in HOME
    """
    def __init__(self):
        try:
            fpath_home = os.path.join(os.environ['HOME'], 'patool_config.json')
            with open(os.path.join(fpath_home), 'r') as fd:
                conf = json.loads(fd.read())
        except Exception as e:
            # After a fresh install we need to initialize the settings from defaults
            logging.info('unable to read user-specific config file ' + fpath_home + '\n' + str(e))
            fpath_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_default.json')
            with open(os.path.join(fpath_default), 'r') as fd:
                j = fd.read()
                conf = json.loads(j)
            logging.info('set gui config to defaults')
            shutil.copy(fpath_default, fpath_home)
            logging.info('created gui config in home directory')

        self.SMTP_SMART_HOST = conf['EMail Account']['SMTP_SMART_HOST']
        self.SMTP_PORT = conf['EMail Account']['SMTP_PORT']
        self.ACCOUNT = conf['EMail Account']['ACCOUNT']
        self.PASSWORD = conf['EMail Account']['PASSWORD']
        self.USE_TLS = conf['EMail Account']['USE_TLS']
        self.RECIPIENT = conf['EMail Account']['RECIPIENT']
        self.TITLE = conf['EMail Account']['TITLE']
        self.FROM = conf['EMail Account']['FROM']

        self.MAIN_WINDOW_HEIGHT = conf['Default window sizes']['MAIN_WINDOW_HEIGHT']
        self.MAIN_WINDOW_WIDTH = conf['Default window sizes']['MAIN_WINDOW_WIDTH']
        self.CREATE_ED_WINDOW_HEIGHT = conf['Default window sizes']['CREATE_ED_WINDOW_HEIGHT']
        self.CREATE_ED_WINDOW_WIDTH = conf['Default window sizes']['CREATE_ED_WINDOW_WIDTH']
        self.DELETE_ED_WINDOW_HEIGHT = conf['Default window sizes']['DELETE_ED_WINDOW_HEIGHT']
        self.DELETE_ED_WINDOW_WIDTH = conf['Default window sizes']['DELETE_ED_WINDOW_WIDTH']

        self.PADDING = conf['Other GUI options']['PADDING']
        self.RECENTS_MAX_SIZE = conf['Other GUI options']['RECENTS_MAX_SIZE']
        self.BUTTON_HEIGHT = conf['Other GUI options']['BUTTON_HEIGHT']
        self.TWO_LINES_BUTTON_HEIGHT = conf['Other GUI options']['TWO_LINES_BUTTON_HEIGHT']
        self.BUTTON_WIDTH = conf['Other GUI options']['BUTTON_WIDTH']
        self.GUI_SAVED_SETTINGS_FILE = conf['Other GUI options']['GUI_SAVED_SETTINGS_FILE']
        self.FONT_SIZE = conf['Other GUI options']['FONT_SIZE']
        self.FONT_FAMILY = conf['Other GUI options']['FONT_FAMILY']