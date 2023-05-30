from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from pyplant.db_models import Pots

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
