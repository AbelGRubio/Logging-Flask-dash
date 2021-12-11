from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from flask_login import current_user, logout_user
from dash.dependencies import State, Input, Output
import dash_bootstrap_components as dbc
from Configuration.admin_users import is_user_admin


def get_user_name():
    Username = ' '
    if str(current_user) != 'None':
        if current_user.is_authenticated:
            Username = current_user.username
    return Username


def get_style():
    styleAdmin = {'visibility': 'hidden'}  # if current_user.is_authenticated else {'visibility': 'visible'}
    if str(current_user) != 'None':
        if current_user.is_authenticated:
            styleAdmin = {'visibility': 'visible'}
    return styleAdmin


def get_menu():
    menu_empty = html.Div([], className="row all-tabs")

    if str(current_user) == 'None':
        return menu_empty

    user_menu = dbc.Row(
        [
            html.Div([], className='col-sm-3'),
            html.Div([
                dcc.Link("Resumen_alarmas",
                         href="welcome_page",
                         className="tab first"),
                dcc.Link("Pestaña de registrado",
                         href="registrado_page",
                         className="tab"),
                dcc.Link("Administrar alarmas",
                         href="admin_alarms_page",
                         className="tab"),
            ], className='col-sm-6'),
            html.Div([], className='col-sm-3'),

        ],
        className="all-tabs",
    )
    user_admin = dbc.Row(
        [
            html.Div([], className='col-sm-3'),
            html.Div([
                dcc.Link("Resumen_alarmas",
                         href="welcome_page",
                         className="tab first"),
                dcc.Link("Pestaña de registrado",
                         href="registrado_page",
                         className="tab"),
                dcc.Link("Administrar alarmas",
                         href="admin_alarms_page",
                         className="tab"),
                dcc.Link("Administrar usuarios",
                         href="admin_users_page",
                         className="tab"),
            ], className='col-sm-6'),
            html.Div([], className='col-sm-3'),

        ],
        className="all-tabs",
    )
    menu = user_admin if is_user_admin(current_user.id) else user_menu

    return menu


def get_row_identification():
    return dbc.Row(
        children=[
            dbc.Col(html.H2(get_user_name()),
                    style=get_style(),
                    ),
            dbc.Col(html.Button("Log out", id='logout-button', n_clicks=0,
                                style=get_style(),
                                ), className='text-align-right')
        ]
    )


header = html.Div(
    [
        dcc.Location(id='url_header', refresh=True),
        html.H2(SysConfig.NAME_SERVER, className='title'),
    ],
    className="margin-10px",
)


def Header():
    return header


@SysConfig.APP.callback(
    Output(component_id='url_header', component_property='pathname'),
    [Input(component_id='logout-button', component_property='n_clicks'), ]
)
def log_out_header(n_clicks):
    if current_user is None:
        return ''

    if current_user.is_authenticated and n_clicks > 0:
        print('Id of current user {}'.format(current_user.id))
        try:
            del SysConfig.CURRENT_USERS[current_user.id]
        except Exception:
            pass
        print('Va a salir el usuario {}'.format(current_user.id))
        logout_user()
        from Pages.routes import load_sign_in_page
        load_sign_in_page()
        # from flask import redirect
        # redirect('.', code=302)
        return '/'


