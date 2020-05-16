import time

import schedule

from news_scraper import update_time, today_time
from news_scraper.dennik_n import DennikN
from news_scraper.hlavne_spravy import HlavneSpravy
from news_scraper.mail_notifier import send_logs
from news_scraper.plus_7_dni import Plus7Dni
from news_scraper.sme import SME
from news_scraper.zem_a_vek import ZemAVek


def set_and_scrape() -> None:  # get sections from config
    update_time()
    print(f'Started at: {today_time}')
    DennikN.main()
    HlavneSpravy.main()
    Plus7Dni.main()
    SME.main()
    # ZemAVek.main()
    send_logs()


schedule.every().day.at('05:00').do(set_and_scrape)


def start():
    while True:
        schedule.run_pending()
        time.sleep(10)
