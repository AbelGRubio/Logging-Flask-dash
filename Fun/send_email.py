from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import Configuration.ReaderConfSystem as SysConfig
import smtplib
from Configuration import LOGGER
from Fun.email_content import CONFIRMATION_CONTENT, RECUPERATION_CONTENT, IS_KNOW_CONTENT
import datetime


def send_mail_recover(mail, username):
    try:
        el_correo = '{}_{}'.format(mail, str(datetime.datetime.now()))
        SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
        url_token = 'http://{}:{}/new_password_page_{}'.format(SysConfig.IP_HOST, SysConfig.PORT_HOST,
                                                               SysConfig.TOKEN)
        mensage = create_email(is_confirmation=False,
                               url_token=url_token,
                               user_name=username,
                               email=mail)
        return send_mail(mensage)
    except Exception as e:
        return False


def send_mail_confirmation(mail, username):
    try:
        el_correo = '{}_{}'.format(mail, str(datetime.datetime.now()))
        SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
        url_token = 'http://{}:{}/confirmed_email_page_{}'.format(SysConfig.IP_HOST,
                                                                  SysConfig.PORT_HOST,
                                                                  SysConfig.TOKEN)
        mensage = create_email(is_confirmation=True,
                               url_token=url_token,
                               user_name=username,
                               email=mail)
        return send_mail(mensage)
    except Exception as e:
        return False


def send_mail_is_know_user(email, username):
    try:
        el_correo = '{}_{}'.format(email, str(datetime.datetime.now()))
        SysConfig.TOKEN = SysConfig.GEN_TOKENS.dumps(el_correo, salt='email-confirm')
        url_token = 'http://{}:{}/confirmed_is_know_user_page_{}'.format(SysConfig.IP_HOST,
                                                                         SysConfig.PORT_HOST,
                                                                         SysConfig.TOKEN)
        mensage = create_email(is_know_user=True,
                               url_token=url_token,
                               user_name=email)
        return send_mail(mensage)
    except Exception as e:
        return False


def create_email(is_confirmation: bool = True,
                 is_know_user: bool = False,
                 url_token: str = '',
                 user_name: str = '',
                 email: str = ''):
    # Create message object instance
    msg = MIMEMultipart()

    # Setup the parameters of the message
    msg['From'] = SysConfig.MAIL_SENDER
    if email == '':
        msg['To'] = ', '.join(SysConfig.MAIL_MANAGER)
    else:
        msg['To'] = email
    if is_know_user:
        msg['Subject'] = SysConfig.MAIL_SUBJECT_EMAIL_IS_KNOW_USER.format(user_name)
        message_body_html = IS_KNOW_CONTENT
    else:
        subject = SysConfig.MAIL_SUBJECT_EMAIL_CONFIRMATION if is_confirmation else SysConfig.MAIN_SUBJECT_EMAIL_RECUPERATION
        msg['Subject'] = subject.format(user_name)
        message_body_html = CONFIRMATION_CONTENT if is_confirmation else RECUPERATION_CONTENT
    message_body_html = message_body_html.format(url_token)

    try:
        msg.attach(MIMEText(message_body_html, 'html'))
    except Exception as e:
        LOGGER.debug("Error found: {}".format(e))
        print('Error en adjuntar')

    # Add logo
    try:
        msgImage = MIMEImage(SysConfig.IMG_LOGO)
        msgImage.add_header('Content-ID', '<image1>')
        msgImage.add_header('Content-Disposition', 'inline; filename={}'.format(SysConfig.IMG_LOGO_PATH))
        msg.attach(msgImage)
    except Exception as e:
        LOGGER.debug("Error found: {}".format(e))

    return msg


def attach_document(msg):
    # ATTACH .TXT
    try:
        attached_file = open('alarmas.txt', 'rb')  # Creamos un objeto MIME base
        attached_MIME = MIMEBase('application', 'octet-stream')
        attached_MIME.set_payload((attached_file).read())  # Load file to attach
        encoders.encode_base64(attached_MIME)  # Object codification in BASE64
        attached_MIME.add_header('Content-Disposition', "attachment; filename= Alarmas.txt")  # Add object header
        msg.attach(attached_MIME)  # Attach object to the message
    except Exception as e:
        LOGGER.debug("Error found: {}".format(e))

    return msg


def send_mail(email_msg: MIMEMultipart):

    # SMTP connection, login and message delivery
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(email_msg['From'], SysConfig.MAIL_PASSWORD)
        smtp.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        smtp.quit()
        LOGGER.debug("Mail sent ")
        print('Se ha enviado el mensaje a {}'.format(email_msg['To']))
    except Exception as e:
        LOGGER.debug("Error found: {}".format(e))
        return False

    return True


if __name__ == '__main__':
    mensaje = create_email(True, 'NADA')
    print(send_mail(mensaje))
    f = 1