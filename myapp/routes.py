from flask import Blueprint, redirect, url_for, render_template, jsonify, request


from .extensions import db
from .models import User

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_list)

@main.route('/api/users/add', methods=['POST'])
def add_user_api():
    data = request.get_json()  # {"username": "newuser"}
    if not data or "username" not in data:
        return jsonify({"error": "Missing username"}), 400

    new_user = User(username=data["username"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added", "id": new_user.id})