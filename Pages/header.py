from dash import html, dcc
import Configuration.ReaderConfSystem as SysConfig
from flask_login import current_user, logout_user
from dash.dependencies import State, Input, Output
import dash_bootstrap_components as dbc
from Configuration.admin_users import user_get_name


def Header():
    return get_header(SysConfig.APP)


def get_header(app):
    styleAdmin = {'visibility': 'hidden'}  # if current_user.is_authenticated else {'visibility': 'visible'}
    Username = '_____'
    if str(current_user) != 'None':
        if current_user.is_authenticated:
            styleAdmin = {'visibility': 'visible'}
            print('Esta registrado')
            try:
                Username = user_get_name(int(current_user.get_id()))
            except:
                Username = '____'

    header = html.Div(
        [
            dcc.Location(id='url_header', refresh=True),
            html.H2(SysConfig.NAME_SERVER, className='title'),
            dbc.Row(
                children=[
                    dbc.Col(html.H2(Username),
                            style=styleAdmin,
                            ),
                    dbc.Col(html.Button("Log out", id='logout-button', n_clicks=0,
                                        style=styleAdmin,
                                        ), className='text-align-right')
                ]
            ),
            get_menu(),
            html.Div(id="hidden-div", style={'display': 'none'}),
            # html.A(html.Button('Refresh page'), href='/', id="hidden-div-2", )
        ],
        className="margin-10px",
    )
    # print('añadimos funciones header')
    if not SysConfig.CALLBACK_HEADER:
        # print('Intentando cargar funciones')
        try:
            add_callback_header(app)
            SysConfig.CALLBACK_HEADER = True
        except Exception as e:
            print('El error es {}'.format(e))
            pass
        # print('Ha cargado las funciones del header')

    return header


def get_menu():
    menu_empty = html.Div([], className="row all-tabs")

    if str(current_user) == 'None':
        return menu_empty

    menu_1 = dbc.Row(
        [
            html.Div([], className='col-sm-4'),
            html.Div([dcc.Link(
                "Sign in",
                href="/sign_in_page",
                className="tab first",
            ),
                dcc.Link(
                    "Sign up",
                    href="/sign_up_page",
                    className="tab",
                ),
                dcc.Link(
                    "Recover account",
                    href="/recover_account_page",
                    className="tab",
                )], className='col-sm-4'),
            html.Div([], className='col-sm-4'),
        ],
        className="all-tabs",
    )

    menu_2 = dbc.Row(
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

    menu = menu_2 if current_user.is_authenticated else menu_empty

    return menu


def add_callback_header(app):
    @app.callback(
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

    # @app.callback(
    #     Output(component_id='url_header', component_property='pathname'),
    #     [Input(component_id='load_successful_page_header', component_property='n_clicks')]
    # )
    # def load_new_page(n_clicks):
    #     from Pages.routes import load_successful_page
    #     load_successful_page()
    #     return '/successful_page'
