import os

from flask import Flask 

from .extensions import db
from .routes import main
from .models import Employee

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgresql://cloud_employee_manager_user:yYYz0c9QSIONdApJQTymN1n47gyIq4yV@dpg-d2jnnkggjchc73cqqm9g-a.oregon-postgres.render.com/cloud_employee_manager

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app