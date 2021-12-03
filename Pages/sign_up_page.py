from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_new_user, check_password_strength
from email_validator import validate_email, EmailNotValidError
from flask_login import current_user
from Fun.send_email import create_email, send_mail


layout = html.Div(
    [Header(SysConfig.APP),
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
             html.H6(id='tituloh6', children='Fill the form and press Register', className='margin-10px')
         ],
         className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)

@SysConfig.APP.callback(
    Output(component_id='tituloh6', component_property='children'),
    [Input(component_id='register-button', component_property='n_clicks')],
    [State(component_id='input-username', component_property='value'),
     State(component_id='input-email', component_property='value'),
     State(component_id='input-password', component_property='value'),
     State(component_id='input-confirm-password', component_property='value')],
)
def update_sign_up_page(n_clicks, username, email, password, confirm_password):
    print('Ha entrado en el callback de la funcion')
    print([username, email, password, confirm_password])
    res = 'The input values are: {}, {}, {}, {}'.format(username, email, password, confirm_password)
    if None in [username, email, password, confirm_password]:
        return 'Fill the form and press Register'
    elif password != confirm_password:
        return 'Please the password is not the same'
    else:
        pass
    try:
        respuesta = check_password_strength(password)

        if respuesta['password_ok']:
            if True:
                res = 'User register complete! Wait for the email'
        else:
            res = 'The password must have upper case, lower case, \n ' \
                  'digits, minimun of 8 lenth and at least one symbol'

    except EmailNotValidError as e:
        res = 'Email not valid'
    return res


@SysConfig.APP.callback(Output('url_sign_up', 'pathname'),
              [Input('register-button', 'n_clicks'),],
                [State(component_id='input-username', component_property='value'),
                 State(component_id='input-email', component_property='value'),
                 State(component_id='input-password', component_property='value'),
                 State(component_id='input-confirm-password', component_property='value')]
                        )
def submit_sign_up_page(input1, username, email, password, confirm_password):
    # print('El usuario esta registrado? {}'.format(current_user.is_authenticated))
    if input1 > 0:
        if None not in [username, email, password, confirm_password] and password == confirm_password:
            valid = validate_email(email)
            email = valid.email
            respuesta = check_password_strength(password)

            if respuesta['password_ok']:
                print('registra? {}'.format(is_new_user(username=username, email=email, password=password)))
                SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(email, salt='email-confirm')
                url_token = 'http://192.168.127.105:8050/confirmed_email_page_{}'.format(SysConfig.TOKEN)
                mensage = create_email(is_confirmation=True,
                                       url_token=url_token,
                                       user_name=username)
                send_mail(mensage)

            print('Hace algo sign up')
            return '/waiting_register_page'
        else:
            print('Pasa rotundamente')
    else:
        print('Pasa')
