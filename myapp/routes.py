from flask import Blueprint, redirect, url_for, render_template, jsonify, request, flash
from .extensions import db
from .models import User, Employee
from datetime import datetime

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@main.route('/api/employees/search')
def search_employees():
    query = request.args.get("q", "").lower()
    employees = Employee.query.filter(
        (Employee.first_name.ilike(f"%{query}%")) |
        (Employee.last_name.ilike(f"%{query}%")) |
        (Employee.email.ilike(f"%{query}%")) |
        (Employee.phone.ilike(f"%{query}%")) |
        (Employee.position.ilike(f"%{query}%"))
    ).all()

    results = [
        {
            "id": emp.employee_id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "email": emp.email,
            "phone": emp.phone,
            "position": emp.position,
            "created_at": emp.created_at,
            "updated_at": emp.updated_at,
        }
        for emp in employees
    ]
    return jsonify(results)

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

@main.route('/edit/<int:employee_id>', methods=["POST"])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee.first_name = request.form.get("first_name")
    employee.last_name = request.form.get("last_name")
    employee.email = request.form.get("email")
    employee.phone = request.form.get("phone")
    employee.position = request.form.get("position")
    employee.updated_at = datetime.utcnow()  # อัปเดตเวลาล่าสุด
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route('/delete/<int:employee_id>', methods=["POST"])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for("main.index"))