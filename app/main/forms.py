from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class CommentForm(FlaskForm):
    name = TextField('Your Name', validators=[Required()])
    email = TextField("Your Email", validators=[Required(), Length(1, 64), Email()])
    content = PageDownField("What's on your mind?", validators=[Required()])
    post_id = TextField('Post ID', validators=[Required()])
    submit = SubmitField("Publish")

    def clear(self):
        self.name.data = ''
        self.email.data = ''
        self.content.data = ''
        self.post_id.data = ''
