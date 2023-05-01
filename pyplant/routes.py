from pyplant import app, db, bcrypt, mail
from pyplant.wt_forms import RegistrationForm, LoginForm, UpdateProfileForm, PotForm, SearchForm, RequestResetForm, ResetPasswordForm, PlantDBForm, PlantCustomForm
from pyplant.db_models import User, Pots, Plant
from scripts.weather import get_weather
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image
from json2table import convert
import secrets
import os
import json
import glob


light_levels = [
    {
        'id': 1,
        'description': 'full sun (+21,500 lux /+2000 fc )'
    },
    {
        'id': 2,
        'description': 'strong light ( 21,500 to 3,200 lux/2000 to 300 fc)'
    },
    {
        'id': 3,
        'description': 'diffuse light ( Less than 5,300 lux / 500 fc)'
    }
]

water_levels = [
    {
        'id': 1,
        'description': 'keep moist between watering  &  must not dry between watering'
    },
    {
        'id': 2,
        'description': 'change water regularly in the cup  &  water when soil is half dry'
    },
    {
        'id': 3,
        'description': 'keep moist between watering  &  water when soil is half dry'
    },
    {
        'id': 4,
        'description': 'must dry between watering  &  water only when dry'
    },
    {
        'id': 5,
        'description': 'do not water'
    },
]


@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    pots = Pots.query.filter_by(owner=current_user).paginate(page=page, per_page=6)
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
    # get weather icon
    icon = _weather["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/wn/" + icon + "@2x.png"
    print(f"ICOn URl : {icon_url}")
    # create a html from json, and save in html file
    weather = '{% block weather %}<div class="styled-table">' + convert(_weather) + '</div>{% endblock %}'
    pollution = '{% block pollution %}<div class="styled-table">' + convert(_pollution) + '</div>{% endblock %}'
    save_to_html(name=f'{weather=}'.split('=')[0], content=weather)
    save_to_html(name=f'{pollution=}'.split('=')[0], content=pollution)
    plant = Plant.query.get(pot.plant_id)
    if plant:
        light_level = [x for x in light_levels if x['id'] == plant.light_level][0]['description']
        water_level = [x for x in water_levels if x['id'] == plant.water_level][0]['description']
        return render_template("pot.html", title=pot.name, pot=pot, plant=plant, light_level=light_level, water_level=water_level, icon_url=icon_url)
    return render_template("pot.html", title=pot.name, pot=pot, plant=plant, icon_url=icon_url)


def read_latest_scrapped_data():
    list_of_scrapped = glob.glob('./scrapped_data/*.json')
    latest_scrap = max(list_of_scrapped, key=os.path.getctime) 
    with open(latest_scrap, "r") as jsondata:
        data = json.load(jsondata)
    return data

@app.route("/pots/<int:pot_id>/connect_db", methods=['GET', 'POST'])
@login_required
def connect_plant_db(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PlantDBForm()
    if form.validate_on_submit():
        data = read_latest_scrapped_data()
        if form.db_id.data >= len(data):
            flash("ID doesn't exist in DB. Look for Plants in the top navigation.", 'danger')
            return redirect(url_for('connect_plant_db', pot_id=pot.id))
        else:
            name = data[form.db_id.data]['common_name']
            temp_min = data[form.db_id.data]['temperature_min._(c\u00b0)']
            temp_max = data[form.db_id.data]['temperature_max._(c\u00b0)']
            light_level = [x for x in light_levels if str(data[form.db_id.data]['light_ideal']) in x['description']][0]['id']
            water_level = [x for x in water_levels if str(data[form.db_id.data]['watering']) in x['description']][0]['id']
            plant = Plant(name=name, temp_min=temp_min, temp_max=temp_max, light_level=light_level, water_level=water_level, pots_id=[pot])
            db.session.add(plant)
            db.session.commit()
            flash('Pot has been updated.', 'success')
            return redirect(url_for("pot", pot_id=pot.id))
    return render_template("create_plant_db.html", title="Connect plant from db to pot", form=form)

@app.route("/pots/<int:pot_id>/edit_plant", methods=['GET', 'POST'])
@login_required
def edit_plant(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PlantCustomForm()
    if form.validate_on_submit():
        plant = Plant(name=form.name.data, temp_min=form.temp_min.data, temp_max=form.temp_max.data, light_level=form.light_level.data, water_level=form.water_level.data, pots_id=[pot])
        db.session.add(plant)
        db.session.commit()
        flash(f'Plant data has been updated', 'success')
        return redirect(url_for('pot', pot_id=pot.id))
    elif request.method == "GET":
        plant = Plant.query.get(pot.plant_id)
        if plant:
            form.name.data = plant.name
            form.temp_min.data = plant.temp_min
            form.temp_max.data = plant.temp_max
            form.light_level.data = plant.light_level
            form.water_level.data = plant.water_level
    return render_template("edit_plant.html", title="Manually edit connected plant", form=form)


@app.route("/pots/<int:pot_id>/update_plant", methods=['GET', 'POST'])
@login_required
def update_plant(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    plant = Plant.query.get(pot.plant_id)
    if pot.owner != current_user:
        abort(403)
    form = PlantCustomForm()
    if form.validate_on_submit():
        plant.name = form.name.data
        plant.temp_min = form.temp_min.data
        plant.temp_max = form.temp_max.data
        plant.light_level = form.light_level.data
        plant.water_level = form.water_level.data
        db.session.commit()
        flash(f'Plant data has been updated', 'success')
        return redirect(url_for('pot', pot_id=pot.id))
    elif request.method == "GET":
        form.name.data = plant.name
        form.temp_min.data = plant.temp_min
        form.temp_max.data = plant.temp_max
        form.light_level.data = plant.light_level
        form.water_level.data = plant.water_level
    return render_template("edit_plant.html", title="Manually edit connected plant", form=form)


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


@app.route("/plants", methods=['GET', 'POST'])
@login_required
def plants():
    show_plant = False
    form = SearchForm()
    if form.validate_on_submit():
        data = read_latest_scrapped_data()
        output_dict = [x for x in data if form.search.data.lower() in x["common_name"]]
        output_json = json.dumps(output_dict)
        if output_json == '[]':
            flash('No results. Try again', 'warning')
        else:
            json_object = json.loads(output_json)
            plant_img = json_object[0]['image_url']
            plant_table = '{% block plant %}' + convert(json_object[0]) + '{% endblock %}'
            save_to_html(name=f'{plant_table=}'.split('=')[0], content=plant_table)
            show_plant = True
            flash(f'Found {form.search.data}', 'info')
            return render_template("plants.html", title="Plant found", form=form, plant_img=plant_img, show_plant=show_plant)
    return render_template("plants.html", title="Plants database", form=form, show_plant=show_plant)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Pyplant - Password Request Reset', sender='noreply@pyplant.io', recipients=[user.email])
    msg.body = f'''Visit the following link to reset your password:
{url_for('reset_token', token=token, _external=True)}

This token will expire in 30 minutes.
'''
    mail.send(msg)

@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("If the email exist in the database, you will receive token.", "info")
            return redirect(url_for('login'))
        send_reset_email(user)
        flash("Email with instructions has been sent", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired token.", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password has been updated. You can now login!', 'success')
        return redirect(url_for('login'))
    return render_template("reset_password.html", title="Reset Password", form=form)