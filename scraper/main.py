import time
import schedule

from scraper.bootstrap import update_time, logging, today_time
from scraper.dennik_n import DennikN
from scraper.hlavne_spravy import HlavneSpravy
from scraper.plus_7_dni import Plus7Dni
from scraper.sme import SME
from scraper.zem_a_vek import ZemAVek


def set_and_scrape():
    logging.basicConfig(filename=f'scraper/logs/{today_time}.log',
                        format='%(asctime)s :: %(filename)s :: %(levelname)s = %(message)s',
                        level=logging.INFO)
    update_time()
    DennikN.main()
    HlavneSpravy.main()
    Plus7Dni.main()
    SME.main()
    ZemAVek.main()


schedule.every().day.at('05:00').do(set_and_scrape)


def start():
    while True:
        schedule.run_pending()
        time.sleep(1)
