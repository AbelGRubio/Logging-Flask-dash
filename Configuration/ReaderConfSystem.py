import configparser
import sys

from Configuration import LOGGER

ReaderConfig = configparser.ConfigParser()


# @@@@@@@@@@@@@ LECTURA DE LOS FICHEROS @@@@@@@@@@@@@@@@
try:
    ReaderConfig.read(r'ConfigurationFiles\Configuration.ini')
except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()


try:
    APP = None
    LOADED_TABLE = False
    NAME_SERVER = ReaderConfig['system']['name_server']
except Exception as e:
    LOGGER.debug('Could not find one of the config files! Mssg: {}'.format(e))
    sys.exit()
