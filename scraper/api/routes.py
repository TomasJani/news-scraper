import logging
import sqlite3

from sqlalchemy import exc

from scraper.api import app, db
from scraper.api.db_utils import load_yesterday_data, save_unsaved_db_data
from scraper.api.models import Article


@app.route('/')
@app.route('/home')
def home_page():
    # Create Home page template
    return '<h1>Hello You</h1>'


# Route for searching
# Save searches & searches only for registered users

class AddToDb:  # new file
    def __init__(self):
        self.yesterday_data = load_yesterday_data()

    def add_yesterday_data(self):
        unsaved_data = {}
        for title, values in self.yesterday_data.items():
            try:
                db.session.add(Article.from_dict_data(title, values))
                db.session.commit()  # how often to commit?
            except exc.IntegrityError:
                unsaved_data[title] = values
                db.session.rollback()
                logging.error(f'title {title} can not be added to DB')
        save_unsaved_db_data(unsaved_data)

    def add_words_analysis(self):
        # search with regex
        pass

    def add_semantic_analysis(self):
        # Google API
        pass
