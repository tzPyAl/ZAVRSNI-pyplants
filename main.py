from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os
from libs.wt_forms import RegistrationForm, LoginForm

load_dotenv()
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db" # relative path
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    pots = db.relationship("Pots", backref="owner", lazy=True) # lazy - load dana in one go

    def __repr__(self): # how our Object is printed, when we printed it out
        return f"User('{self.id}', '{self.username}', '{self.email}')"
    
class Pots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    pot_image = db.Column(db.String(60), default="https://www.ikea.com/es/en/images/products/fejka-artificial-potted-plant-in-outdoor-monstera__0614197_pe686822_s5.jpg")
    data_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    status = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self): # how our Object is printed, when we printed it out
        return f"User('{self.name}', '{self.status}', '{self.data_created}')"
    
# clear db -> db.drop_all() db.create_all()

pots = [
    {
        'name': 'Potted plant 1',
        'status': 'ok',
        'img': "https://www.ikea.com/es/en/images/products/fejka-artificial-potted-plant-in-outdoor-monstera__0614197_pe686822_s5.jpg"
    },
    {
        'name': 'Potted plant 2',
        'status': 'no_water',
        'img': "https://www.ikea.com/es/en/images/products/fejka-artificial-potted-plant-with-pot-in-outdoor-succulent__0614211_pe686835_s5.jpg?f=s"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', pots=pots)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'PyPlant account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)