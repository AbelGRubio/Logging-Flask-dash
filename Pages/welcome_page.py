from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig

layout = html.Div(
    [
        # Header(),
        html.Div(
            [
                dcc.Location(id='url_successful_page', refresh=True),
                html.H1(["Bienvenido a {}".format(SysConfig.NAME_SERVER)], style={'color': 'blue'}),
                html.H2(['Resumen de las alarmas'])
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    # className="page",
)
