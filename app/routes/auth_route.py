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

    else:
        user_info = res.user
        if user_info:
            user_id = user_info.id
            user_email = user_info.email

            response = supabase.table('users').insert({'id': user_id, 'email': user_email, 'name': name}).execute()

            return jsonify({
                'id': user_id, 'email': user_email, 'name': name
            }), 200
        else:
            return jsonify({'message': 'Signup failed! User information not found'}), 400
        

        
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
