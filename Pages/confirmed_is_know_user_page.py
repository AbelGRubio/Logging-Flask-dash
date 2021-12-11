from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from dash.dependencies import Input, Output, State
from Configuration.admin_users import confirm_is_know_user
from Fun.send_email import send_mail_confirmation
import datetime


USER_NAME = ''
USER_MAIL = ''
NCLICK_CONFIRM = 0

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_is_know_user', refresh=True),
                html.H1(["Confirmed user with email {}".format(USER_NAME)], style={'color': 'blue'}),
                html.Div(html.Button('Confirm & Go back', id='mail-confirmation-user', n_clicks=NCLICK_CONFIRM)
                         , className='margin-10px'),
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_is_know_user', component_property='pathname'),
    [Input(component_id='mail-confirmation-user', component_property='n_clicks')]
)
def output_waiting(n_clicks):
    global NCLICK_CONFIRM
    if n_clicks != NCLICK_CONFIRM:
        print('Confirmed is_know_user')
        if confirm_is_know_user(USER_NAME):
            send_mail_confirmation(USER_MAIL, USER_NAME)
        return '/sign_in_page'
    else:
        print('Pasa')
