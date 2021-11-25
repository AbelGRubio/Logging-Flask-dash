import dash_html_components as html
import dash_core_components as dcc
import Configuration.ReaderConfSystem as SysConfig


def Header(app):
    # return html.Div([get_header(app), html.Br([]), get_menu()])
    return get_header(app)


def get_header(app):
    header = html.Div(
        [
            # html.Div(
            #     [
            #         html.Img(
            #             src=app.get_asset_url("imgs\\APL.png"),
            #             className="logo",
            #         ),
            #     ],
            #     className="row",
            # ),
            html.Div(
                [
                    # html.Img(
                    #     src=app.get_asset_url("imgs\\APL.png"),
                    #     # className="logo",
                    # ),
                    html.H2(SysConfig.NAME_SERVER),
                ],
            ),
            html.Br([]),
            get_menu(),
        ],
        className="margin-10px",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Sign in",
                href="/sign_in_page",
                className="tab first",
            ),
            dcc.Link(
                "Sign up",
                href="/sign_up_page",
                className="tab",
            ),
            dcc.Link(
                "Recover account",
                href="/recover_account_page",
                className="tab",
            ),
            dcc.Link(
                "New password",
                href="/new_password_page",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu

