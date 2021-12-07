from dash import html, dcc
from dash.dependencies import Input, Output, State
from Pages.header import Header
import Configuration.ReaderConfSystem as SysConfig
from Fun.send_email import create_email, send_mail
import dash_bootstrap_components as dbc


layout = html.Div(
    [Header(),
     html.Div(
         [
             dcc.Location(id='url_recover_account', refresh=True),
             html.H1(["Recover account"], style={'color': 'blue'}),
             html.Div(dcc.Input(id='input-email-recover', type='text', placeholder="Your email...")
                      , className='margin-10px'),
             html.Div(html.Button('Confirm', id='submit-recover', n_clicks=0)
                      , className='margin-10px'),
             html.Div(html.A('Back', href='sign_in_page', n_clicks=0)
                      , className='margin-10px'),
         ],
         className="row text-align-center margin-10px",
     ),
     ],
    className="page",
)


@SysConfig.APP.callback(
    Output(component_id='url_recover_account', component_property='pathname'),
    [Input(component_id='submit-recover', component_property='n_clicks')],
    State(component_id='input-email-recover', component_property='value')
)
def output_recover(n_clicks, value):
    if n_clicks > 0:
        print('Hace algo en recover page {}'.format(value))
        import datetime
        el_correo = '{}_{}'.format(value, str(datetime.datetime.now()))
        SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
        url_token = 'https://{}:{}/new_password_page_{}'.format(SysConfig.IP_HOST, SysConfig.PORT_HOST,
                                                                SysConfig.TOKEN)
        mensage = create_email(is_confirmation=False,
                               url_token=url_token,
                               user_name=value.split('@')[0])
        send_mail(mensage)
        # print(SysConfig.TOKEN)
        # return '/confirmed_email_page_{}'.format(SysConfig.TOKEN)
        return '/waiting_password_page'
    else:
        print('Pasa')
