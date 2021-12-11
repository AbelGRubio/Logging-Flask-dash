
import Configuration.ReaderConfSystem as SysConfig
from Configuration.admin_users import is_confirmed_used, is_know_used, confirm_user
from flask_login import login_required
from flask import request
from flask_login import current_user
from Fun.send_email import SALT_MAIL_CONFIRM, SALT_MAIL_RECOVER, SALT_MAIL_KNOW_USER


# @@@@@@@@@@@@@@@@@@@ ADDING ROUTES @@@@@@@@@@@@@


@SysConfig.SERVER.route('/confirmed_email_page_<token>')
def load_confirmed_email_page(token):
    try:
        email_date = SysConfig.GEN_TOKENS.loads(token, salt=SALT_MAIL_CONFIRM, max_age=SysConfig.MAX_AGE_TOKENS)
        email = email_date.split('_')[0]
        confirm_user(email)
        if is_know_used(email):
            import Pages.confirmed_email_page as confirmed_email_page 
            SysConfig.APP.layout = confirmed_email_page.layout
            return SysConfig.APP.index()
        else:
            raise Exception
    except Exception:
        import Pages.expired_token_page as expired_token_page
        SysConfig.APP.layout = expired_token_page.layout
        return SysConfig.APP.index()


@SysConfig.SERVER.route('/confirmed_is_know_user_page_<token>')
def load_confirmed_is_know_user_page(token):
    try:
        email_date = SysConfig.GEN_TOKENS.loads(token, salt=SALT_MAIL_KNOW_USER, max_age=86400)
        email = email_date.split('_')[0]
        import Pages.confirmed_is_know_user_page as confirmed_is_know_user_page
        confirmed_is_know_user_page.USER_NAME = email
        confirmed_is_know_user_page.USER_MAIL = email
        SysConfig.APP.layout = confirmed_is_know_user_page.layout
        return SysConfig.APP.index()
    except Exception:
        import Pages.expired_token_page as expired_token_page
        SysConfig.APP.layout = expired_token_page.layout
        return SysConfig.APP.index()


@SysConfig.SERVER.route('/expired_token_page')
def load_expired_token_page():
    import Pages.expired_token_page as expired_token_page
    SysConfig.APP.layout = expired_token_page.layout
    return SysConfig.APP.index() 


@SysConfig.SERVER.route('/forbidden_page')
def load_forbidden_page():
    import Pages.forbidden_page as forbidden_page
    SysConfig.APP.layout = forbidden_page.layout
    return SysConfig.APP.index() 


@SysConfig.SERVER.route('/new_password_page_<token>')
def load_new_password_page(token):
    try:
        email_date = SysConfig.GEN_TOKENS.loads(token, salt=SALT_MAIL_RECOVER,
                                                max_age=SysConfig.MAX_AGE_TOKENS)
        email = email_date.split('_')[0]
        if is_know_used(email) and is_confirmed_used(email):
            import Pages.new_password_page as new_password_page 
            SysConfig.APP.layout = new_password_page.layout
            new_password_page.USER_EMAIL = email
            return SysConfig.APP.index()
        else:
            raise Exception
    except Exception:
        import Pages.expired_token_page as expired_token_page
        SysConfig.APP.layout = expired_token_page.layout
        return SysConfig.APP.index()


@SysConfig.SERVER.route('/recover_account_page')
def load_recover_account_page():
    import Pages.recover_account_page as recover_account_page
    SysConfig.APP.layout = recover_account_page.layout
    return SysConfig.APP.index() 


@SysConfig.SERVER.route('/')
@SysConfig.SERVER.route('/sign_in_page')
def load_sign_in_page():
    import Pages.sign_in_page as sign_in_page
    SysConfig.APP.layout = sign_in_page.layout
    return SysConfig.APP.index()


@SysConfig.SERVER.route('/beginning_page')
@SysConfig.SERVER.route('/admin_alarms_page', methods=['POST', 'GET'])
@SysConfig.SERVER.route('/registrado_page')
@SysConfig.SERVER.route('/welcome_page', methods=['POST', 'GET'])
@SysConfig.SERVER.route('/admin_users_page')
@login_required
def load_mask_page():
    print('Entra aqui con metodo request {}'.format(request.method))
    print('El usuario que ha entrado es {}'.format(current_user.username))
    import Pages.mask_page as mask_page
    SysConfig.APP.layout = mask_page.layout
    return SysConfig.APP.index()


@SysConfig.SERVER.route('/sign_up_page')
def load_sign_up_page():
    import Pages.sign_up_page as sign_up_page
    SysConfig.APP.layout = sign_up_page.layout
    return SysConfig.APP.index() 


@SysConfig.SERVER.route('/waiting_password_page')
def load_waiting_password_page():
    import Pages.waiting_password_page as waiting_password_page
    SysConfig.APP.layout = waiting_password_page.layout
    return SysConfig.APP.index() 


@SysConfig.SERVER.route('/waiting_register_page')
def load_waiting_register_page():
    import Pages.waiting_register_page as waiting_register_page
    SysConfig.APP.layout = waiting_register_page.layout
    return SysConfig.APP.index() 


# @@@@@@@@@@@@@@@@@@@@@@ ADDING ROUTES TO SERVER @@@@@@@@@@@@@@@


SysConfig.SERVER.add_url_rule('/confirmed_email_page_<token>', 'confirmed_email_page', view_func=load_confirmed_email_page)


SysConfig.SERVER.add_url_rule('/expired_token_page', 'expired_token_page', view_func=load_expired_token_page)


SysConfig.SERVER.add_url_rule('/forbidden_page', 'forbidden_page', view_func=load_forbidden_page)


SysConfig.SERVER.add_url_rule('/new_password_page_<token>', 'new_password_page', view_func=load_new_password_page)


SysConfig.SERVER.add_url_rule('/recover_account_page', 'recover_account_page', view_func=load_recover_account_page)


SysConfig.SERVER.add_url_rule('/sign_in_page', 'sign_in_page', view_func=load_sign_in_page)
SysConfig.SERVER.add_url_rule('/', '', view_func=load_sign_in_page)


SysConfig.SERVER.add_url_rule('/sign_up_page', 'sign_up_page', view_func=load_sign_up_page)


SysConfig.SERVER.add_url_rule('/waiting_password_page', 'waiting_password_page', view_func=load_waiting_password_page)


SysConfig.SERVER.add_url_rule('/waiting_register_page', 'waiting_register_page', view_func=load_waiting_register_page)
