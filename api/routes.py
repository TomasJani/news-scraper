import logging

from api import app, db
from api.db_utils import load_yesterday_data
from api.models import Article


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
        for title, values in self.yesterday_data.items():
            try:
                db.session.add(Article.from_dict_data(title, values))
                db.session.commit()  # how often to commit?
            except Exception as e:
                db.session.rollback()
                logging.error(f'title {title} can not be added to DB\n{e}')

    def add_words_analysis(self):
        # search with regex
        pass

    def add_semantic_analysis(self):
        # Google API
        pass
