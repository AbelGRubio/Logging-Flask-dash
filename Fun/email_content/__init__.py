import os

folder_path = os.path.dirname(__file__)

open_html = open(os.path.join(folder_path, 'confirmation_mail.html'), 'r')
CONFIRMATION_CONTENT = ''.join(open_html.readlines())
open_html.close()

open_html = open(os.path.join(folder_path, 'recuperation_mail.html'), 'r')
RECUPERATION_CONTENT = ''.join(open_html.readlines())
open_html.close()


open_html = open(os.path.join(folder_path, 'is_know_mail.html'), 'r')
IS_KNOW_CONTENT = ''.join(open_html.readlines())
open_html.close()

