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
    from app.routes.posts_route import post_bp
    from app.routes.comment_route import comment_bp
    from app.routes.group_route import group_bp
    from app.routes.profile_route import profile_bp
    from app.routes.post_collection_route import post_collection_bp
    from app.routes.resources_route import resources_bp

    app.register_blueprint(home_route.bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/post')
    app.register_blueprint(comment_bp, url_prefix='/comment')
    app.register_blueprint(group_bp, url_prefix='/group')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(post_collection_bp, url_prefix='/post_collection')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    # Add more blueprints as needed for other tables/routes

    return app
