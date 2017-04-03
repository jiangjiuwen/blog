from flask import render_template, redirect, url_for, abort
from . import main
from ..models import User, Post, Tag, Category
from config import Config, NavigationItemEnum
from .. import db
from flask import jsonify
import json

@main.route('/')
@main.route('/page/<int:page>')
def index(page=1):
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.POSTS
    p = Post.query.order_by(Post.timestamp.desc())
    posts = p.paginate(page, Config.POSTS_PER_PAGE, False)
    post_count = p.count()
    return render_template('index.html', posts=posts, post_count=post_count)

@main.route('/about')
def about():
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.ABOUT
    return render_template('about.html')

@main.route('/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/tag')
@main.route('/tag/<tag_alias>', methods=['GET'])
def tag(tag_alias=None):
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.ARCHIVE
    if tag_alias is None:
        tags = Tag.query.all()
        return render_template('tags.html', tags=tags)
    else:
        tag = Tag.query.filter_by(alias=tag_alias).first()
        return render_template('tag.html', tag=tag)

@main.route('/post/<alias>')
def detail(alias):
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.POSTS
    post = Post.query.filter_by(alias=alias).first()
    return render_template('detail.html', post=post)

@main.route('/category', methods=['GET', 'POST'])
@main.route('/category/<category_alias>')
@main.route('/category/<category_alias>?page=<page>')
def category(category_alias=None, page=1):
    if category_alias is None:
        categories = Category.query.all()
        ret = []
        for c in categories:
            ret.append([c.id, c.name, c.alias])
        return jsonify(categories=ret)
    else:
        Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.POSTS
        category = Category.query.filter_by(alias=category_alias).first()
        posts = Post.query.filter_by(category_id=category.id).order_by(Post.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
        return render_template('category.html', category=category, posts=posts)

@main.route('/current')
def current():
    return jsonify(current=Config.CURRENT_NAVIGATION_ITEM.value)
