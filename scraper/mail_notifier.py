import codecs
import smtplib
import ssl
from scraper.bootstrap import logging, config, today_time


def get_log_content(path):
    try:
        with codecs.open(path, 'r', 'utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f'error with opening log file {path}\n{e}')
        return ""


context = ssl.create_default_context()
n_c = config['MailNotifier']

with smtplib.SMTP_SSL(n_c['SMTPServer'], n_c['Port'], context=context) as server:
    server.login(n_c['Sender'], n_c['Password'])
    message = 'Subject: {}\n\n{}'.format(f'Log {today_time}', get_log_content(f'logs/{today_time}.log'))
    server.sendmail(n_c['Sender'], n_c['Receiver'], message.encode("utf8"))