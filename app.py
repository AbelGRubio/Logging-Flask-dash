import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import Configuration.ReaderConfSystem as SysConfig
from Configuration import LOGGER
from flask import Flask, request, redirect
from flask_login import current_user, logout_user
import os


if __name__ == '__main__':

    # Setup the Flask server
    server = Flask(__name__)

    server.config.update(
        SECRET_KEY=os.urandom(12),
    )

    app = dash.Dash(
        name=__name__,
        meta_tags=[{"name": "viewport", "content": "width=device-width"},],
        server=server)
    # server = app.server
    app.config['suppress_callback_exceptions'] = True
    app.title = 'ALERION'

    # Describe the layout/ UI of the app
    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
    )

    SysConfig.APP = app
    SysConfig.LOGIN_MANAGER.init_app(server)
    SysConfig.LOGIN_MANAGER.login_view = '/sign_in_page'

    # Update page
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        try:
            if pathname == '/recover_account_page':
                import Pages.recover_account_page as recover_account_page
                return recover_account_page.create_layout(SysConfig.APP)
            elif pathname == '/sign_up_page':
                import Pages.sign_up_page as sign_up_page
                return sign_up_page.create_layout(SysConfig.APP)
            elif pathname == '/sign_in_page':
                import Pages.sign_in_page as sign_in_page
                return sign_in_page.create_layout(SysConfig.APP)
            elif pathname == '/admin_alarms_page' and current_user.is_authenticated:
                import Pages.admin_alarms_page as admin_alarms_page
                return admin_alarms_page.create_layout(SysConfig.APP)
            elif pathname == '/registrado_page' and current_user.is_authenticated:
                import Pages.registrado_page as registrado_page
                return registrado_page.create_layout(SysConfig.APP)
            else:
                if current_user.is_authenticated:
                    import Pages.admin_alarms_page as admin_alarms_page
                    return admin_alarms_page.create_layout(SysConfig.APP)
                else:
                    import Pages.sign_in_page as sign_in_page
                    return sign_in_page.create_layout(SysConfig.APP)
        except Exception as e:
            LOGGER.error('Error found {} -- {} -- {}'.format(e, SysConfig.APP,
                                                           current_user.is_authenticated ))
            return 'Page not found 404'


    app.run_server(debug=True, host='192.168.127.105')  # host=os.getenv("HOST", "10.8.0.32"))
