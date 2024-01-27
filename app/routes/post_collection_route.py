from flask import Blueprint, request, jsonify
from app.utils.database import connect_to_supabase

post_collection_bp = Blueprint('posts_collection', __name__)

@post_collection_bp.route('/addPostToCollection', methods=['POST'])
def addPostToCollection():
    supabase = connect_to_supabase()

    data = request.form
    userId = data.get('userId')
    postId = data.get('postId')
    collectionId = data.get('collectionId')

    try:
        post_collection_data = {'user_id': userId, 'post_id': postId, 'collection_id': collectionId}
        supabase.table('postCollection').insert(post_collection_data).execute()

        return jsonify({'message': 'success'}), 200
    except Exception as ex:
        return jsonify({'message': 'adding post to collection failed', 'errors': [str(ex)]}), 400
    

@post_collection_bp.route('/getPostFromCollection', methods=['POST'])
def getPostFromCollection():
    supabase = connect_to_supabase()

    data = request.form
    userId = data.get('userId')
    collectionId = data.get('collectionId')

    try:
        ret = supabase.table('postCollection').select('posts(*)').eq('user_id', userId).eq('collection_id', collectionId).execute()

        return ret.data
    except Exception as ex:
        return jsonify({'message': 'getting posts from collection failed', 'errors': [str(ex)]}), 400


@post_collection_bp.route('/addCollection', methods=['POST'])
def addCollection():
    supabase = connect_to_supabase()

    data = request.form
    userId = data.get('userId')
    name = data.get('name')
    type = data.get('type')

    try:
        collection_data = {'user_id': userId, 'name': name, 'type': type}
        supabase.table('collections').insert(collection_data).execute()

        return jsonify({'message': 'success'}), 200
    except Exception as ex:
        return jsonify({'message': 'adding collection failed', 'errors': [str(ex)]}), 400
    

@post_collection_bp.route('/getCollections', methods=['POST'])
def getCollections():
    supabase = connect_to_supabase()

    data = request.form
    userId = data.get('userId')

    try:
        ret = supabase.table('collections').select('*').eq('user_id', userId).eq('type', 'posts').execute()

        return ret.data
    except Exception as ex:
        return jsonify({'message': 'getting collections failed', 'errors': [str(ex)]}), 400