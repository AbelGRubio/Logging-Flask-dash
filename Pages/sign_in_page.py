import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import os
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig


def create_layout(app):
    web = html.Div(
        [Header(app),
         html.Div(
         [
            html.H1(["Sign in"], style={'color': 'blue'}),
            html.Div(dcc.Input(id='input-email', type='text', placeholder="Your email...")),
            html.Div(dcc.Input(id='input-password', type='text', placeholder="Your password...")),
            html.Button('Sign in', id='submit-val', n_clicks=0),
            html.H6(['New in {}? '.format(SysConfig.NAME_SERVER),
                     dcc.Link(
                         "Create an account",
                         href="/sign_up_page",
                     ), ]),
            html.H6([dcc.Link("Forgot the password?", href="/recover_account_page"), ])
         ],
         className="row text-align-center",
         ),
         ],
        className="page",
    )
    # add_callback(app)
    if not SysConfig.LOADED_TABLE:
        try:
            add_callback(app)
        except Exception as e:
            pass
        SysConfig.LOADED_TABLE = True
    return web


def add_callback(app):
    # @app.callback(
    #     Output("container", "children"),
    #     [Input("upload-data", "filename"), Input("upload-data", "contents")],
    # )
    # def update_output(uploaded_filenames, uploaded_file_contents):
    #     """Save uploaded files and regenerate the file list."""
    #     directory = 'checkFile'
    #     name = ''
    #     if uploaded_filenames is not None and uploaded_file_contents is not None:
    #         for name, data in zip(uploaded_filenames, uploaded_file_contents):
    #             print(os.path.join(directory, name))
    #             # save_file(name, data, directory=directory)
    #     try:
    #         print('Hola')
    #         # pathFile = os.path.join(MAIN_DIRECTORY, UPLOAD_DIRECTORY, 'checkFile',
    #         #                         name)
    #         # pathFile = 'checkFile\\2021_03_31_10_19_23_PredictionError_CH_2.bin'
    #         # pathFile = os.path.join(directory, name)
    #         # stats = getStatFile(pathFile)
    #     except Exception as e:
    #         stats = [0, 0, 0]
    #
    #     return html.Div([
    #         html.Table([
    #             html.Tr([html.Th('Hz file'),
    #                      html.Th('nPoints'),
    #                      html.Th('Percentage')]),
    #             html.Tr([html.Td(1000),
    #                      html.Td(6000),
    #                      html.Td(95)])],
    #             style={'width': '70%', 'margin-left': '15%', 'margin-right': '15%'},
    #         )
    #     ])
    #
    #     # files = uploaded_files(directory=directory)
    #     # if len(files) == 0:
    #     #     return [html.Li("No files yet!")]
    #     # else:
    #     #     return [html.Li(file_download_link(filename)) for filename in files]
    @app.callback(
        Output('container-button-basic', 'children'),
        Input('submit-val', 'n_clicks'),
        State('input-on-submit', 'value')
    )
    def update_output(n_clicks, value):
        return 'The input value was "{}" and the button has been clicked {} times'.format(
            value,
            n_clicks
        )