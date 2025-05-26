from flask import Flask
from routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # ENSURE database initialization happens first
    with app.app_context():
        # Import here to ensure proper timing
        from restaurant.database import init_db
        print("[APP] Ensuring database initialization...")
        # Your init_db() will naturally integrate sample_data.py if needed
    
    # Add root route
    @app.route('/')
    def home():
        from restaurant.database import session
        from restaurant.models import Restaurant
        restaurant_count = session.query(Restaurant).count()
        return {
            "message": "FoodieSpot API is running!",
            "restaurants_in_database": restaurant_count,
            "endpoints": ["/api/restaurants", "/api/users"]
        }
    
    # Register all routes
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)
