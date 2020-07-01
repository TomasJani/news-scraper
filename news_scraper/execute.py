import time

import schedule

from news_scraper import ProjectVariables
from news_scraper.scrapers.dennik_n import DennikN
from news_scraper.scrapers.hlavne_spravy import HlavneSpravy
from news_scraper.mail_notifier import send_logs
from news_scraper.scrapers.plus_7_dni import Plus7Dni
from news_scraper.scraper_utils import save_data_json
from news_scraper.scrapers.sme import SME
from news_scraper.scrapers.zem_a_vek import ZemAVek


def set_and_scrape() -> None:
    ProjectVariables.set_logger()
    ProjectVariables.update_time()
    print(f'Started at: {ProjectVariables.today_time}')

    data = list()
    data.extend(DennikN.main())
    data.extend(HlavneSpravy.main())
    data.extend(Plus7Dni.main())
    data.extend(SME.main())
    data.extend(ZemAVek.main())
    save_data_json(data)
    send_logs()


schedule.every().day.at('05:00').do(set_and_scrape)


def start():
    while True:
        schedule.run_pending()
        time.sleep(10)
