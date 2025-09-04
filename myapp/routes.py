from flask import Blueprint, redirect, url_for, render_template


from .extensions import db
from .models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/add/<username>')
def add_user(username):
    db.session.add(User(username=username))
    db.session.commit()
    return redirect(url_for("main.index"))