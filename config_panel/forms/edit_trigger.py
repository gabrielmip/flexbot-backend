from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField, SubmitField, TextAreaField, HiddenField)


class EditTrigger(FlaskForm):
    expression = StringField('Trigger', validators=[DataRequired()])
    answers = TextAreaField('Answers', validators=[DataRequired()])
    chat_id = HiddenField('chat_id')
    submit = SubmitField('Save')
