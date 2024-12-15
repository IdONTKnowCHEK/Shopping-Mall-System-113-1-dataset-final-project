from flask import Blueprint
from api.test_route import test_bp

def register_blueprints(app):
    app.register_blueprint(test_bp)
