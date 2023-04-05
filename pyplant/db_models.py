from pyplant import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_profile.png")
    pots = db.relationship("Pots", backref="owner", lazy=True) # lazy - load dana in one go

    def __repr__(self): # how our Object is printed, when we printed it out
        return f"User('{self.id}', '{self.username}', '{self.email}')"
    
class Pots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    pot_image = db.Column(db.String(20), default="default_pot.jpeg")
    data_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    status = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # add plant id

    def __repr__(self): # how our Object is printed, when we printed it out
        return f"User('{self.name}', '{self.status}', '{self.data_created}')"
    
# clear db -> db.drop_all() db.create_all()