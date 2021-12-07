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
from Configuration.admin_users import is_confirmed_used, is_know_used, confirm_user


if __name__ == '__main__':

    # Setup the Flask server
    SysConfig.SERVER = Flask(__name__)

    SysConfig.SERVER.config.update(
        SECRET_KEY=SysConfig.SECRET,
    )

    from Pages.routes import *

    SysConfig.APP = dash.Dash(
        name=__name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{"name": "viewport", "content": "width=device-width"},],
        server=SysConfig.SERVER)

    SysConfig.APP.config['suppress_callback_exceptions'] = True
    SysConfig.APP.title = 'ALERION'

    SysConfig.LOGIN_MANAGER.init_app(SysConfig.SERVER)
    SysConfig.LOGIN_MANAGER.login_view = '/sign_in_page'

    import Pages.sign_in_page as sign_in_page
    SysConfig.APP.layout = sign_in_page.layout

    # SysConfig.SERVER.add_url_rule('/successful_page', 'successful_page', view_func=load_successful_page)
    # Update page
    # @SysConfig.APP.callback(Output("page-content", "children"), [Input("url", "pathname")])
    # def display_page(pathname):
    #     print(pathname)
    #     try:
    #         if pathname == '/sign_up_page':
    #             import Pages.sign_up_page as sign_up_page
    #             return sign_up_page.layout
    #         elif pathname == '/sign_in_page':
    #             import Pages.sign_in_page as sign_in_page
    #             return sign_in_page.layout
    #         elif pathname == '/forbidden_page':
    #             import Pages.forbidden_page as forbidden_page
    #             return forbidden_page.layout
    #         elif pathname == '/recover_account_page':
    #             import Pages.recover_account_page as recover_account_page
    #             return recover_account_page.layout
    #         elif pathname == '/waiting_password_page':
    #             import Pages.waiting_password_page as waiting_password_page
    #             return waiting_password_page.layout
    #         elif pathname == '/waiting_register_page':
    #             import Pages.waiting_register_page as waiting_register_page
    #             return waiting_register_page.layout
    #         elif '/new_password_page_' in pathname:
    #             pathname = pathname.replace('/new_password_page_', '')
    #             try:
    #                 email_date = SysConfig.GEN_TOKENS.loads(pathname, salt='email-confirm', max_age=20)
    #                 email = email_date.split('_')[0]
    #                 print('El usuario {} del token esta confirmado? {}'.format(email, is_confirmed_used(email)))
    #                 if is_know_used(email) and is_confirmed_used(email):
    #                     import Pages.new_password_page as new_password_page
    #                     return new_password_page.layout
    #                 else:
    #                     raise Exception
    #             except Exception:
    #                 import Pages.forbidden_page as forbidden_page
    #                 return forbidden_page.layout
    #         elif '/confirmed_email_page_' in pathname:
    #             pathname = pathname.replace('/confirmed_email_page_', '')
    #             try:
    #                 email_date = SysConfig.GEN_TOKENS.loads(pathname, salt='email-confirm', max_age=20)
    #                 email = email_date.split('_')[0]
    #                 print('El usuario {} del token esta confirmado? {}'.format(email, is_confirmed_used(email)))
    #                 confirm_user(email)
    #                 if is_know_used(email):
    #                     print('entraa para confirmar')
    #                     import Pages.confirmed_email_page as confirmed_email_page
    #                     return confirmed_email_page.layout
    #                 else:
    #                     print('HA entrado en la exception ')
    #                     raise Exception
    #             except Exception:
    #                 import Pages.expired_token_page as expired_token_page
    #                 return expired_token_page.layout
    #         elif pathname == '/admin_alarms_page' and current_user.is_authenticated:
    #             import Pages.admin_alarms_page as admin_alarms_page
    #             return admin_alarms_page.layout
    #         elif pathname == '/registrado_page' and current_user.is_authenticated:
    #             import Pages.registrado_page as registrado_page
    #             return registrado_page.layout
    #         elif pathname == '/sucessful_page' and current_user.is_authenticated:
    #             import Pages.sucessful_page as sucessful_page
    #             return sucessful_page.layout
    #         else:
    #             if current_user.is_authenticated:
    #                 import Pages.sucessful_page as sucessful_page
    #                 return sucessful_page.layout
    #             else:
    #                 import Pages.sign_in_page as sign_in_page
    #                 return sign_in_page.layout
    #     except Exception as e:
    #         LOGGER.error('Error found {} -- {} -- {}'.format(e, SysConfig.APP,
    #                                                          current_user.is_authenticated))
    #         return 'Page not found 404'
    # #

    SysConfig.APP.run_server(debug=False, host=SysConfig.IP_HOST,
                             port=SysConfig.PORT_HOST)  # host='192.168.127.105')  # host=os.getenv("HOST", "10.8.0.32"))
