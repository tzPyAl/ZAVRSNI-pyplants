from pyplant.db_models import User, Pots
from scripts.weather import _get_location_from_city
from scripts.endpoint_data import Endpoint
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
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
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")

class PlantDBForm(FlaskForm):
    db_id = IntegerField("Plants db ID", validators=[DataRequired()])
    submit = SubmitField("Connect")

    def validate_search(self, db_id):
        if not db_id:
            raise ValidationError(f'Enter the Plant db ID. Find it in Plants top navigation.')

class PlantCustomForm(FlaskForm):
    name = StringField("Enter plant name", validators=[DataRequired()])
    temp_min = IntegerField("Enter the minimal temperature", validators=[DataRequired()])
    temp_max = IntegerField("Enter the maximal temperature", validators=[DataRequired()])
    light_level = IntegerField("Enter light level from 1 to 3 (1 being highest)", validators=[DataRequired(), NumberRange(min=1, max=3)])
    water_level = IntegerField("Enter watering level from 1 to 5 (5 means do not water at all)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField("Connect")

    def validate_name(self, name):
        if not name:
            raise ValidationError(f'You must assign name to the plant')
    def validate_temp_min(self, temp_min):
        if not temp_min:
            raise ValidationError(f'Temperature must be a whole number')
    def validate_temp_max(self, temp_max):
        if not temp_max:
            raise ValidationError(f'Temperature must be a whole number')