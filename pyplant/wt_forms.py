from pyplant.db_models import User, Pots
from scripts.weather import _get_location_from_city
from scripts.endpoint_data import Endpoint
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
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
            raise ValidationError('That email is taken. Please choose a different one.') 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

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
    image = FileField("Update profile picture", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')   
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
            
            
class PotForm(FlaskForm):
    name = StringField("Pot name", validators=[DataRequired()])
    image = FileField("Upload pot picture", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    endpoint = Endpoint()
    location = StringField("City", default=endpoint.city)
    lon = StringField("lon", default=endpoint.lon)
    lat = StringField("lat", default=endpoint.lat)
    submit = SubmitField("Create")
    returned_location = ""

    def validate_pot_name(self, pot_name):
        if pot_name.data != current_user.username:
            name = Pots.query.filter_by(pot_name=pot_name.data).first()
            if name:
                raise ValidationError('That name is taken. Please choose a different one.')
    def validate_location(self, location):
        global returned_location
        returned_location = _get_location_from_city(location.data)
        if not returned_location or location.data == "Unknown":
            raise ValidationError(f'Not found anything. Try again or leave empty to use proposed city.')
        else:
            location.data = returned_location[0] + "," + returned_location[1]
    def validate_lat(self, lat):
        global returned_location
        lat.data = returned_location[2]
    def validate_lon(self, lon):
        global returned_location
        lon.data = returned_location[3]

class SearchForm(FlaskForm):
    search = StringField("Enter plant name. Search by keyword", validators=[DataRequired()])
    submit = SubmitField("Search")

    def validate_search(self, search):
        if not search:
            raise ValidationError(f'Enter the desired keyword.')