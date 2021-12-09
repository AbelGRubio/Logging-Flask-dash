from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import check_user, user_get_id, user_get_password_hash, User, is_user_confirmed, user_get_name
from flask_login import login_user, current_user
from flask import redirect
import time


layout = html.Div(
    [
        dcc.Location(id='url_sign_in',  refresh=True),
        Header(),
        html.Div(
            [
                html.H1(["Sign in"], style={'color': 'blue'}),
                html.Div(dcc.Input(id='input-email-sign-in', type='text', placeholder="Your email...",
                              ), className='margin-10px'),
                html.Div(dcc.Input(id='input-password-sign-in', type='password', placeholder="Your password...",
                          ), className='margin-10px'),
                html.Div(html.Button('Sign in', id='submit-val', type='submit', n_clicks=0, className='margin-10px'
                             )),
                html.H6(['New in {}? '.format(SysConfig.NAME_SERVER),
                         html.A(
                             children="Create an account",
                             href="/sign_up_page",
                         ), ], className='margin-10px'),
                html.H6([html.A(children="Forgot the password?", href="/recover_account_page"),],
                        className='margin-10px'),
                html.H6(id='titulo-sign-in', children='Fill the form and press sign in', className='margin-10px')
         ],
            className="row text-align-center",
        ),
    ],
    className="page",
)


@SysConfig.APP.callback(
    [Output(component_id='titulo-sign-in', component_property='children'),
     Output(component_id='url_sign_in', component_property='pathname')],
    [Input(component_id='submit-val', component_property='n_clicks'), ],
    [State(component_id='input-email-sign-in', component_property='value'),
     State(component_id='input-password-sign-in', component_property='value'),
     ],
)
def update_sign_in(n_clicks, email, password):
    res = 'Error at sign in'
    pathname = None
    if not is_user_confirmed(email):
        return 'The user is not confirmed', pathname
    if check_user(email, password):
        pathname = '/sign_in_page'
        try:
            password_hash = user_get_password_hash(email)
            id_user = user_get_id(email)
            name_user = user_get_name(id_user)
            new_user = User(id_user=id_user,
                            email=email,
                            password_hash=password_hash,
                            username=name_user)
            SysConfig.CURRENT_USERS[int(id_user)] = new_user
            login_user(new_user)
            res = 'User registered with name {}'.format(name_user)

            if current_user.is_authenticated:
                if n_clicks >= 0:
                    pathname = '/beginning_page'
                    return res, pathname
                else:
                    print('Pasa')
        except Exception as e:
                print('FALLO {}'.format(e))
    else:
        res = 'The password is incorrect'
    # redirect(pathname, code=302)
    return res, pathname


