from dash import html, dcc
from dash.dependencies import Input, Output
from Pages.header import Header, get_row_identification, get_menu
from flask_login import current_user
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_user_admin
from flask_login import login_required
import Pages.admin_users_page as admin_user_page
import Pages.admin_alarms_page as admin_alarms_page
import Pages.registrado_page as registrado_page
import Pages.welcome_page as welcome_page

layout = html.Div(
    [
        Header(),
        dcc.Location(id='url_mask', refresh=False),
        html.Div(id='page-content', className="margin-10px"),
    ],
    className="page",
)


@SysConfig.APP.callback(Output("page-content", "children"), [Input("url_mask", "pathname")])
@login_required
def display_page(pathname):
    print(' {} -- {}'.format(pathname, current_user))
    if pathname == '/admin_alarms_page':
        layout_to_show = admin_alarms_page.layout
    elif pathname == '/registrado_page':
        layout_to_show = registrado_page.layout
    elif pathname == '/admin_users_page' and is_user_admin(current_user.id):
        layout_to_show = admin_user_page.layout
    else:  # pathname == '/successful_page':
        layout_to_show = welcome_page.layout

    return html.Div(children=[get_menu(), get_row_identification(), layout_to_show])
