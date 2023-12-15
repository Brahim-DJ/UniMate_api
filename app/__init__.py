from flask import Flask
from app.utils.database import connect_to_supabase

def create_app():
    app = Flask(__name__)

    # Configuration settings (if any)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Connect to Supabase
    supabase = connect_to_supabase()

    # Pass the Supabase client to the app context for use in routes, etc.
    app.config['SUPABASE'] = supabase

    # Register blueprints (routes) for different modules
    from app.routes import home_route  # Import your routes here
    from app.routes.auth_route import auth_bp

    app.register_blueprint(home_route.bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # Add more blueprints as needed for other tables/routes

    return app
