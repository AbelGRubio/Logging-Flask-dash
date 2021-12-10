import time

from dash import html, dcc
from dash.dependencies import Input, Output, State
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import change_new_password, check_password_strength
from email_validator import validate_email, EmailNotValidError

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_new_password', refresh=True),
                html.H1(["New password "], style={'color': 'blue'}),
                html.Div(dcc.Input(id='input-new-password', type='password', placeholder="Your new password...")),
                html.Div(dcc.Input(id='input-confirm-new-password', type='password',
                                   placeholder="Confirm your password...")),
                html.Button('Confirm', id='submit-new-password', n_clicks=0),
                html.H6(id='new_password_title', children=' ', className='margin-10px')
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="page",
)

USER_EMAIL = ''


@SysConfig.APP.callback(
    [Output(component_id="new_password_title", component_property='children'),
     Output(component_id='url_new_password', component_property='pathname')],
    Input(component_id='submit-new-password', component_property='n_clicks'),
    [State(component_id="input-new-password", component_property='value'),
     State(component_id="input-confirm-new-password", component_property='value')]
)
def new_password_action(n_clicks_submit, new_password: str, confirm_new_password: str):
    pathname = None
    try:
        if n_clicks_submit > 0:
            if None in [new_password, confirm_new_password]:
                return 'Fill the form and press Register', pathname
            elif new_password != confirm_new_password:
                return 'Please the password is not the same', pathname
            else:
                respuesta = check_password_strength(new_password)
                if respuesta['password_ok']:
                    valid = validate_email(USER_EMAIL)
                    email = valid.email
                    change_new_password(email, new_password)
                    print('Se ha cambiado para el usuario {}'.format(email))
                    pathname = '/sign_in_page'
                    time.sleep(2)
                    return '', pathname
                else:
                    return 'The password must have upper case, lower case, ' \
                           'digits, minimun of 8 lenth and at least one symbol', pathname
        else:
            return 'Fill the form and press confirm', pathname
    except EmailNotValidError as e:
        res = 'Email not valid'
        return res, pathname
