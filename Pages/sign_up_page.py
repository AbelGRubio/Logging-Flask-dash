from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_new_user, check_password_strength
from email_validator import validate_email, EmailNotValidError


def create_layout(app):
    web = html.Div(
        [Header(app),
         html.Div(
             [
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
    # print('ha cargado la pagina de registro {}'.format(datetime.datetime.now()))
    # print('Status load callback {}'.format(SysConfig.CALLBACK_SIGN_UP))
    if not SysConfig.CALLBACK_SIGN_UP:
        try:
            add_callback_sign_up(app)
            SysConfig.CALLBACK_SIGN_UP = True
            # print('Añadido el callback {}'.format(SysConfig.CALLBACK_SIGN_UP))
        except Exception as e:
            print('El error es {}'.format(e))
            pass
    return web


def add_callback_sign_up(app):
    @app.callback(
        Output(component_id='tituloh6', component_property='children'),
        [Input(component_id='register-button', component_property='n_clicks')],
        [State(component_id='input-username', component_property='value'),
         State(component_id='input-email', component_property='value'),
         State(component_id='input-password', component_property='value'),
         State(component_id='input-confirm-password', component_property='value')],
    )
    def update_output(n_clicks, username, email, password, confirm_password):
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
            valid = validate_email(email)
            email = valid.email
            respuesta = check_password_strength(password)

            if respuesta['password_ok']:
                if is_new_user(username=username, email=email, password=password):
                    res = 'User register complete! Wait for the email'
                else:
                    res = 'The username or email already exists!'
            else:
                res = 'The password must have upper case, lower case, \n ' \
                      'digits, minimun of 8 lenth and at least one symbol'

        except EmailNotValidError as e:
            res = 'Email not valid'
        return res


# def is_new_user(username: str, email, password):
#
#     try:
#         df = pd.read_csv('Users.txt', sep='\t')
#     except Exception:
#         df = pd.DataFrame([], columns=['id', 'Username', 'Email', 'Password'])
#
#     try:
#         if username not in df['Username'].unique() and email not in df['Email'].unique():
#             new_df = pd.DataFrame([], columns=['id', 'Username', 'Email', 'Password'])
#             password = generate_password_hash(password)
#             random_id = int(np.random.random() * (2 ** 20 - 1))
#             new_df = new_df.append(dict(zip(new_df.columns, [random_id, username.lower(), email, password])),
#                                    ignore_index=True)
#             df_to_save = new_df.append(df)
#             df_to_save.to_csv('Users.txt', sep='\t', index=False)
#             return True
#         else:
#             return False
#     except Exception as e:
#         print('ERROR: {}'.format(e))
#         return False
