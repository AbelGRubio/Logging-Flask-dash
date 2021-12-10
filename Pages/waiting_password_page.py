from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from dash.dependencies import Input, Output, State

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_waiting_password_page', refresh=True),
                html.H1(["We have sent an email to change the password"], style={'color': 'blue'}),
                html.Div(html.Button('Confirm', id='submit-waiting', n_clicks=0)
                         , className='margin-10px'),
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_waiting_password_page', component_property='pathname'),
    [Input(component_id='submit-waiting', component_property='n_clicks')]
)
def output_waiting_password(n_clicks):
    if n_clicks > 0:
        print('Hace algo en waiting page')

        return '/sign_in_page'
    else:
        print('Pasa')
