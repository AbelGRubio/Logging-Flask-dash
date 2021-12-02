import configparser
import sys

from Configuration import LOGGER
from flask_login import LoginManager, UserMixin


ReaderConfig = configparser.ConfigParser()


# @@@@@@@@@@@@@ LECTURA DE LOS FICHEROS @@@@@@@@@@@@@@@@
try:
    ReaderConfig.read(r'ConfigurationFiles\Configuration.ini')
except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()


try:
    SERVER = None  #Flask(__name__)
    APP = None
    # APP = dash.Dash(
    #     name=__name__,
    #     external_stylesheets=[dbc.themes.BOOTSTRAP],
    #     meta_tags=[{"name": "viewport", "content": "width=device-width"},],
    #     server=SERVER)

    LOADED_TABLE = False
    NAME_SERVER = ReaderConfig['system']['name_server']

    USER_PASSWORDS = {'root': 'prueba'}

    USER_IS_LOGGED = True

    TIME_SLEEP_AFTER_SIGN_IN_OUT_UP = 2

    CALLBACK_SIGN_IN = False
    CALLBACK_SIGN_UP = False
    CALLBACK_RECOVER_ACCOUNT = False
    CALLBACK_NEW_PASSWORD = False
    CALLBACK_SUCESSFUL = False
    CALLBACK_HEADER = False

    LOGIN_MANAGER = LoginManager()

    CURRENT_USERS = {}

except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    user_id = int(float(user_id))
    # print('the user id is {}'.format(user_id))
    return CURRENT_USERS[user_id]

