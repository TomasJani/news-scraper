import schedule
import time

from scraper.dennik_n import DennikN
from scraper.hlavne_spravy import HlavneSpravy
from scraper.mail_notifier import send_logs
from scraper.plus_7_dni import Plus7Dni
from scraper.sme import SME
from scraper.zem_a_vek import ZemAVek


def zav_scrape():
    zav = ZemAVek()
    zav.get_new_articles()
    print(len(zav.data))
    zav.save_data_json(zav.data, site='zem_a_vek')


def hs_scraper():
    hs = HlavneSpravy()
    hs.get_new_articles()
    print(len(hs.data))
    hs.save_data_json(hs.data, site='hlavne_spravy')


def p7d_scraper():
    p7d = Plus7Dni()
    p7d.get_new_articles()
    print(len(p7d.data))
    p7d.save_data_json(p7d.data, site='plus_7_dni')


def dn_scraper():
    dn = DennikN()
    dn.get_new_articles()
    print(len(dn.data))
    dn.save_data_json(dn.data, site='dennik_n')


def sme_scraper():
    sme = SME()
    sme.get_new_articles()
    print(len(sme.data))
    sme.save_data_json(sme.data, site='sme')


def scrape_all():
    zav_scrape()
    p7d_scraper()
    dn_scraper()
    hs_scraper()
    sme_scraper()
    send_logs()


schedule.every().day.at('05:00').do(scrape_all)

while True:
    schedule.run_pending()
    time.sleep(1)
