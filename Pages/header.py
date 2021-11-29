import dash_html_components as html
import dash_core_components as dcc
import Configuration.ReaderConfSystem as SysConfig
from flask_login import current_user, logout_user
from dash.dependencies import State, Input, Output


def Header(app):
    # return html.Div([get_header(app), html.Br([]), get_menu()])
    return get_header(app)


def get_header(app):
    styleAdmin = {'visibility': 'hidden'} # if current_user.is_authenticated else {'visibility': 'visible'}
    if current_user.is_authenticated:
        styleAdmin = {'visibility': 'visible'}
        print('Esta registrado')

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
            html.Div(
                [
                    html.H2(SysConfig.NAME_SERVER),
                    html.Button(
                        "Log out",
                        id='logout-button',
                        n_clicks=0,
                        style=styleAdmin,
                    ),
                ],
                className='row'
            ),
            html.Br([]),
            get_menu(),
            html.Div(id="hidden-div", style={'display': 'none'})
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
    menu = html.Div(
        [
            dcc.Link(
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
            ),
            dcc.Link(
                "New password",
                href="/new_password_page",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def add_callback_header(app):
    @app.callback(
        Output(component_id='hidden-div', component_property='children'),
        [Input(component_id='logout-button', component_property='n_clicks')]
    )
    def log_out_header(n_clicks):
        if current_user.is_authenticated and n_clicks > 0:
            logout_user()
            print('Ha salido el usuario {}'.format(n_clicks))
        return 1


