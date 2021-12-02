from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig


layout = html.Div(
    [Header(SysConfig.APP),
     html.Div(
     [
        html.H1(["Bienvenido a {}".format(SysConfig.NAME_SERVER)], style={'color': 'blue'}),
        html.H2(['Resumen de las alarmas'])
     ],
     className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)

