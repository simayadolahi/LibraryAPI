from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    book_id = IntegerField('Book ID')
    title = StringField('Book Title', validators=[DataRequired()])
    author_id = IntegerField('Author ID', validators=[DataRequired()])
    submit = SubmitField('Add Book')