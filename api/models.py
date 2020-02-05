from api import db
from datetime import datetime


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', backref='author', lazy=True)
    name = db.Column(db.String(50), nullable=False)
    site = db.Column(db.String(50), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    photo = db.Column(db.String(150), nullable=False)
    time_published = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


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
