from api import app


@app.route('/')
@app.route('/home')
def home_page():
    # Create Home page template
    return '<h1>Hello You</h1>'


class AddToDb:
    def __init__(self):
        self.today_data = ""

    @app.route('/add', methods=['Post'])
    def add_today_data(self):
        # load files - use for all functions once
        # send to DB
        pass

    @app.route('/add/words', methods=['Post'])
    def add_words_analysis(self):
        # search with regex
        pass

    @app.route('/add/semantic', methods=['Post'])
    def add_semantic_analysis(self):
        # Google API
        pass
