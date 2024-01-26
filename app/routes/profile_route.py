from flask import Blueprint, jsonify, request
from app.utils.database import connect_to_supabase
import os
import uuid

# Create a blueprint for home routes
profile_bp = Blueprint('profile', __name__)

# Define the route and function
@profile_bp.route('/editprofile', methods=['POST'])
def edit_profile():
    try:
        supabase = connect_to_supabase()
        data = request.form
        bio = data.get('bio')
        name = data.get('name')
        userid = data.get('userid')
        avatar = request.files.get('avatar')
        print("ani hnaaaaaa")
        print(avatar)
        # Check if the user exists
        existing_user = supabase.from_('users').select('*').eq('id', userid).execute()

        # Inside the existing_user block where you update the profile
        if len(existing_user.data) > 0:
            # User exists, update the profile
            user_data = {'name': name}

            if bio:
                user_data['bio'] = bio

            if avatar!= None:
                unique_filename = str(uuid.uuid4())
                avatar_filename = f'avatars/{userid}/avatar/{unique_filename}.jpg'

                # Before upload
                print(f"Uploading avatar: {avatar_filename}")

                # Remove the previous avatar if it exists
                previous_avatar_url = existing_user.data[0].get('avatar_url')
                
                print(f"previous_avatar_url:{previous_avatar_url}")
                if previous_avatar_url:
                    # Extract the path from the previous avatar URL
                    try:
                        avatar_path = previous_avatar_url
                    except IndexError:
                        avatar_path = None

                    # Remove the previous avatar
                    if avatar_path:
                      try:
                           # Ensure the 'path' is a string, not a URL
                           avatar_path = avatar_path.split("/")[-1]  # Extract the file name from the URL
                           supabase.storage.from_("avatars").remove(path=avatar_path)
                           print(f"Previous avatar removed successfully. Path: {avatar_path}")
                      except Exception as remove_error:
                           print(f"Error removing previous avatar: {remove_error}")

                # Upload the new avatar image to Supabase storage with the unique filename
                try:
                    # Upload the new avatar image to Supabase storage
                    supabase.storage.from_("avatars").upload(
                        file=avatar.read(),
                        path=avatar_filename,
                        file_options={"content-type": avatar.mimetype}
                    )

                    # After upload
                    avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_filename)
                    print(f"Avatar uploaded successfully. URL: {avatar_url}")

                    # Get the public URL of the uploaded avatar image
                    user_data['avatar_url'] = avatar_url
                except Exception as upload_error:
                    print(f"Error during upload: {upload_error}")

            # Update the user's profile
            print(f"userdata:{user_data}")
            supabase.from_('users').update(user_data).eq('id', userid).execute()
            
            if avatar:
                return jsonify({
                'name': name,
                'avatarUrl': avatar_url,
                'bio': bio
                     }), 200
            else:
                 return jsonify({
                'name': name,
                'avatarUrl': '',
                'bio': bio
                     }), 200
           

        else:
            # User not found
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@profile_bp.route('/posts', methods=['POST'])
def getposts():
    try:
        supabase = connect_to_supabase()
        data = request.form
        userid = data.get("id")
        
        result = supabase.from_('posts').select('*').eq('user_id', userid).execute()
        posts_data = result.data
       

        # Structure the data as a dictionary of dictionaries
        structured_data = {
            post['id']: {
                key: str(value) if key != 'image_url' else str(value) if value is not None else ''
                for key, value in post.items()
            }
            for post in posts_data
        }
        
        
        return jsonify(structured_data), 200
       
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
