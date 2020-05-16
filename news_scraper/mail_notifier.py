import codecs
import smtplib
import ssl
import logging

from news_scraper import config, today_time, SCRAPER_DIR


def get_log_content(path: str) -> str:
    try:
        with codecs.open(path, 'r', 'windows-1250') as f:
            return f.read()
    except Exception as e:
        logging.error(f'error with opening log file {path}\n{e}')
        return ""


def send_logs() -> None:
    context = ssl.create_default_context()
    n_c = config['MailNotifier']
    with smtplib.SMTP_SSL(n_c['SMTPServer'], n_c['Port'], context=context) as server:
        server.login(n_c['Sender'], n_c['Password'])
        message = 'Subject: {}\n\n{}'.format(f'Log {today_time}', get_log_content(f'{SCRAPER_DIR}/logs/{today_time}.log'))
        server.sendmail(n_c['Sender'], n_c['Receiver'], message.encode("windows-1250"))
