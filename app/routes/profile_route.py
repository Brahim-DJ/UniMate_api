from flask import Blueprint, jsonify, request
from app.utils.database import connect_to_supabase
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
        if avatar!= None:
                unique_filename = str(uuid.uuid4())
                avatar_filename = f'avatars/{userid}/avatar/{unique_filename}.jpg' 
                # Upload the new avatar image to Supabase storage with the unique filename
                
                    # Upload the new avatar image to Supabase storage
                supabase.storage.from_("avatars").upload(
                        file=avatar.read(),
                        path=avatar_filename,
                        file_options={"content-type": avatar.mimetype}
                    )

                    # After upload
                avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_filename) 
        user_data = {
            'name': name,
            **({'avatar_url': avatar_url} if avatar is not None else {}),
            'bio': bio
                      # Add the avatar URL to the table
        }
        print(user_data)
        print(userid)
        # Execute Supabase update operation
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
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/posts', methods=['POST'])
def getposts():
    try:
        supabase = connect_to_supabase()
        data = request.form
        userid = data.get("id")
        
        result = supabase.from_('posts').select("*, users(*), postVotes(vote_type)").eq('user_id', userid).execute()
        posts_data = result.data
       
        return jsonify(posts_data), 200
       
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
