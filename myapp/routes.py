from flask import Blueprint, redirect, url_for, render_template, jsonify, request


from .extensions import db
from .models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/') 
def index():
	users = User.query.all()
	users_list_html = [f"<li>{ user.username }</li>" for user in users]
	return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add/<username>')
def add_user(username):
	db.session.add(User(username=username))
	db.session.commit()
	return redirect(url_for("main.index"))