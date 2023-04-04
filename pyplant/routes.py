from pyplant import app, db, bcrypt
from pyplant.wt_forms import RegistrationForm, LoginForm, UpdateProfileForm
from pyplant.db_models import User, Pots
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os


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
@login_required
def home():
    return render_template('home.html', pots=pots)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'PyPlant account has been created. You can now login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

def save_profile_img(form_image):
    random_hex = secrets.token_hex(12)
    _, file_extension = os.path.splitext(form_image.filename) # using "_" to drop the file name
    img_fn = random_hex + file_extension
    img_path = os.path.join(app.root_path, "static/profile_img", img_fn)
    output_size = (125, 125) # simple resize image to 125x125 px
    temp_image = Image.open(form_image)
    temp_image.thumbnail(output_size)
    temp_image.save(img_path)
    # delete the old image
    current_img_name, _ = os.path.splitext(current_user.image_file)
    if current_img_name != "default_profile":
        old_img_path = os.path.join(app.root_path, "static/profile_img", current_user.image_file)
        os.remove(old_img_path)
    return img_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_profile_img(form.image.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated.', 'success')
        return redirect(url_for("profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_img/" + current_user.image_file)
    return render_template('profil.html', title='Profile', image_file=image_file, form=form)