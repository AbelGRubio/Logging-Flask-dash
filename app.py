import dash
from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import Configuration.ReaderConfSystem as SysConfig
from Configuration import LOGGER
from flask import Flask, request, redirect
from flask_login import current_user, logout_user
import os
import dash_bootstrap_components as dbc


if __name__ == '__main__':

    # Setup the Flask server
    SysConfig.SERVER = Flask(__name__)

    SysConfig.SERVER.config.update(
        SECRET_KEY=os.urandom(12),
    )

    SysConfig.APP = dash.Dash(
        name=__name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{"name": "viewport", "content": "width=device-width"},],
        server=SysConfig.SERVER)
    # server = app.server
    SysConfig.APP.config['suppress_callback_exceptions'] = True
    SysConfig.APP.title = 'ALERION'

    # Describe the layout/ UI of the app
    SysConfig.APP.layout = html.Div(
        [html.Div(id="page-content"), dcc.Location(id="url", refresh=False)]
    )

    SysConfig.LOGIN_MANAGER.init_app(SysConfig.SERVER)
    SysConfig.LOGIN_MANAGER.login_view = '/sign_up_page'
    SysConfig.LOGIN_MANAGER.refresh_view = '/registrado_page'

    # Update page
    @SysConfig.APP.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        try:
            if pathname == '/recover_account_page':
                import Pages.recover_account_page as recover_account_page
                return recover_account_page.layout
            elif pathname == '/sign_up_page':
                import Pages.sign_up_page as sign_up_page
                return sign_up_page.layout
            elif pathname == '/sign_in_page':
                import Pages.sign_in_page as sign_in_page
                return sign_in_page.layout
            elif pathname == '/waiting_password_page':
                import Pages.waiting_password_page as waiting_password_page
                return waiting_password_page.layout
            elif pathname == '/waiting_register_page':
                import Pages.waiting_register_page as waiting_register_page
                return waiting_register_page.layout
            elif pathname == '/admin_alarms_page' and current_user.is_authenticated:
                import Pages.admin_alarms_page as admin_alarms_page
                return admin_alarms_page.layout
            elif pathname == '/registrado_page' and current_user.is_authenticated:
                import Pages.registrado_page as registrado_page
                return registrado_page.layout
            elif pathname == '/sucessful_page' and current_user.is_authenticated:
                import Pages.sucessful_page as sucessful_page
                return sucessful_page.layout
            else:
                if current_user.is_authenticated:
                    import Pages.sucessful_page as sucessful_page
                    return sucessful_page.layout
                else:
                    import Pages.sign_in_page as sign_in_page
                    return sign_in_page.layout
        except Exception as e:
            LOGGER.error('Error found {} -- {} -- {}'.format(e, SysConfig.APP,
                                                             current_user.is_authenticated ))
            return 'Page not found 404'


    SysConfig.APP.run_server(debug=False, host='192.168.127.105')  # host=os.getenv("HOST", "10.8.0.32"))
