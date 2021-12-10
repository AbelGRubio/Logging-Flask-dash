import configparser
import sys
import os
from Configuration import LOGGER
from flask_login import LoginManager, UserMixin
from itsdangerous import URLSafeTimedSerializer


ReaderConfig = configparser.ConfigParser()


# @@@@@@@@@@@@@ LECTURA DE LOS FICHEROS @@@@@@@@@@@@@@@@
try:
    ReaderConfig.read(r'ConfigurationFiles\Configuration.ini')
except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()


try:
    SERVER = None
    APP = None

    LOADED_TABLE = False
    NAME_SERVER = ReaderConfig['system']['name_server']

    USER_PASSWORDS = {'root': 'prueba'}

    USER_IS_LOGGED = True

    TIME_SLEEP_AFTER_SIGN_IN_OUT_UP = int(ReaderConfig['system']['time_sleep_after_sign_in_out_up'])

    IP_HOST = ReaderConfig['system']['ip_host']
    PORT_HOST = int(ReaderConfig['system']['port_host'])

    IMG_LOGO_PATH = ReaderConfig['system']['path_logo_mensaje']
    with open(IMG_LOGO_PATH, 'rb') as f:
        IMG_LOGO = f.read()

    MAIL_SENDER = ReaderConfig['system']['email']
    MAIL_PASSWORD = ReaderConfig['system']['password']
    # lista de correos para enviar la confirmacion de la cuenta
    # MAIL_RECEIVER = ReaderConfig['system']['receiver'].split(',')
    MAIL_MANAGER = ReaderConfig['system']['manager_email'].split(',')

    MAIL_SUBJECT_EMAIL_CONFIRMATION = 'Email confirmation for {}'
    MAIL_SUBJECT_EMAIL_IS_KNOW_USER = 'Email is know user for {}'
    MAIN_SUBJECT_EMAIL_RECUPERATION = 'Recuperation email for {}'

    MAX_AGE_TOKENS = 60

    CALLBACK_HEADER = False

    LOGIN_MANAGER = LoginManager()

    CURRENT_USERS = {}

    SECRET = os.urandom(12)

    GEN_TOKENS = URLSafeTimedSerializer(SECRET)
    TOKEN = None

except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    user_id = int(float(user_id))
    # print('the user id is {}'.format(user_id))
    return CURRENT_USERS[user_id]

