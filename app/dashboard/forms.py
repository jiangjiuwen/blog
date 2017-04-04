from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField 

class PostForm(FlaskForm):
    alias = TextField('Alias', validators=[Required()])
    title = TextField("Title", validators=[Required()])
    content = PageDownField("What's on your mind?", validators=[Required()])
    tags = TextField('Tags')
    category = SelectField('Category', coerce=int, choices=[('0', 'default')])
    submit = SubmitField("Publish")

class CategoryForm(FlaskForm):
    alias = TextField('Alias', validators=[Required()])
    name = TextField("Name", validators=[Required()])
    submit = SubmitField("Publish")

class TagForm(FlaskForm):
    alias = TextField('Alias', validators=[Required()])
    name = TextField("Name", validators=[Required()])
    submit = SubmitField("Publish")
