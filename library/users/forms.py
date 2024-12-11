from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from library.models import UserModel
from flask_login import current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')



    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = UserModel.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class UserForm(FlaskForm):
    name = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    borrowing_date = DateTimeField('Borrowing Date (YYYY-MM-DD HH:MM:SS)', validators=[Optional()])
    book_id = IntegerField('Book ID', validators=[Optional()])
    submit = SubmitField('Add User')
