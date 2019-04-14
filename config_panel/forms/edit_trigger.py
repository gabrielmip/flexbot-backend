from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField, SubmitField, TextAreaField, HiddenField)


class EditTrigger(FlaskForm):
    expression = StringField(label='When someone says...', validators=[DataRequired()])
    answers = TextAreaField(label='The bot says...', validators=[DataRequired()])
    chat_id = HiddenField(label='chat_id')
    submit = SubmitField(label='Save')
