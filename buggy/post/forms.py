from flask_wtf import Form
from wtforms import StringField, TextAreaField

from wtforms.validators import DataRequired, Length


class CreatePostForm(Form):
    """Create post form"""

    title = StringField('Title', validators=[DataRequired(), Length(max=250)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=50000)])
    tags = StringField('Tags', validators=[Length(max=1000)])
