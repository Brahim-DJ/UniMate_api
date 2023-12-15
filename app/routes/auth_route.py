from flask import Blueprint, request, jsonify
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
    error = False
    
    if (not email) or (len(email)<5):
        error='Email needs to be valid'
    if (not error) and ( (not password) or (len(password)<8) ):
        error='Provide a password'        
    if (not error):    
        response = supabase.table('users').select("*").ilike('email', email).execute()
        if len(response.data)>0:
            error='User already exists'
    if (not error):
        res = supabase.auth.sign_up({'email': email, 'password': password})

    if isinstance(res, Exception):
        return jsonify({'message': f'Signup failed! Error: {res}'}), 400

    if 'error' in res and res['error'] is not None:
        error_message = res['error']['message']
        return jsonify({'message': f'Signup failed! Error: {error_message}'}), 400
    else:
        user_info = res.user
        if user_info:
            user_id = user_info.id
            user_email = user_info.email

            response = supabase.table('users').insert({'auth_id': user_id, 'email': user_email, 'name': name}).execute()

            return jsonify({
                'message': f'Signup successful! User ID: {user_id}, Email: {user_email}'
            }), 200
        else:
            return jsonify({'message': 'Signup failed! User information not found'}), 400
        

        
@auth_bp.route('/signin', methods=['POST'])
def signin():
    # Extract data from the request
    data = request.json  # Assuming the request contains JSON data with 'email' and 'password'

    # Connect to Supabase
    supabase = connect_to_supabase()

    # Attempt to sign in the user using Supabase auth
    res = supabase.auth.sign_in_with_password({'email': data.get('email'), 'password': data.get('password')})

    # Check the response from Supabase auth
    if isinstance(res, Exception):
        return jsonify({'message': f'Sign-in failed! Error: {res}'}), 400

    if 'error' in res and res['error'] is not None:
        error_message = res['error']['message']
        return jsonify({'message': f'Sign-in failed! Error: {error_message}'}), 400
    else:
        # Extract user information from the sign-in response
        user_info = res.user

        if user_info:
            user_id = user_info.id # Access the 'id' attribute from 'user_info'
            user_email = user_info.email  # Access the 'email' attribute from 'user_info'

            return jsonify({
                'message': f'Sign-in successful! User ID: {user_id}, Email: {user_email}'
            }), 200
        else:
            return jsonify({'message': 'Sign-in failed! User information not found'}), 400
