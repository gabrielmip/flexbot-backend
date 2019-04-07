from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField, SubmitField, TextAreaField)


class EditTrigger(FlaskForm):
    expression = StringField('Trigger', validators=[DataRequired()])
    answers = TextAreaField('Answers', validators=[DataRequired()])
    submit = SubmitField('Save')
