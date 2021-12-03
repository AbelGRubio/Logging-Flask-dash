from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import Configuration.ReaderConfSystem as SysConfig
import smtplib
from Configuration import LOGGER
from Fun.email_content import CONFIRMATION_CONTENT, RECUPERATION_CONTENT


def create_email(is_confirmation: bool = True, url_token: str = '', user_name: str = ''):
    # Create message object instance
    msg = MIMEMultipart()

    # Setup the parameters of the message
    msg['From'] = SysConfig.MAIL_SENDER
    msg['To'] = ', '.join(SysConfig.MAIL_RECEIVER)
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
        print('Se ha enviado el mensaje')
    except Exception as e:
        LOGGER.debug("Error found: {}".format(e))
        return False

    return True


if __name__ == '__main__':
    mensaje = create_email(True, 'NADA')
    print(send_mail(mensaje))
    f = 1