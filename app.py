from flask import Flask
from routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # Add root route
    @app.route('/')
    def home():
        return {"message": "FoodieSpot API is running!", 
                "endpoints": ["/api/restaurants", "/api/users"]}
    
    # Register all routes
    register_routes(app)
    
    return app
app= create_app()
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

