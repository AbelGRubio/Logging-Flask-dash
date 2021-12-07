from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from flask_login import login_required


layout = html.Div(
    [Header(),
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
        return admin_alarms_page.layout
    elif pathname == '/registrado_page':
        import Pages.registrado_page as registrado_page
        return registrado_page.layout
    else:  # pathname == '/successful_page':
        import Pages.welcome_page as welcome_page
        return welcome_page.layout
