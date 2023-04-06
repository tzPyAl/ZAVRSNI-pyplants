from pyplant import app, db, bcrypt
from pyplant.wt_forms import RegistrationForm, LoginForm, UpdateProfileForm, PotForm
from pyplant.db_models import User, Pots
from scripts.weather import get_weather
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from json2html import *
import secrets
import os


@app.route("/")
@app.route("/home")
@login_required
def home():
    pots = Pots.query.filter_by(owner=current_user)
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


def save_img(form_image, save_dir, size_x, size_y):
    random_hex = secrets.token_hex(12)
    _, file_extension = os.path.splitext(form_image.filename) # using "_" to drop the file name
    img_fn = random_hex + file_extension
    img_path = os.path.join(app.root_path, save_dir, img_fn)
    output_size = (size_x, size_y) # simple resize image to 125x125 px
    temp_image = Image.open(form_image)
    temp_image.thumbnail(output_size)
    temp_image.save(img_path)
    # delete the old user image
    current_img_name, _ = os.path.splitext(current_user.image_file)
    if current_img_name != "default":
        old_img_path = os.path.join(app.root_path, save_dir, current_user.image_file)
        try:
            os.remove(old_img_path)
        except FileNotFoundError:
            pass # if i find to way to fetch the old pot image filename, i can delete it here
    return img_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.image.data:
            profile_img = save_img(form_image=form.image.data, save_dir="static/profile_img", size_x=125, size_y=125)
            current_user.image_file = profile_img
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


@app.route("/pots/new", methods=['GET', 'POST'])
@login_required
def new_pot():
    form = PotForm()
    if form.validate_on_submit():
        if form.image.data:
            pot_img = save_img(form_image=form.image.data, save_dir="static/pot_img", size_x=375, size_y=375)
            pot = Pots(name=form.name.data, location=form.location.data, lon=form.lon.data, lat=form.lat.data, pot_image=pot_img, owner=current_user)
        else:
            pot = Pots(name=form.name.data, location=form.location.data, lon=form.lon.data, lat=form.lat.data, owner=current_user)
        db.session.add(pot)
        db.session.commit()
        flash(f'New pot has been created. Found location {form.location.data}', 'success')
        return redirect(url_for("home"))
    return render_template("create_pot.html", title="New pot", form=form)

def save_to_html(name, content):
    html_file = os.path.join('pyplant/templates', name + '.html')
    print(html_file)
    with open(html_file, 'w+') as file:
        file.write(content)

@app.route("/pots/<int:pot_id>")
@login_required
def pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    _weather, _pollution = get_weather(lon=pot.lon, lat=pot.lat)
    # create a html from json, and save in html file
    weather = '{% block weather %}' + json2html.convert(json=_weather) + '{% endblock %}'
    pollution = '{% block pollution %}' + json2html.convert(json=_pollution) + '{% endblock %}'
    save_to_html(name=f'{weather=}'.split('=')[0], content=weather)
    save_to_html(name=f'{pollution=}'.split('=')[0], content=pollution)
    return render_template("pot.html", title=pot.name, pot=pot)


@app.route("/pots/<int:pot_id>/update", methods=['GET', 'POST'])
@login_required
def update_pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PotForm()
    if form.validate_on_submit():
        if form.image.data:
            pot.pot_image = save_img(form_image=form.image.data, save_dir="static/pot_img", size_x=375, size_y=375)
        else:
            pot.pot_image = pot.pot_image
        pot.name = form.name.data
        pot.location = form.location.data
        pot.lat = form.lat.data
        pot.lon = form.lon.data
        db.session.commit()
        flash('Pot has been updated.', 'success')
        return redirect(url_for("pot", pot_id=pot.id))
    elif request.method == "GET":
        form.name.data = pot.name
        form.location.data = pot.location
        form.image.data = pot.pot_image
    return render_template("create_pot.html", title="Update pot", form=form)


@app.route("/pots/<int:pot_id>/delete", methods=['POST'])
@login_required
def delete_pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    db.session.delete(pot)
    db.session.commit()
    flash('Pot has been deleted.', 'success')
    return redirect(url_for("home"))


@app.route("/profile/delete", methods=['POST'])
@login_required
def delete_profile():
    User.query.filter_by(id=current_user.id).delete()
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for("login"))