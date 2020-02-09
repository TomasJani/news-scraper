import logging

from api import db
from datetime import datetime


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', backref='author', lazy=True)
    name = db.Column(db.String(50), nullable=False)
    site = db.Column(db.String(50), nullable=False)

    @classmethod
    def get_or_create_by_name(cls, name, site):
        try:
            return cls.query.filter_by(name=name, site=site).first().id
        except Exception as e:  # ONLY IF NONE FOUND
            logging.info(f'name {name} is not in DB\n{e}')
            try:
                author = Author(name=name, site=site)
                db.session.add(author)
                db.session.commit()
                return author.id
            except Exception as e:
                logging.error(f'author {name} of site {site} can not be added to DB\n{e}')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    photo = db.Column(db.String(150), nullable=False)
    time_published = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def from_dict_data(cls, title, values):
        author_id = Author.get_or_create_by_name(values['author'], values['site'])
        return cls(author_id=author_id, title=title, url=values['url'], description=values['description'],
                   photo=values['photo'])


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)


class ArticleAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semantic = db.Column()


class WordsCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # words


class SemanticWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # words
