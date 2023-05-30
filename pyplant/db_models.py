from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as TimedSerializer
from flask import current_app
from pyplant import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")
    # lazy - load dana in one go
    pots = db.relationship("Pots", backref="owner", lazy=True)

    def get_reset_token(self):
        s = TimedSerializer(current_app.config['SECRET_KEY'], 'confirmation')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = TimedSerializer(current_app.config['SECRET_KEY'], 'confirmation')
        try:
            user_id = s.loads(token, max_age=max_age)
        except:
            return None
        else:
            return User.query.get(user_id['user_id'])

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}'), '{self.pots}')"


class Pots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    pot_image = db.Column(db.String(20), default="default.jpeg")
    data_created = db.Column(
        db.DateTime(), nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, default=0)
    location = db.Column(db.String(20), nullable=False)
    lon = db.Column(db.String(20), nullable=False)
    lat = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))

    def __repr__(self):  # how our Object is printed, when we printed it out
        return f"Pots('{self.id}', '{self.name}', '{self.location}', '{self.pot_image}', '{self.status}', '{self.user_id}', '{self.plant_id}', '{self.data_created}')"


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    temp_min = db.Column(db.Integer, nullable=False)
    temp_max = db.Column(db.Integer, nullable=False)
    light_level = db.Column(db.Integer, nullable=False)
    water_level = db.Column(db.Integer, nullable=False)
    # lazy - load dana in one go
    pots_id = db.relationship("Pots", backref="plant", lazy=True)

    def __repr__(self):  # how our Object is printed, when we printed it out
        return f"Pots('{self.id}', '{self.name}', '{self.temp_min}', '{self.temp_max}', '{self.water_level}', '{self.light_level}', '{self.pots_id}')"

# clear db -> db.drop_all() db.create_all()
