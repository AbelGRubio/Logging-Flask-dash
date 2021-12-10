from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from dash.dependencies import Input, Output, State


layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_confirmed_email_page', refresh=True),
                html.H1(["Email confirmation accepted"], style={'color': 'blue'}),
                html.Div(html.Button('Go back', id='submit-confirmed-email', n_clicks=0)
                         , className='margin-10px'),
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_confirmed_email_page', component_property='pathname'),
    [Input(component_id='submit-confirmed-email', component_property='n_clicks')]
)
def output_waiting_confirmed_email(n_clicks):
    if n_clicks > 0:
        print('Hace algo en waiting page')
        return '/sign_in_page'
    else:
        print('Pasa')
