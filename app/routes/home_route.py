from flask import Blueprint, jsonify
from app.utils.database import connect_to_supabase

# Create a blueprint for home routes
bp = Blueprint('home', __name__)

# Define the route and function
@bp.route('/')
def hello():
    # supabase = connect_to_supabase()
    # res = supabase.table('users').select('*').execute()

    # return jsonify({'data': res.data}), 200
    return jsonify({'message': 'Signup failed', 'errors': ['hello']}), 400
