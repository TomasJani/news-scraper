import logging

from api import db
from datetime import datetime

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
                )


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', backref='author', lazy=True)
    name = db.Column(db.String(50), nullable=False)
    site = db.Column(db.String(50), nullable=False)

    @classmethod
    def get_or_create_by_name(cls, name, site):  # refactor with args and kwargs
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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    @classmethod
    def get_or_create_by_name(cls, name):  # refactor
        try:
            return cls.query.filter_by(name=name).first().id
        except Exception as e:  # ONLY IF NONE FOUND
            logging.info(f'name {name} is not in DB\n{e}')
            try:
                category = Category(name=name)
                db.session.add(category)
                db.session.commit()
                return category.id
            except Exception as e:
                logging.error(f'category {name} can not be added to DB\n{e}')


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('articles', lazy=True))
    title = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    photo = db.Column(db.String(150), nullable=False)
    time_published = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def from_dict_data(cls, title, values):
        author_id = Author.get_or_create_by_name(values['author'], values['site'])
        category_id = Category.get_or_create_by_name(values['category'])
        return cls(author_id=author_id, category_id=category_id, site=values['site'], title=title, url=values['url'],
                   description=values['description'], photo=values['photo'])


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
