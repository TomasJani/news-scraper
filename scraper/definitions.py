from pathlib import Path
from typing import NewType, Dict, Union, Any

ROOT_DIR = Path(__file__).parent.parent.as_posix()
SCRAPER_DIR = Path(__file__).parent.as_posix()
TIME_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = f'{TIME_FORMAT} %H:%M'
WEB_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
LOGGING_FORMAT = '%(asctime)s :: %(levelname)s = %(message)s'
DataDict = NewType('DataDict', Dict[str, Union[Dict[str, Union[str, Any]], Any]])
