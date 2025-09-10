from flask import Blueprint, redirect, url_for, render_template, jsonify, request


from .extensions import db
from .models import User, Employee

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@main.route('/add', methods=["POST"])
def add_employee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    position = request.form.get("position")

    if first_name and last_name and email:
        new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            position=position
        )
        db.session.add(new_employee)
        db.session.commit()

    return redirect(url_for("main.index"))