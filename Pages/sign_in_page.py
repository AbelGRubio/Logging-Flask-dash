import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import check_user, user_get_id, user_get_password_hash, User
from flask_login import login_user, logout_user, current_user, UserMixin


def create_layout(app):
    web = html.Div(
        [Header(app),
         html.Div(
         [
            html.H1(["Sign in"], style={'color': 'blue'}),
            html.Div(dcc.Input(id='input-email-sign-in', type='text', placeholder="Your email...")),
            html.Div(dcc.Input(id='input-password-sign-in', type='text', placeholder="Your password...")),
            html.Button('Sign in', id='submit-val', n_clicks=0),
            html.H6(['New in {}? '.format(SysConfig.NAME_SERVER),
                     dcc.Link(
                         "Create an account",
                         href="/sign_up_page",
                     ), ]),
            html.H6([dcc.Link(children="Forgot the password?", href="/recover_account_page"), ]),
            html.H6(id='titulo-sign-in', children='Fill the form and press sign in')
         ],
         className="row text-align-center",
         ),
         ],
        className="page",
    )
    if not SysConfig.CALLBACK_SIGN_IN:
        try:
            add_callback_sign_in(app)
            SysConfig.CALLBACK_SIGN_IN = True
        except Exception as e:
            print('El error es {}'.format(e))
            pass

    return web


def add_callback_sign_in(app):
    @app.callback(
        Output(component_id='titulo-sign-in', component_property='children'),
        [Input(component_id='submit-val', component_property='n_clicks'), ],
        [State(component_id='input-email-sign-in', component_property='value'),
         State(component_id='input-password-sign-in', component_property='value'),
         ],
    )
    def update_output(n_clicks, email, password):
        # print('Ha entrado en el callback de la funcion de sign in')
        # res = 'The input value was "{}" and the button has been clicked {} times'.format(
        #     email,
        #     n_clicks
        # )
        res = 'Fallo al registrarse'
        if check_user(email, password):
            try:
                password_hash = user_get_password_hash(email)
                id_user = user_get_id(email)
                new_user = User(id_user=id_user,
                                email=email,
                                password_hash=password_hash)
                SysConfig.CURRENT_USERS[int(id_user)] = new_user
                # print('ff = 1')
                login_user(new_user)
                res = 'Ha entrado el usuario'
            except Exception as e:
                print('FALLO {}'.format(e))
        return res


# def is_user(email):
#
#     try:
#         df = pd.read_csv('Users.txt', sep='\t', index_col=0)
#     except Exception:
#         df = pd.DataFrame([], columns=['Username', 'Email', 'Password'])
#
#     if email in df['Email'].unique():
#         return True
#     else:
#         return False
#
#
# def check_user(email, password):
#
#     if is_user(email):
#         try:
#             df = pd.read_csv('Users.txt', sep='\t')
#         except Exception:
#             df = pd.DataFrame([], columns=['Username', 'Email', 'Password'])
#
#         password_hash = df['Password'].where(df['Email'] == email)[0]
#
#         print(check_password_hash(password_hash, password))
#
#         return True
#     else:
#         return False
#
#
# def user_get_password_hash(email):
#     try:
#         df = pd.read_csv('Users.txt', sep='\t')
#         password_hash = df['Password'].where(df['Email'] == email)[0]
#     except Exception:
#         password_hash = None
#     return password_hash
#
#
# def user_get_id(email):
#     try:
#         df = pd.read_csv('Users.txt', sep='\t')
#         id = df['id'].where(df['Email'] == email)[0]
#     except Exception:
#         id = None
#     return id
#
