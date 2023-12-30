from flask import Blueprint, request, jsonify
import re
from app.utils.database import connect_to_supabase

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/add', methods=['POST'])
def addComment():
    supabase = connect_to_supabase()

    data = request.form

    userId = data.get('userId')
    postId = data.get('postId')
    content = data.get('content')

    try:
        comment_data = {'user_id': userId, 'post_id': postId, 'content': content}
        res = supabase.table('comments').insert(comment_data).execute()
    except Exception as ex:
        return jsonify({'message': 'adding post failed', 'errors': [str(ex)]}), 400