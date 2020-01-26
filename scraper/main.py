import schedule
import time
from scraper.zem_a_vek import ZemAVek


def zav_scrape():
    zav = ZemAVek()
    zav.get_new_articles()
    print(len(zav.data))
    zav.save_data_json(zav.data)


schedule.every(2).minutes.do(zav_scrape)

while True:
    schedule.run_pending()
    time.sleep(10)
