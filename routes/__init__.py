from flask import Blueprint

# Import all blueprints
from .restaurants import restaurants_bp
from .reservations import reservations_bp
from .users import users_bp

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(restaurants_bp, url_prefix='/api')
    app.register_blueprint(reservations_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
