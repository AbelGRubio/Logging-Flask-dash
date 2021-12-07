from dash import html, dcc
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from dash.dependencies import Input, Output, State


layout = html.Div(
    [Header(),
     html.Div(
     [
         dcc.Location(id='url_forbidden_page', refresh=True),
         html.H1(["Email confirmation accepted"], style={'color': 'blue'}),
         html.Div(html.Button('Go back', id='submit-forbidden', n_clicks=0)
                  , className='margin-10px'),
     ],
     className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_forbidden_page', component_property='pathname'),
    [Input(component_id='submit-forbidden', component_property='n_clicks')]
)
def output_waiting(n_clicks):
    if n_clicks > 0:
        print('Hace algo en waiting page')
        return '/sign_in_page'
    else:
        print('Pasa')

