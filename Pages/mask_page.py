from dash import html, dcc
from dash.dependencies import Input, Output
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from flask_login import login_required
import copy
from Fun.funtions import get_row_identification

layout = html.Div(
    [
        Header(),
        dcc.Location(id='url_mask', refresh=False),
        html.Div(id='page-content'),
    ],
    className="page",
)


@SysConfig.APP.callback(Output("page-content", "children"), [Input("url_mask", "pathname")])
@login_required
def display_page(pathname):
    if pathname == '/admin_alarms_page':
        import Pages.admin_alarms_page as admin_alarms_page
        layout_to_show = copy.copy(admin_alarms_page.layout)
    elif pathname == '/registrado_page':
        import Pages.registrado_page as registrado_page
        layout_to_show = copy.copy(registrado_page.layout)
    else:  # pathname == '/successful_page':
        import Pages.welcome_page as welcome_page
        layout_to_show = copy.copy(welcome_page.layout)

    return html.Div(children=[get_row_identification(), layout_to_show])
