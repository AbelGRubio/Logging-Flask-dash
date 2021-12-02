from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig


layout = html.Div(
    [Header(SysConfig.APP),
     html.Div(
     [
         dcc.Location(id='url_recover_account', refresh=True),
         html.H1(["Recover account"], style={'color': 'blue'}),
        html.Div(dcc.Input(id='input-password', type='text', placeholder="Your email...")
                 , className='margin-10px'),
        html.Div(html.Button('Confirm', id='submit-recover', n_clicks=0)
                 , className='margin-10px'),
     ],
     className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_recover_account', component_property='pathname'),
    [Input(component_id='submit-recover', component_property='n_clicks')]
)
def output_recover(n_clicks):
    if n_clicks > 0:
        print('Hace algo en recover page')

        return '/waiting_password_page'
    else:
        print('Pasa')
