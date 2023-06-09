from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from json2table import convert
from pyplant.main.utils import save_img, save_to_html
from pyplant.plants.forms import PlantDBForm, PlantCustomForm
from pyplant.pots.forms import PotForm
from pyplant.pots.utils import read_latest_scrapped_data, get_plant_status
from pyplant.pots.data import light_levels, water_levels, plant_status
from scripts.weather import get_weather
from pyplant import db
from pyplant.db_models import Pots, Plant


pots = Blueprint("pots", __name__)


@pots.route("/pots/new", methods=['GET', 'POST'])
@login_required
def new_pot():
    form = PotForm()
    if form.validate_on_submit():
        if form.image.data:
            pot_img = save_img(form_image=form.image.data,
                               save_dir="static/pot_img",
                               size_x=375, size_y=375)
            pot = Pots(name=form.name.data,
                       location=form.location.data,
                       lon=form.lon.data,
                       lat=form.lat.data,
                       pot_image=pot_img,
                       owner=current_user)
        else:
            pot = Pots(name=form.name.data,
                       location=form.location.data,
                       lon=form.lon.data, lat=form.lat.data,
                       owner=current_user)
        db.session.add(pot)
        db.session.commit()
        flash(
            f'New pot has been created. Found location {form.location.data}', 'success')
        return redirect(url_for("main.home"))
    return render_template("create_pot.html", title="New pot", form=form)


@pots.route("/pots/<int:pot_id>")
@login_required
def pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    # _weather, _pollution = get_weather(lon=pot.lon, lat=pot.lat)
    # # get weather icon
    # icon = _weather["weather"][0]["icon"]
    # icon_url = "https://openweathermap.org/img/wn/" + icon + "@2x.png"
    # print(f"ICOn URl : {icon_url}")
    # # create a html from json, and save in html file
    # weather = '{% block weather %}<div class="styled-table">' + \
    #     convert(_weather) + '</div>{% endblock %}'
    # pollution = '{% block pollution %}<div class="styled-table">' + \
    #     convert(_pollution) + '</div>{% endblock %}'
    # save_to_html(name=f'{weather=}'.split('=')[0], content=weather)
    # save_to_html(name=f'{pollution=}'.split('=')[0], content=pollution)
    icon_url = ".."
    plant = Plant.query.get(pot.plant_id)
    if plant:
        plant_status_id = get_plant_status(light_level_id=plant.light_level,
                                           water_level_id=plant.water_level,
                                           temp_min=plant.temp_min,
                                           temp_max=plant.temp_max)
        light_level = [x for x in light_levels if x['id']
                       == plant.light_level][0]['description']
        water_level = [x for x in water_levels if x['id']
                       == plant.water_level][0]['description']
        plant_status_description = plant_status[plant_status_id]
        return render_template("pot.html",
                               title=pot.name,
                               pot=pot,
                               plant=plant,
                               light_level=light_level,
                               water_level=water_level,
                               icon_url=icon_url,
                               status=plant_status_description,
                               status_id=str(plant_status_id))
    return render_template("pot.html",
                           title=pot.name,
                           pot=pot,
                           plant=plant,
                           icon_url=icon_url)


@pots.route("/pots/<int:pot_id>/connect_db", methods=['GET', 'POST'])
@login_required
def connect_plant_db(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PlantDBForm()
    if form.validate_on_submit():
        data = read_latest_scrapped_data()
        if form.db_id.data >= len(data):
            flash(
                "ID doesn't exist in DB. Look for Plants in the top navigation.", 'danger')
            return redirect(url_for('pots.connect_plant_db', pot_id=pot.id))
        else:
            name = data[form.db_id.data]['common_name']
            temp_min = data[form.db_id.data]['temperature_min._(c\u00b0)']
            temp_max = data[form.db_id.data]['temperature_max._(c\u00b0)']
            light_level = [x for x in light_levels if str(
                data[form.db_id.data]['light_ideal']) in x['description']][0]['id']
            water_level = [x for x in water_levels if str(
                data[form.db_id.data]['watering']) in x['description']][0]['id']
            plant = Plant(name=name,
                          temp_min=temp_min,
                          temp_max=temp_max,
                          light_level=light_level,
                          water_level=water_level,
                          pots_id=[pot])
            db.session.add(plant)
            db.session.commit()
            flash('Pot has been updated.', 'success')
            return redirect(url_for("pots.pot", pot_id=pot.id))
    return render_template("create_plant_db.html", title="Connect plant from db to pot", form=form)


@pots.route("/pots/<int:pot_id>/edit_plant", methods=['GET', 'POST'])
@login_required
def edit_plant(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PlantCustomForm()
    if form.validate_on_submit():
        plant = Plant(name=form.name.data,
                      temp_min=form.temp_min.data,
                      temp_max=form.temp_max.data,
                      light_level=form.light_level.data,
                      water_level=form.water_level.data,
                      pots_id=[pot])
        db.session.add(plant)
        db.session.commit()
        flash(f'Plant data has been updated', 'success')
        return redirect(url_for('pots.pot', pot_id=pot.id))
    elif request.method == "GET":
        plant = Plant.query.get(pot.plant_id)
        if plant:
            form.name.data = plant.name
            form.temp_min.data = plant.temp_min
            form.temp_max.data = plant.temp_max
            form.light_level.data = plant.light_level
            form.water_level.data = plant.water_level
    return render_template("edit_plant.html", title="Manually edit connected plant", form=form)


@pots.route("/pots/<int:pot_id>/update_plant", methods=['GET', 'POST'])
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
        return redirect(url_for('pots.pot', pot_id=pot.id))
    elif request.method == "GET":
        form.name.data = plant.name
        form.temp_min.data = plant.temp_min
        form.temp_max.data = plant.temp_max
        form.light_level.data = plant.light_level
        form.water_level.data = plant.water_level
    return render_template("edit_plant.html", title="Manually edit connected plant", form=form)


@pots.route("/pots/<int:pot_id>/update", methods=['GET', 'POST'])
@login_required
def update_pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    form = PotForm()
    if form.validate_on_submit():
        if form.image.data:
            pot.pot_image = save_img(
                form_image=form.image.data, save_dir="static/pot_img", size_x=375, size_y=375)
        else:
            pot.pot_image = pot.pot_image
        pot.name = form.name.data
        pot.location = form.location.data
        pot.lat = form.lat.data
        pot.lon = form.lon.data
        db.session.commit()
        flash('Pot has been updated.', 'success')
        return redirect(url_for("pots.pot", pot_id=pot.id))
    elif request.method == "GET":
        form.name.data = pot.name
        form.location.data = pot.location
        form.image.data = pot.pot_image
    return render_template("create_pot.html", title="Update pot", form=form)


@pots.route("/pots/<int:pot_id>/delete", methods=['POST'])
@login_required
def delete_pot(pot_id):
    pot = Pots.query.get_or_404(pot_id)
    if pot.owner != current_user:
        abort(403)
    db.session.delete(pot)
    db.session.commit()
    flash('Pot has been deleted.', 'success')
    return redirect(url_for("main.home"))
