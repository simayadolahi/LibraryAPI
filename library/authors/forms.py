from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AuthorForm(FlaskForm):
    author_id = IntegerField('Author ID') 
    name = StringField('Author Name', validators=[DataRequired()])
    submit = SubmitField('Add Author')