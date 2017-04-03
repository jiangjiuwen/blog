from flask import render_template, redirect, url_for, abort, session
from . import dashboard
from .. import db
from .forms import PostForm, CategoryForm, TagForm
from ..models import Post, Tag, Category
from flask_login import current_user, login_required
import re
from config import Config, NavigationItemEnum


@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.DASHBOARD
    form = PostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    if form.validate_on_submit():
        entry = Post(alias=form.alias.data,
                     title=form.title.data,
                     content=form.content.data,
                     author_id=current_user.id)
        entry.category_id = form.category.data
        entry.post_type = form.post_type.data
        tags = re.split(';|；|,|，', form.tags.data)
        for tag in tags:
            tag = tag.strip()
            t = Tag.query.filter_by(name=tag).first()
            if not t:
                a = tag.split()
                formata = []
                for b in a:
                    b = b.strip()
                    b = b.replace('.', 'dot')
                    formata.append(b)
                alias = '-'.join(formata)
                new_tag = Tag(name=tag, alias=alias)
                entry.related_tags.append(new_tag)
            else:
                entry.related_tags.append(t)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('dashboard/index.html', form=form)

@dashboard.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.DASHBOARD    
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(alias=form.alias.data, name=form.name.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('dashboard.categories'))
    categories = Category.query.all()
    return render_template('dashboard/categories.html', form=form, categories=categories)

@dashboard.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    Config.CURRENT_NAVIGATION_ITEM = NavigationItemEnum.DASHBOARD
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(alias=form.alias.data, name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('dashboard.tags'))
    tags = Tag.query.all()
    return render_template('dashboard/tags.html', form=form, tags=tags)