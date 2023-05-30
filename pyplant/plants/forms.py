from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange


class SearchForm(FlaskForm):
    search = StringField(
        "Enter plant name. Search by keyword", validators=[DataRequired()])
    submit = SubmitField("Search")

    def validate_search(self, search):
        if not search:
            raise ValidationError(f'Enter the desired keyword.')


class PlantDBForm(FlaskForm):
    db_id = IntegerField("Plants db ID", validators=[DataRequired()])
    submit = SubmitField("Connect")

    def validate_search(self, db_id):
        if not db_id:
            raise ValidationError(
                f'Enter the Plant db ID. Find it in Plants top navigation.')


class PlantCustomForm(FlaskForm):
    name = StringField("Enter plant name", validators=[DataRequired()])
    temp_min = IntegerField(
        "Enter the minimal temperature", validators=[DataRequired()])
    temp_max = IntegerField(
        "Enter the maximal temperature", validators=[DataRequired()])
    light_level = IntegerField("Enter light level from 1 to 3 (1 being highest)", validators=[
                               DataRequired(), NumberRange(min=1, max=3)])
    water_level = IntegerField("Enter watering level from 1 to 5 (5 means do not water at all)", validators=[
                               DataRequired(), NumberRange(min=1, max=5)])
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
