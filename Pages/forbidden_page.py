from dash import html, dcc

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url_forbidden_page', refresh=True),
                html.H2("Forbidden URL", className='title'),
                # html.Img(src='assets/imgs/forbidden-sign.jpg', style={'width': '40%', 'height': '40%'}),
            ],
            className="row margin-10px",
        ),
    ],
    className="page align-content-center",
)
