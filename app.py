import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import Configuration.ReaderConfSystem as SysConfig


if __name__ == '__main__':

    app = dash.Dash(
        __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    )
    server = app.server
    app.config['suppress_callback_exceptions'] = True
    app.title = 'ALERION'

    # Describe the layout/ UI of the app
    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
    )

    SysConfig.APP = app

    # Update page
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == '/sign_up_page':
            import Pages.sign_up_page as sign_up_page
            return sign_up_page.create_layout(SysConfig.APP)
        elif pathname == '/sign_in_page':
            import Pages.sign_in_page as sign_in_page
            return sign_in_page.create_layout(SysConfig.APP)
        elif pathname == '/recover_account_page':
            import Pages.recover_account_page as recover_account_page
            return recover_account_page.create_layout(SysConfig.APP)
        elif pathname == '/admin_alarms_page':
            import Pages.admin_alarms_page as admin_alarms_page
            return admin_alarms_page.create_layout(SysConfig.APP)
        elif pathname == '/new_password_page':
            import Pages.new_password_page as new_password_page
            return new_password_page.create_layout(SysConfig.APP)
        else:
            import Pages.sign_in_page as sign_in_page
            return sign_in_page.create_layout(SysConfig.APP)

    app.run_server(debug=True, )  # host=os.getenv("HOST", "10.8.0.32"))