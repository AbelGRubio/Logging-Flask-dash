from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import Configuration.ReaderConfSystem as SysConfig
import pandas as pd
import random
from Configuration.admin_users import add_the_user, COLUMNS, USERS_NAME_TXT

DATA_FRAME = pd.read_csv(USERS_NAME_TXT, sep='\t')
del DATA_FRAME['Password']
COLUMNS_DATA_FRAME = [{'name': col, 'id': col} for col in COLUMNS[:-1]]
RECORDS_DATA_FRAME = DATA_FRAME.to_dict(orient='records')

COUNTER_ADD = 0
COUNTER_SAVE = 0
COUNTER_SEND_TOKEN = 0

layout = html.Div([
    dcc.Location(id='url_admin_users', refresh=True),

    dash_table.DataTable(
        id='adding-rows-table',
        columns=COLUMNS_DATA_FRAME,
        data=RECORDS_DATA_FRAME,
        editable=True,
        row_deletable=True,
    ),

    html.Button('Add user', id='editing-rows-button', n_clicks=COUNTER_ADD),
    html.Button('Save ', id='save-admin-user-button', n_clicks=COUNTER_SAVE, style={'margin-left': '10px'}),
    html.Button('Resend token', id='resend-token', n_clicks=COUNTER_SEND_TOKEN, style={'margin-left': '10px'}),
    html.H5('', id='status-admin-user'),
])


def reload_page():
    global DATA_FRAME, COLUMNS_DATA_FRAME, RECORDS_DATA_FRAME, layout
    DATA_FRAME = pd.read_csv(USERS_NAME_TXT, sep='\t')
    del DATA_FRAME['Password']
    COLUMNS_DATA_FRAME = [{'name': col, 'id': col} for col in DATA_FRAME.columns]
    RECORDS_DATA_FRAME = DATA_FRAME.to_dict(orient='records')
    layout = html.Div([
        dcc.Location(id='url_admin_users', refresh=True),

        dash_table.DataTable(
            id='adding-rows-table',
            columns=COLUMNS_DATA_FRAME,
            data=RECORDS_DATA_FRAME,
            editable=True,
            row_deletable=True,
        ),

        html.Button('Add user', id='editing-rows-button', n_clicks=COUNTER_ADD),
        html.Button('Save ', id='save-admin-user-button', n_clicks=COUNTER_SAVE, style={'margin-left': '10px'}),
        html.Button('Resend token', id='resend-token', n_clicks=COUNTER_SEND_TOKEN, style={'margin-left': '10px'}),
        html.H5('', id='status-admin-user'),
    ])


@SysConfig.APP.callback(
    [Output('adding-rows-table', 'data'),
     Output('status-admin-user', 'children')],
    [Input('editing-rows-button', 'n_clicks'),
     Input('save-admin-user-button', 'n_clicks')],
    [State('adding-rows-table', 'data'),
     State('adding-rows-table', 'columns')])
def add_row(n_clicks, n_clicks_save, rows, columns):
    global COUNTER_ADD, COUNTER_SAVE, COUNTER_SEND_TOKEN
    status_message = ''
    if n_clicks != COUNTER_ADD:
        random_id = int(random.random() * (2 ** 20 - 1))
        user_new_values = [random_id, 'no_user_name_yet', False, 'no_email_yet', True, 1]
        rows.append({c['id']: v for c, v in zip(columns, user_new_values)})
        status_message = 'New user added'
        if not add_the_user('no_user_name_yet', 'no_email_yet', random_id, 1):
            status_message = 'The user already exist'
        COUNTER_ADD += 1
    if n_clicks_save != COUNTER_SAVE:
        df_old = pd.read_csv(USERS_NAME_TXT, sep='\t').copy()
        df_old = df_old.set_index('id')
        df_new = pd.DataFrame.from_dict(rows)
        df_new = df_new.set_index('id')
        if len(df_new) < len(df_old):
            new_set = set(list(df_new.index))
            old_set = set(list(df_old.index))
            index_to_delete = list(old_set - new_set)
            df_old = df_old.drop(index_to_delete)
        else:
            df_old.update(df_new)
        df_old.to_csv(path_or_buf=USERS_NAME_TXT, sep='\t', index=True)
        status_message = 'User database updated'
        COUNTER_SEND_TOKEN += 1
    return rows, status_message



