from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from pyplant.db_models import User
import email_validator


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[
                                         DataRequired(),
                                         EqualTo("password")
                                     ])
    submit = SubmitField("Sign up")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    image = FileField("Update profile picture", validators=[
                      FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    submit = SubmitField("Send reset code to email")

    # handling verification in routes. don't want to show if the email is not in db
    # def validate_email(self, email):
    #     email = User.query.filter_by(email=email.data).first()
    #     if email is None:
    #         raise ValidationError('Email is not in database')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
