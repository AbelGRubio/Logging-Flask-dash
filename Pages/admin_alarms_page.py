from dash import html, dcc

layout = html.Div(
    [
        dcc.Location(id='url_admin_alarms', refresh=True),
        html.Div(
            [
                html.Br([]),
                html.Div([
                    html.Table([
                        html.Tr([html.Th('Hz file'),
                                 html.Th('nPoints'),
                                 html.Th('Percentage')]),
                        html.Tr([html.Td(1000),
                                 html.Td(6000),
                                 html.Td(95)])],
                        style={'width': '70%', 'margin-left': '15%', 'margin-right': '15%'},
                    )
                ])
            ],
            className="row  margin-10px",
            # style={'margin-left': '10px', 'margin-right': '10px'}
        ),
    ],
    className=" margin-10px",
)

