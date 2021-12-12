import dash
import Configuration.ReaderConfSystem as SysConfig
from flask import Flask
import dash_bootstrap_components as dbc


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
        meta_tags=[{"name": "viewport", "content": "width=device-width"}, ],
        server=SysConfig.SERVER)

    SysConfig.APP.config['suppress_callback_exceptions'] = True
    SysConfig.APP.title = 'ALERION'

    SysConfig.LOGIN_MANAGER.init_app(SysConfig.SERVER)

    import Pages.sign_in_page as sign_in_page
    SysConfig.APP.layout = sign_in_page.layout

    SysConfig.APP.run_server(debug=False, host=SysConfig.IP_HOST,
                             port=SysConfig.PORT_HOST)  # host='192.168.127.105')  # host=os.getenv("HOST", "10.8.0.32"))
