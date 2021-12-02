from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from flask_login import current_user


layout = html.Div(
    [dcc.Location(id='url_admin_alarms', refresh=True),
     Header(SysConfig.APP),
     html.Div(
     [
         html.Br([]),
         html.Div([
         html.Table([
             html.Tr([html.Th('Hz file'),
                      html.Th('nPoints'),
                      html.Th('Percentage')]),
             html.Tr([html.Td(1000),
                      html.Td(6000),
                      html.Td(95)])],
             style={'width': '70%', 'margin-left': '15%', 'margin-right': '15%'},
         )
        ])
     ],
     className="row",
     style={'margin-left': '10px', 'margin-right': '10px'}
     ),
     ],
    className="page",
)


@SysConfig.APP.callback(
    Output("container", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
        """Save uploaded files and regenerate the file list."""
        directory = 'checkFile'
        name = ''
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                print(os.path.join(directory, name))
                # save_file(name, data, directory=directory)
        try:
            print('Hola')
            # pathFile = os.path.join(MAIN_DIRECTORY, UPLOAD_DIRECTORY, 'checkFile',
            #                         name)
            # pathFile = 'checkFile\\2021_03_31_10_19_23_PredictionError_CH_2.bin'
            # pathFile = os.path.join(directory, name)
            # stats = getStatFile(pathFile)
        except Exception as e:
            stats = [0, 0, 0]

        return

        # files = uploaded_files(directory=directory)
        # if len(files) == 0:
        #     return [html.Li("No files yet!")]
        # else:
        #     return [html.Li(file_download_link(filename)) for filename in files]


