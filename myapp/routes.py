from flask import Blueprint, redirect, url_for, render_template, jsonify, request


from .extensions import db
from .models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@main.route('/add', methods=["POST"])
def add_user():
    username = request.form.get("username")  # ดึงค่าจาก input form
    if username:  # กันค่าที่ว่าง
        db.session.add(User(username=username))
        db.session.commit()
    return redirect(url_for("main.index"))