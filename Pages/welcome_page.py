from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig


layout = html.Div(
    [
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
