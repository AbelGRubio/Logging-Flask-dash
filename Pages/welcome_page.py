from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Fun.funtions import get_row_identification


layout = html.Div(
    [
        # Header(),
        # get_row_identification(),
        html.Div(
            [
                dcc.Location(id='url_successful_page', refresh=True),
                html.H1(["Bienvenido a {}".format(SysConfig.NAME_SERVER)], style={'color': 'blue'}),
                html.H2(['Resumen de las alarmas'])
            ],
            className="row text-align-center margin-10px",
        ),
    ],
    className="margin-10px",
)
