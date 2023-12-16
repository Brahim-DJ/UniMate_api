from flask import Blueprint, request, jsonify
import re
from app.utils.database import connect_to_supabase

auth_bp = Blueprint('auth', __name__)

# Function to handle user signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    supabase = connect_to_supabase()
    data = request.json
    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')
    name = data.get('name')
    errors = []

    # Validation functions
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def is_valid_password(password, confirm_password):
        if not password or len(password) < 8:
            return 'Password should be at least 8 characters long'
        elif password != confirm_password:
            return 'Passwords do not match'
        return None

    # Validate email
    if not email or not is_valid_email(email):
        errors.append('Email needs to be valid')

    # Validate password
    password_error = is_valid_password(password, confirmPassword)
    if password_error:
        errors.append(password_error)

    # Check for existing user
    existing_user = supabase.table('users').select("*").ilike('email', email).execute()
    if len(existing_user.data) > 0:
        errors.append('User already exists')

    # If errors, return them
    if errors:
        return jsonify({'message': 'Signup failed', 'errors': errors}), 400
    

    # Signup the user
    try:
        res = supabase.auth.sign_up({'email': email, 'password': password})
        user_info = res.user
        if user_info:
            user_id = user_info.id
            user_email = user_info.email

            # Insert user into the database
            response = supabase.table('users').insert({'id': user_id, 'email': user_email, 'name': name}).execute()

            return jsonify({
                'id': user_id,
                'email': user_email,
                'name': name
            }), 200
        else:
            return jsonify({'message': 'Signup failed! User information not found'}), 400

    except Exception as e:
        return jsonify({'message': f'Signup failed! Error: {str(e)}'}), 400


@auth_bp.route('/signin', methods=['POST'])
def signin():
    supabase = connect_to_supabase()
    data = request.json

    res = supabase.auth.sign_in_with_password({'email': data.get('email'), 'password': data.get('password')})

    if isinstance(res, Exception):
        return jsonify({'message': f'Sign-in failed! Error: {res}'}), 400

    else:
        user_info = res.user

        if user_info:
            user_id = user_info.id # Access the 'id' attribute from 'user_info'
            user_email = user_info.email  # Access the 'email' attribute from 'user_info'
            response = supabase.table('users').select('name').eq('id', user_id).execute()

            return jsonify({
                'id': user_id, 'email': user_email, 'name': response.name
            }), 200
        else:
            return jsonify({'message': 'Sign-in failed! User information not found'}), 400
