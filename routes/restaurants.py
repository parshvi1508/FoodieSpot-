from flask import Blueprint, jsonify
from restaurant.database import session
from restaurant.models import Restaurant

restaurants_bp = Blueprint('restaurants', __name__)

@restaurants_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = session.query(Restaurant).all()
        restaurant_list = []
        
        for restaurant in restaurants:
            restaurant_data = {
                'id': restaurant.id,
                'name': restaurant.name,
                'cuisine': restaurant.cuisine,
                'location': restaurant.location,
                'capacity': restaurant.capacity,
                'available_tables': len([t for t in restaurant.tables if t.is_available])
            }
            restaurant_list.append(restaurant_data)
        
        return jsonify({'restaurants': restaurant_list}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
