from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from dash.dependencies import Input, Output, State
from Configuration.admin_users import confirm_is_know_user
from Fun.send_email import send_mail_confirmation
import datetime


USER_NAME = ''
USER_MAIL = ''

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_is_know_user', refresh=True),
                html.H1(["Confirmed user with email {}".format(USER_NAME)], style={'color': 'blue'}),
                html.Div(html.Button('Confirm & Go back', id='mail-confirmation', n_clicks=0)
                         , className='margin-10px'),
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_is_know_user', component_property='pathname'),
    [Input(component_id='mail-confirmation', component_property='n_clicks')]
)
def output_waiting(n_clicks):
    if n_clicks > 0:
        print('Confirmed is_know_user')
        if confirm_is_know_user(USER_NAME):
            send_mail_confirmation(USER_MAIL, USER_NAME)
        # el_correo = '{}_{}'.format(USER_NAME, str(datetime.datetime.now()))
        # SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
        # url_token = 'http://{}:{}/confirmed_email_page_{}'.format(SysConfig.IP_HOST,
        #                                                           SysConfig.PORT_HOST,
        #                                                           SysConfig.TOKEN)
        # mensage = create_email(is_confirmation=True,
        #                        url_token=url_token,
        #                        user_name=USER_NAME,
        #                        email=USER_NAME)
        # send_mail(mensage)
        return '/sign_in_page'
    else:
        print('Pasa')
