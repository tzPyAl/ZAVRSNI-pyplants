import json
from json2table import convert
from flask import render_template, flash, Blueprint
from flask_login import login_required
from pyplant.main.utils import read_latest_scrapped_data, save_to_html
from pyplant.plants.forms import SearchForm

plants = Blueprint("plants", __name__)


@plants.route("/plants", methods=['GET', 'POST'])
@login_required
def plant():
    show_plant = False
    form = SearchForm()
    if form.validate_on_submit():
        data = read_latest_scrapped_data()
        output_dict = [x for x in data if form.search.data.lower()
                       in x["common_name"]]
        output_json = json.dumps(output_dict)
        if output_json == '[]':
            flash('No results. Try again', 'warning')
        else:
            json_object = json.loads(output_json)
            plant_img = json_object[0]['image_url']
            plant_table = '{% block plant %}' + \
                convert(json_object[0]) + '{% endblock %}'
            save_to_html(name=f'{plant_table=}'.split('=')[0],
                         content=plant_table)
            show_plant = True
            flash(f'Found {form.search.data}', 'info')
            return render_template("plants.html",
                                   title="Plant found",
                                   form=form,
                                   plant_img=plant_img,
                                   show_plant=show_plant)
    return render_template("plants.html",
                           title="Plants database",
                           form=form,
                           show_plant=show_plant)
