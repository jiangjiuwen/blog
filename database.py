from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from datetime import datetime


app = Flask(__name__)
app.config.from_object(config['development'])
config['development'].init_app(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    related_posts = db.relationship('Post', backref='related_author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    alias = db.Column(db.String(64), unique=True)
    related_posts = db.relationship('Post', backref='related_category', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    alias = db.Column(db.String(64), unique=True)

post_tags = db.Table('post_tags',
            db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
            db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(128), unique=True)
    post_type = db.Column(db.Integer, default=0)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    related_tags = db.relationship('Tag', secondary = post_tags,
                   backref = db.backref('related_posts', lazy = 'dynamic'))

    def on_change_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        attrs = { '*': ['class'],
                  'a': ['href', 'rel'],
                  'img': ['src', 'alt'] }
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

db.event.listen(Post.content, 'set', Post.on_change_content)


if __name__ == '__main__':
    db.create_all()
