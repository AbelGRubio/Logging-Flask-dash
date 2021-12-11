import numpy as np
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import re


COLUMNS = ['id', 'Username', 'Confirm', 'Email', 'UserKnow', 'level', 'Password']
USERS_NAME_TXT = 'Users_new_format.txt'


def is_new_user(username: str, email, password):

    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
    except Exception:
        df = pd.DataFrame([], columns=COLUMNS)

    try:
        if username not in df['Username'].unique() and email not in df['Email'].unique():
            new_df = pd.DataFrame([], columns=COLUMNS)
            password = generate_password_hash(password)
            random_id = int(np.random.random() * (2 ** 20 - 1))
            new_df = new_df.append(dict(zip(new_df.columns, [random_id, username.lower(), False, email,
                                                             False, 1, password])),
                                   ignore_index=True)
            df_to_save = new_df.append(df)
            df_to_save.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=False)
            return True
        else:
            return False
    except Exception as e:
        print('ERROR: {}'.format(e))
        return False


def add_the_user(username: str, email, id_user: int,
                 level: int):

    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
    except Exception:
        df = pd.DataFrame([], columns=COLUMNS)

    try:
        if username not in df['Username'].unique() and email not in df['Email'].unique():
            new_df = pd.DataFrame([], columns=COLUMNS)
            new_df = new_df.append(dict(zip(new_df.columns, [id_user, username.lower(), False, email, 
                                                             True, level, 'no_password_yet'])),
                                   ignore_index=True)
            df_to_save = new_df.append(df)
            df_to_save.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=False)
            return True
        else:
            return False
    except Exception as e:
        print('ERROR: {}'.format(e))
        return False


def is_user(email):

    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t', index_col=0)
    except Exception:
        return False

    if email in df['Email'].unique():
        return True
    else:
        return False


def is_user_confirmed(email):
    value = False
    if email is None:
        return value
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t', index_col=0)
        value = list(df[df['Email'] == email]['Confirm'])[0]
    except Exception:
        value = False

    return value


def check_user(email, password):

    if is_user(email):
        try:
            df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        except Exception:
            df = pd.DataFrame([], columns=COLUMNS)

        password_hash = list(df[df['Email'] == email]['Password'])[0] # df['Password'].where(df['Email'] == email)[0]

        return check_password_hash(password_hash, password)
    else:
        return False


def user_get_password_hash(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        password_hash = list(df[df['Email'] == email]['Password'])[0]
    except Exception:
        password_hash = None
    return password_hash


def user_get_id(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        id_user = list(df[df['Email'] == email]['id'])[0]
    except Exception:
        id_user = None
    return id_user


def user_get_name(id: int):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        user_name = list(df[df['id'] == id]['Username'])[0]
    except Exception:
        user_name = 'Fallo get name'
    return user_name


class User(UserMixin):
    def __init__(self, id_user, email: str, password_hash: str, username: str):
        UserMixin.__init__(self)
        self.id = id_user
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return "{}".format(self.id)


def check_password_strength(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }


def confirm_is_know_user(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        df.at[list(df[df['Email'] == email].index)[0], 'UserKnow'] = True
        df.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=False)
        return True
    except Exception:
        id_user = False
    return id_user


def is_know_used(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        id_user = list(df[df['Email'] == email]['UserKnow'])[0]
    except Exception:
        id_user = False
    return id_user


def confirm_user(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        df.at[list(df[df['Email'] == email].index)[0], 'Confirm'] = True
        df.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=False)
        return True
    except Exception:
        id_user = False
    return id_user


def is_confirmed_used(email):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        id_user = list(df[df['Email'] == email]['Confirm'])[0]
        return id_user
    except Exception:
        id_user = False
    return id_user


def is_user_admin(idn: str):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        id_user = list(df[df['id'] == idn]['level'])[0] == 0
        return id_user
    except Exception:
        id_user = False
    return id_user


def change_new_password(email, new_password):
    try:
        df = pd.read_csv(USERS_NAME_TXT, sep='\t')
        new_token_password = generate_password_hash(new_password)
        df.loc[df['Email'] == email, 'Password'] = new_token_password
        df.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=False)
        return True
    except Exception:
        return False



