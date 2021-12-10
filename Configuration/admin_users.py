import numpy as np
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import re


def is_new_user(username: str, email, password):

    try:
        df = pd.read_csv('Users.txt', sep='\t')
    except Exception:
        df = pd.DataFrame([], columns=['id', 'Username', 'Confirm', 'Email', 'Password', 'UserKnow', 'level'])

    try:
        if username not in df['Username'].unique() and email not in df['Email'].unique():
            new_df = pd.DataFrame([], columns=['id', 'Username', 'Confirm', 'Email', 'Password', 'UserKnow', 'level'])
            password = generate_password_hash(password)
            random_id = int(np.random.random() * (2 ** 20 - 1))
            new_df = new_df.append(dict(zip(new_df.columns, [random_id, username.lower(), False, email, password,
                                                             False, 1])),
                                   ignore_index=True)
            df_to_save = new_df.append(df)
            df_to_save.to_csv('Users.txt', sep='\t', index=False)
            return True
        else:
            return False
    except Exception as e:
        print('ERROR: {}'.format(e))
        return False


def is_user(email):

    try:
        df = pd.read_csv('Users.txt', sep='\t', index_col=0)
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
        df = pd.read_csv('Users.txt', sep='\t', index_col=0)
        value = list(df[df['Email'] == email]['Confirm'])[0]
    except Exception:
        value = False

    return value


def check_user(email, password):

    if is_user(email):
        try:
            df = pd.read_csv('Users.txt', sep='\t')
        except Exception:
            df = pd.DataFrame([], columns=['id', 'Username', 'Confirm', 'Email', 'Password', 'UserKnow', 'level'])

        password_hash = list(df[df['Email'] == email]['Password'])[0] # df['Password'].where(df['Email'] == email)[0]

        # print('Es correcta la constraseña? {}'.format(check_password_hash(password_hash, password)))

        return check_password_hash(password_hash, password)
    else:
        return False


def user_get_password_hash(email):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # password_hash = df['Password'].where(df['Email'] == email)[0]
        password_hash = list(df[df['Email'] == email]['Password'])[0]
    except Exception:
        password_hash = None
    return password_hash


def user_get_id(email):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
        id_user = list(df[df['Email'] == email]['id'])[0]
    except Exception:
        id_user = None
    return id_user


def user_get_name(id: int):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
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
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
        df.at[list(df[df['Email'] == email].index)[0], 'UserKnow'] = True
        df.to_csv('Users.txt', sep='\t', index=False)
        return True
    except Exception:
        id_user = False
    return id_user


def is_know_used(email):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
        id_user = list(df[df['Email'] == email]['UserKnow'])[0]
    except Exception:
        id_user = False
    # print('El usuario esta confirmado? {}'.format(id_user))
    return id_user


def confirm_user(email):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
        df.at[list(df[df['Email'] == email].index)[0], 'Confirm'] = True
        df.to_csv('Users.txt', sep='\t', index=False)
        return True
    except Exception:
        id_user = False
    return id_user


def is_confirmed_used(email):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        # id_user = int(float(df['id'].where(df['Email'] == email)[0]))
        id_user = list(df[df['Email'] == email]['Confirm'])[0]
        # df.at[list(df[df['Email'] == email].index)[0], 'Confirm'] = True
        # df.to_csv('Users.txt', sep='\t', index=False)
        return id_user
    except Exception:
        id_user = False
    # print('El usuario esta confirmado? {}'.format(id_user))
    return id_user


def change_new_password(email, new_password):
    try:
        df = pd.read_csv('Users.txt', sep='\t')
        new_token_password = generate_password_hash(new_password)
        df.loc[df['Email'] == email, 'Password'] = new_token_password
        df.to_csv('Users.txt', sep='\t', index=False)
        return True
    except Exception:
        return False



