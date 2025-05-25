from flask import Blueprint, jsonify
from restaurant.database import session
from restaurant.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = session.query(User).all()
        user_list = [{
            'id': user.id,
            'name': user.name,
            'phone': user.phone,
            'email': user.email
        } for user in users]
        
        return jsonify({'users': user_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
