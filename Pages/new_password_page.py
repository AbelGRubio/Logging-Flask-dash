from dash import html, dcc
from dash.dependencies import Input, Output, State
import os
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig


layout = html.Div(
    [Header(SysConfig.APP),
     html.Div(
     [
         dcc.Location(id='url_new_password', refresh=True),
         html.H1(["New password "], style={'color': 'blue'}),
         html.Div(dcc.Input(id='input-password', type='password', placeholder="Your new password...")),
         html.Div(dcc.Input(id='input-confirm-password', type='password', placeholder="Confirm your password...")),
         html.Button('Confirm', id='submit-val', n_clicks=0),
     ],
     className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)
