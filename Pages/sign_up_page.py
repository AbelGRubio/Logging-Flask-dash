import datetime

from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_new_user, check_password_strength
from email_validator import validate_email, EmailNotValidError
from Fun.send_email import create_email, send_mail

layout = html.Div(
    [Header(),
     html.Div(
         [
             dcc.Location(id='url_sign_up', refresh=True),
             html.H1(["Sign up"], style={'color': 'blue'}),
             html.Div(dcc.Input(id='input-username', type='text', placeholder="Your username...")
                      , className='margin-10px'),
             html.Div(dcc.Input(id='input-email', type='text', placeholder="Your email...")
                      , className='margin-10px'),
             html.Div(dcc.Input(id='input-password', type='password', placeholder="Your password...")
                      , className='margin-10px'),
             html.Div(dcc.Input(id='input-confirm-password', type='password', placeholder="Confirm your password...")
                      , className='margin-10px'),
             html.Div(html.Button(children='Register', id='register-button', n_clicks=0)
                      , className='margin-10px'),
             html.Div(html.A('Back', href='sign_in_page', n_clicks=0)
                      , className='margin-10px'),
             html.H6(id='tituloh6', children='Fill the form and press Register', className='margin-10px')
         ],
         className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)


@SysConfig.APP.callback(
    [Output(component_id='tituloh6', component_property='children'),
     Output(component_id='url_sign_up', component_property='pathname')],
    [Input(component_id='register-button', component_property='n_clicks')],
    [State(component_id='input-username', component_property='value'),
     State(component_id='input-email', component_property='value'),
     State(component_id='input-password', component_property='value'),
     State(component_id='input-confirm-password', component_property='value')],
)
def update_sign_up_page(n_clicks, username, email, password, confirm_password):
    print('Ha entrado en el callback de la funcion')
    print([username, email, password, confirm_password])
    from flask import request
    print('current request path {}'.format(request.path))
    pathname = None
    if None in [username, email, password, confirm_password]:
        return 'Fill the form and press Register', pathname
    elif password != confirm_password:
        return 'Please the password is not the same', pathname
    else:
        try:
            respuesta = check_password_strength(password)
            valid = validate_email(email)
            email = valid.email
            if respuesta['password_ok']:
                if True:
                    res = 'User register complete! Wait for the email'
                    # print('registra? {}'.format(is_new_user(username=username, email=email, password=password)))
                    if is_new_user(username=username, email=email, password=password):
                        el_correo = '{}_{}'.format(email, str(datetime.datetime.now()))
                        SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
                        url_token = 'http://{}:{}/confirmed_is_know_user_page_{}'.format(SysConfig.IP_HOST,
                                                                                         SysConfig.PORT_HOST,
                                                                                         SysConfig.TOKEN)
                        mensage = create_email(is_know_user=True,
                                               url_token=url_token,
                                               user_name=username)
                        send_mail(mensage)
                        pathname = '/waiting_register_page'
            else:
                res = 'The password must have upper case, lower case, \n ' \
                      'digits, minimun of 8 lenth and at least one symbol'
        except EmailNotValidError as e:
            res = 'Email not valid'

    return res, pathname
