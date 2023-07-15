from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from pyplant.db_models import Pots
from pyplant.main.utils import generate_random_status
from pyplant import db

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    pots = Pots.query.filter_by(
        owner=current_user).paginate(page=page, per_page=6)
    return render_template('home.html', pots=pots)


@main.route("/info")
@login_required
def info():
    return render_template('info.html')


@main.route("/contact")
@login_required
def contact():
    return render_template('contact.html')


@main.route("/sync_data")
@login_required
def sync_data():
    # fetch all pots at current age
    page = request.args.get('page', 1, type=int)
    pots = Pots.query.filter_by(
        owner=current_user).paginate(page=page, per_page=6)
    # generate new status for each of pots, IoT data will be generated when you enter pot profile
    # guess this is fince since only status is visible on home page
    for pot in pots:
        pot.status = generate_random_status()
    # save status to db
    db.session.commit()
    return redirect(url_for("main.home"))
