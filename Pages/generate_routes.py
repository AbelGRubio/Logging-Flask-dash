import os

if __name__ == '__main__':
    print(__file__)
    listing_file_dir = os.listdir(os.path.dirname(__file__))
    no_route_files = ['__init__.py', 'routes.py', os.path.basename(__file__), 'header.py', 'footer.py'
                      'routes_old.py']
    route_files = [file for file in listing_file_dir if file not in no_route_files]
    string_full_code = """
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_confirmed_used, is_know_used, confirm_user
from flask_login import login_required
from flask import request 


# @@@@@@@@@@@@@@@@@@@ ADDING ROUTES @@@@@@@@@@@@@
"""

    pages_with_login_required = ['successful_page', 'admin_alarms_page', 'registrado_page']

    fragment_with_login_required = """
@SysConfig.SERVER.route('/{}')
@login_required
def load_{}():
    import Pages.{} as {}
    SysConfig.APP.layout = {}.layout
    return SysConfig.APP.index() 

"""

    normal_fragment_code = """
@SysConfig.SERVER.route('/{}')
def load_{}():
    import Pages.{} as {}
    SysConfig.APP.layout = {}.layout
    return SysConfig.APP.index() 

"""

    pages_with_token = ['confirmed_email_page', 'new_password_page']

    fragment_with_token = """
@SysConfig.SERVER.route('/{}_<token>')
def load_{}(token):
    try:
        email_date = SysConfig.GEN_TOKENS.loads(token, salt='email-confirm', max_age=20)
        email = email_date.split('_')[0]
        confirm_user(email)
        if is_know_used(email):
            import Pages.{} as {} 
            SysConfig.APP.layout = {}.layout
            return SysConfig.APP.index()
        else:
            raise Exception
    except Exception:
        import Pages.expired_token_page as expired_token_page
        SysConfig.APP.layout = expired_token_page.layout
        return SysConfig.APP.index()

"""

    for route_file in route_files:
        r = route_file.split('.py')[0]

        print(r)

        if r in pages_with_login_required:
            string_code = fragment_with_login_required
        elif r in pages_with_token:
            string_code = fragment_with_token
        else:
            string_code = normal_fragment_code
        string_full_code += string_code.format(r, r, r, r, r)

    string_full_code += """
# @@@@@@@@@@@@@@@@@@@@@@ ADDING ROUTES TO SERVER @@@@@@@@@@@@@@@

"""

    # @@@@@@@@ including routes
    for route_file in route_files:
        r = route_file.split('.py')[0]
        if r in pages_with_token:
            add_route = """
SysConfig.SERVER.add_url_rule('/{}_<token>', '{}', view_func=load_{})

"""
        else:
            add_route = """
SysConfig.SERVER.add_url_rule('/{}', '{}', view_func=load_{})

"""
        string_full_code += add_route.format(r, r, r)

    with open('routes2.py', 'w') as f:
        f.write(string_full_code)

    f = 1

