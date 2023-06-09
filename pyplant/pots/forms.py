from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from pyplant.db_models import Pots
from scripts.weather import _get_location_from_city
from scripts.endpoint_data import Endpoint


class PotForm(FlaskForm):
    name = StringField("Pot name",
                       validators=[DataRequired()])
    image = FileField("Upload pot picture",
                      validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
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
                raise ValidationError(
                    'That name is taken. Please choose a different one.')

    def validate_location(self, location):
        global returned_location
        returned_location = _get_location_from_city(location.data)
        if not returned_location or location.data == "Unknown":
            raise ValidationError(
                f'Not found anything. Try again or leave empty to use proposed city.')
        else:
            location.data = returned_location[0] + "," + returned_location[1]

    def validate_lat(self, lat):
        global returned_location
        lat.data = returned_location[2]

    def validate_lon(self, lon):
        global returned_location
        lon.data = returned_location[3]
