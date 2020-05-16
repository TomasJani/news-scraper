import logging
from datetime import datetime, timedelta
from news_scraper.definitions import TIME_FORMAT, SCRAPER_DIR, LOGGING_FORMAT


class ProjectVariables:
    today_time = datetime.utcnow().strftime(TIME_FORMAT)
    yesterday_time = (datetime.utcnow() - timedelta(days=1)).strftime(TIME_FORMAT)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=f'{SCRAPER_DIR}/logs/{today_time}.log', mode='w',
                                  encoding='windows-1250')
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    root_logger.addHandler(handler)

    @classmethod
    def update_time(cls):
        cls.today_time = datetime.now().strftime(TIME_FORMAT)
        cls.yesterday_time = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
        cls.handler.close()
        cls.handler.baseFilename = f'{SCRAPER_DIR}/logs/{cls.today_time}.log'
        cls.root_logger.addHandler(cls.handler)
