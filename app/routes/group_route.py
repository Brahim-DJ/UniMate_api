from flask import Blueprint, jsonify, request
from app.utils.database import connect_to_supabase
from werkzeug.utils import secure_filename
import os
import uuid
from app.utils.database import supabase_url

# Create a blueprint for home routes
group_bp = Blueprint('group', __name__)

# Define the route and function
@group_bp.route('/addgroup', methods=['POST'])
def addgroup():
    try:
        
        supabase = connect_to_supabase()

        data = request.form
        bio = data.get('bio')
        name = data.get('name')
        adminid = data.get('adminid')
        year = data.get('year')
        specialty = data.get('specialty')
        tags = data.get('tags')
        
        # Handling file upload
        avatar = request.files.get('avatar')
      
        # Check if the file is present in the request
        if avatar:
            # Generate a unique filename for the avatar
            
            unique_filename = str(uuid.uuid4())
            avatar_filename = f'avatars-profile/{adminid}/avatar/{unique_filename}.jpg'
            
              # Upload the new avatar image to Supabase storage
            supabase.storage.from_("groups_avatars").upload(
                        file=avatar.read(),
                        path=avatar_filename,
                        file_options={"content-type": avatar.mimetype}
                    )
        avatar_url = supabase.storage.from_('groups_avatars').get_public_url(avatar_filename)
        


        # Add data to the Groups table
        groups_table = supabase.from_('Groups')
        new_group = {
            'Name': name,
            'year': year,
            'url_image': avatar_url,
            'Tags': tags,
            'Bio': bio,
            'Specialty': specialty,
            'adminid': adminid,
            'members':1
                # Add the avatar URL to the table
        }
      
        # Insert the new group into the Groups table
      
        result = groups_table.insert([new_group]).execute()
        group_id = result.data[0]['id']
        
        
        return jsonify({
                'groupid':group_id,
                'isadmin':1
            }), 200

    except Exception as e:
     print(f"Error: {e}")
   
     return jsonify({'error': str(e)}), 500
    

@group_bp.route('/getgroups', methods=['POST'])
def getgroups():
    try:
        supabase = connect_to_supabase()
        data = request.form

        group_ids_string = data.get("ids")
        if group_ids_string is not None:
          group_ids = group_ids_string.split(",")
    # Rest of your code with the group_ids list
        else:
    # Handle the case when "ids" is not present in data or is None
          group_ids = []

        
        
        result = supabase.table('Groups').select('*').in_('id', group_ids).execute()

        groups_data = result.data
        
       # Structure the data as a dictionary of dictionaries
 
        structured_data = {
            group['id']: {
                key: str(value) if key != 'coverpic_url' else str(value) if value is not None else ''
                for key, value in group.items()
            }
            for group in groups_data
        }
        return jsonify(structured_data), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
@group_bp.route('/addcoverimage', methods=['POST'])
def addcoverimage():
    # Connect to Supabase
    supabase = connect_to_supabase()
    
    
    # Get data from the request form
    data = request.form
    id = data.get("id")
    
    # Get the avatar file from the request
    avatar = request.files.get('avatar')
    
    # Check if the file is present in the request
    if avatar:
        # Generate a unique filename for the avatar
        unique_filename = str(uuid.uuid4())
        avatar_filename = f'avatars-profile/{id}/avatar/{unique_filename}.jpg'
        
        # Upload the new avatar image to Supabase storage
        supabase.storage.from_("groups_avatars").upload(
            file=avatar.read(),
            path=avatar_filename,
            file_options={"content-type": avatar.mimetype}
        )

        # Get the public URL of the uploaded avatar
        avatar_url = supabase.storage.from_('groups_avatars').get_public_url(avatar_filename)
        
        
       
            # Update the existing record with the new coverpic_url
        supabase.table('Groups').update({
                'coverpic_url': avatar_url,
            }).eq('id', id).execute()
        

        return jsonify({"message": "Cover image uploaded successfully.", "avatar_url": avatar_url})
        
           
    else:
        return jsonify({"error": "No avatar file provided in the request."})

# Define the route and function
@group_bp.route('/editgroup', methods=['POST'])
def editgroup():
    try:
        
        supabase = connect_to_supabase()

        data = request.form
        bio = data.get('bio')
        name = data.get('name')
        year = data.get('year')
        specialty = data.get('specialty')
        tags = data.get('tags')
        groupid = data.get('groupid')
        
        # Handling file upload
        avatar = request.files.get('avatar')
        print("adoulaaaaaa")
        print(avatar)
        # Check if the file is present in the request
        if avatar!=None:
            # Generate a unique filename for the avatar
           
            unique_filename = str(uuid.uuid4())
            avatar_filename = f'avatars-covpic/{groupid}/avatar/{unique_filename}.jpg'
            
              # Upload the new avatar image to Supabase storage
            supabase.storage.from_("groups_avatars").upload(
                        file=avatar.read(),
                        path=avatar_filename,
                        file_options={"content-type": avatar.mimetype}
                    )
            avatar_url = supabase.storage.from_('groups_avatars').get_public_url(avatar_filename)
        


        # update data Groups table
       
        updated_group = {
            'Name': name,
            'year': year,
            **({'url_image': avatar_url} if avatar is not None else {}),
            'Tags': tags,
            'Bio': bio,
            'Specialty': specialty,
            
                # Add the avatar URL to the table
        }
      
      
        supabase.from_('Groups').update(updated_group).eq('id', groupid).execute()
        
        
        
        return jsonify({
                'message':"edited succefully"
                
            }), 200

    except Exception as e:
     print(f"Error: {e}")
   
     return jsonify({'error': str(e)}), 500
        

@group_bp.route('/getsuggestedgroups', methods=['POST'])
def getsuggestedgroups():
    try:
        supabase = connect_to_supabase()
        data = request.form

        group_ids_string = data.get("ids")
        if group_ids_string is not None:
          group_ids = group_ids_string.split(",")
    # Rest of your code with the group_ids list
        else:
    # Handle the case when "ids" is not present in data or is None
          group_ids = []

        
        
        result = supabase.table('Groups').select('*').not_in('id', group_ids).execute()

        groups_data = result.data
        
       # Structure the data as a dictionary of dictionaries
 
        structured_data = {
            group['id']: {
                key: str(value) if key != 'coverpic_url' else str(value) if value is not None else ''
                for key, value in group.items()
            }
            for group in groups_data
        }
        return jsonify(structured_data), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500