import logging

from scraper.api import db
from scraper.api.db_utils import get_or_create

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
    @get_or_create
    def get_or_create_by_name(cls, name=name, site=site):
        author = Author(name=name, site=site)
        db.session.add(author)
        db.session.commit()
        return author.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    @classmethod
    @get_or_create
    def get_or_create_by_name(cls, name=name):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category.id


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('articles', lazy=True))
    title = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    photo = db.Column(db.String(150), nullable=False)
    time_published = db.Column(db.String(20), nullable=False)

    @classmethod
    def from_dict_data(cls, title, values):
        author_id = Author.get_or_create_by_name(name=values['author'], site=values['site'])
        category_id = Category.get_or_create_by_name(name=values['category'])

        article = cls(author_id=author_id, category_id=category_id, title=title, url=values['url'],
                      content=values['content'], description=values['description'], photo=values['photo'],
                      time_published=values['time_published'])

        tags_list = values['tags'].split(', ')
        if tags_list != ['']:
            Article.add_tags(article, tags_list)
        return article

    @classmethod
    def add_tags(cls, article, tags):
        for tag_str in tags:
            tag = Tag.get_or_create_by_name(tag_str)
            article.tags.append(tag)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    @classmethod
    def get_or_create_by_name(cls, name):
        tag = cls.query.filter_by(name=name).first()
        if tag is not None:
            return tag
        else:
            logging.info(f'tag {name} is not in DB')
            try:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
                return tag
            except Exception as e:
                logging.error(f'tag {name} can not be added to DB\n{e}')


# class ArticleAnalysis(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     semantic = db.Column()


# class WordsCount(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # words
#
#
# class SemanticWords(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # words
