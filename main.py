from flask import Flask, render_template, url_for, flash, redirect
from dotenv import load_dotenv
import os
from libs.wt_forms import RegistrationForm, LoginForm

load_dotenv()
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

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