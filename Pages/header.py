from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
import Configuration.ReaderConfSystem as SysConfig
from flask_login import current_user, logout_user
from dash.dependencies import State, Input, Output
import dash_bootstrap_components as dbc
from Configuration.admin_users import user_get_name


def Header(app):
    # return html.Div([get_header(app), html.Br([]), get_menu()])
    return get_header(app)


def get_header(app):
    styleAdmin = {'visibility': 'hidden'} # if current_user.is_authenticated else {'visibility': 'visible'}
    Username = '_____'
    if current_user.is_authenticated:
        styleAdmin = {'visibility': 'visible'}
        print('Esta registrado')
        try:
            Username = user_get_name(int(current_user.get_id()))
        except:
            Username = '____'

    header = html.Div(
        [
            # html.Div(
            #     [
            #         html.Img(
            #             src=app.get_asset_url("imgs\\APL.png"),
            #             className="logo",
            #         ),
            #     ],
            #     className="row",
            # ),
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
            # html.Div([
            #     html.H2('', className='col-sm-3'),
            #     html.H2(SysConfig.NAME_SERVER, style={'background': 'red'}, className='col-sm-3'),
            #     html.Button("Log out", id='logout-button', n_clicks=0,
            #                          style={'background': 'blue'},
            #                          className='col-sm-3'
            #                          )],
            #     className="row",
            #     style={'background': 'green'},
            # ),
            # html.Br([]),
            get_menu(),
            html.Div(id="hidden-div", style={'display': 'none'}),
            html.A(html.Button('Refresh page'), href='/', id="hidden-div-2", style={'display': 'none'}, )
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
    # styleAdmin = {'visibility': 'hidden'} # if current_user.is_authenticated else {'visibility': 'visible'}
    # if current_user.is_authenticated:
    #     styleAdmin = {'visibility': 'visible'}
    #     print('Esta registrado get menu')

    menu_empty = html.Div([], className="row all-tabs")

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
            html.Div([], className='col-sm-4'),
            html.Div([
            dcc.Link(
                "Pestaña de registrado",
                href="/registrado_page",
                className="tab first",
            ),
            dcc.Link(
                "Administrar alarmas",
                href="/admin_alarms_page",
                className="tab",
            ),], className='col-sm-4'),
            html.Div([], className='col-sm-4'),

        ],
        className="all-tabs",
    )

    menu = menu_2 if current_user.is_authenticated else menu_empty

    return menu


def add_callback_header(app):
    @app.callback(
        Output(component_id='hidden-div', component_property='children'),
        [Input(component_id='logout-button', component_property='n_clicks')]
    )
    def log_out_header(n_clicks):
        if current_user.is_authenticated and n_clicks > 0:
            print('Id of current user {}'.format(current_user.id))
            try:
                del SysConfig.CURRENT_USERS[current_user.id]
            except Exception:
                pass
            logout_user()
            print('Ha salido el usuario {}'.format(current_user.id))
        return 1


