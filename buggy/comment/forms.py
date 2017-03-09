from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField

from wtforms.validators import DataRequired, Length, Email


class CreateCommentForm(Form):
    """Create comment form"""

    name = StringField('Name', validators=[Length(max=80)])
    email = StringField('Email', validators=[Length(max=80), Email()])
    text = TextAreaField(
        'Text',
        validators=[
            DataRequired(), Length(max=50000)
        ]
    )
    post_id = IntegerField(validators=[DataRequired()])
