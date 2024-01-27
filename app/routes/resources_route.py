from flask import Blueprint, request, jsonify
from app.utils.database import connect_to_supabase
import uuid

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/')
def authhello():
    return jsonify({'message': 'accessing resources service test 1', 'errors': ['hello']}), 400


@resources_bp.route('/rateResource', methods=['POST'])
def rate_resource():

    print('i was called heree ')
    supabase = connect_to_supabase()

    data = request.form

    print ('the returned data is ')
    print (data)
    resource_id = data.get('resourceId')
    user_id = data.get('userId')
    rating = data.get('rating')
    thedata = {'resource_id': resource_id, 'rating': rating, 'user_id': user_id}
    print(thedata)

    # Handle rating insert/update in resource_ratings table
    try:
        # Handle rating insert/update in resource_ratings table
        data, count = supabase.table('resource_ratings').upsert(
            {'resource_id': resource_id, 'rating': rating, 'user_id': user_id}
        ).execute()
    except Exception as e:
        print(f"Error while inserting/updating rating: {e}")
        return jsonify({'error': 'Failed to submit rating'}), 500

   
    # Fetch all ratings for the specific resource
    ratings_rows = supabase.table('resource_ratings').select('rating').eq('resource_id', resource_id).execute()
    ratings = [row['rating'] for row in ratings_rows.data]

    # Calculate the average rating
    average_rating = sum(ratings) / len(ratings) if ratings else 0

    # Update the resource table with the new average rating
    supabase.table('resources').update({'rating': average_rating}).eq('id', resource_id).execute()

    return jsonify({'message': 'Rating submitted successfully'}), 200


@resources_bp.route('/getResources')
def get_all_resources():
    supabase = connect_to_supabase()

    # Fetch all resources from the 'resources' table
    resources_rows = supabase.table('resources').select('*').execute()

    resources_data = []

    for resource_row in resources_rows.data:
        resources_data.append({
            'id': resource_row['id'],
            'title': resource_row['title'],
            'description': resource_row['description'],
            'specialty': resource_row['specialty'],
            'rating': resource_row['rating'],
            # Add other fields as needed
        })

    return resources_data, 200


@resources_bp.route('/<resource_id>', methods=['GET'])
def get_resource_data(resource_id):
    supabase = connect_to_supabase()

    resource_row = supabase.table('resources').select('*').eq('id', resource_id).execute()

    if not resource_row:
        return jsonify({'error': 'Resource not found'}), 404

    resource_data = {
        'title': resource_row.data[0]['title'],
        'description': resource_row.data[0]['description'],
        'rating': resource_row.data[0]['rating'],
        'attachments': [],
    }

    attachment_rows = supabase.table('resource_attachments').select('attachment_url').eq('resource_id', resource_id).execute()

    for attachment_row in attachment_rows.data:
        resource_data['attachments'].append({
            'fileName': attachment_row['attachment_url'].split('/')[-1],  # Extracting the file name from the URL
            'url': attachment_row['attachment_url'],
        })

        print('returned status code 200')

    return jsonify(resource_data), 200




@resources_bp.route('/uploadResource', methods=['POST'])
def uploadResource():
    supabase = connect_to_supabase()

    data = request.form

    title = data.get('title')
    specialty = data.get('specialty')
    description = data.get('description')
    user_id = data.get('user_id')

    # Handle file uploads
    files = request.files.getlist('files')

    if files:
        resource_data = {'title': title, 'specialty': specialty, 'description': description, 'user_id': user_id}
        resource_record = supabase.table('resources').insert(resource_data).execute()
        resource_id = resource_record.data[0]['id']

        attachments = []

        for file in files:
            # Generate a unique filename using uuid
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            file_path = f"resources/{unique_filename}"  # Storing in 'resources' bucket
            file_options = {"content-type": file.mimetype}

            # Upload file to Supabase storage with the unique filename
            supabase.storage.from_("resources").upload(
                file=file.read(),
                path=file_path,
                file_options=file_options
            )

            # Get Supabase storage URL
            attachment_url = supabase.storage.from_('resources').get_public_url(file_path)

            # Store the attachment in the new database table
            attachment_data = {'resource_id': resource_id, 'attachment_url': attachment_url}
            supabase.table('resource_attachments').insert(attachment_data).execute()

            attachments.append({'attachment_url': attachment_url})

        resource_data['attachments'] = attachments

        return jsonify(resource_data), 200
    else:
        return jsonify({'error': 'No files provided in the request'}), 400

@resources_bp.route('/getUserCollections', methods=['GET'])
def get_user_collections():
    user_id = request.args.get('userId')
    supabase = connect_to_supabase()

    collections_rows = supabase.table('collections').select('*').eq('user_id', user_id).eq('type', 'resource').execute()
    collections = [{'id': row['id'], 'name': row['name']} for row in collections_rows.data]
    print(collections)

    return jsonify(collections), 200

@resources_bp.route('/submitSelectedCollections', methods=['POST'])
def submit_selected_collections():
    data = request.json
    user_id = data.get('userId')
    resource_id = data.get('resourceId')
    selected_collection_ids = data.get('selectedIds')
    supabase = connect_to_supabase()

    for collection_id in selected_collection_ids:
        try:
            # Upsert the record in the collection_resource table
            supabase.table('collection_resource').upsert({
                'user_id': user_id,
                'resource_id': resource_id,
                'collection_id': collection_id
            }).execute()
        except Exception as e:
            print(f"Error while upserting into collection_resource table: {e}")
            return jsonify({'error': 'Failed to submit collections'}), 500

    return jsonify({'message': 'Collections submitted successfully'}), 200


@resources_bp.route('/addNewCollection', methods=['POST'])
def add_new_collection():
    data = request.json
    user_id = data.get('userId')
    collection_name = data.get('name')
    supabase = connect_to_supabase()

    try:
        collection_data = {'user_id': user_id, 'name': collection_name, 'type': 'resource'}
        supabase.table('collections').insert(collection_data).execute()
    except Exception as e:
        print(f"Error while adding new collection: {e}")
        return jsonify({'error': 'Failed to add new collection'}), 500

    return jsonify({'message': 'New collection added successfully'}), 200
