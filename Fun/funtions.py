import dash_bootstrap_components as dbc
from dash import html, dcc
from flask_login import current_user


def get_style():
    styleAdmin = {'visibility': 'hidden'}  # if current_user.is_authenticated else {'visibility': 'visible'}
    if str(current_user) != 'None':
        if current_user.is_authenticated:
            styleAdmin = {'visibility': 'visible'}
    return styleAdmin


def get_user_name():
    Username = ' '
    if str(current_user) != 'None':
        if current_user.is_authenticated:
            Username = current_user.username
    return Username


def get_row_identification():
    return dbc.Row(
        children=[
            dbc.Col(html.H2(get_user_name()),
                    style=get_style(),
                    ),
            dbc.Col(html.Button("Log out", id='logout-button', n_clicks=0,
                                style=get_style(),
                                ), className='text-align-right')
        ]
    )
