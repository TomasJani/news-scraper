from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.as_posix()
SCRAPER_DIR = Path(__file__).parent.as_posix()
TIME_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = f'{TIME_FORMAT} %H:%M'
WEB_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
LOGGING_FORMAT = '%(asctime)s :: %(levelname)s = %(message)s'