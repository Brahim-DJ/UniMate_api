from flask import Blueprint, request, jsonify
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

        return jsonify({
                'message': 'post added successfully'
            }), 200
    except Exception as ex:
        return jsonify({'message': 'adding comment failed', 'errors': [str(ex)]}), 400

@comment_bp.route('/get', methods=['POST'])
def getComments():
    supabase = connect_to_supabase()

    data = request.form
    postId = data.get('postId')
    print(type(postId))
    try:
        res = supabase.table('comments').select("*, users(id, email, name, avatar_url), commentVotes(vote_type)").eq('post_id', postId).execute()

        return res.data
    except Exception as ex:
        return jsonify({'message': 'getting comments failed', 'errors': [str(ex)]}), 400
    
@comment_bp.route('/vote', methods=['POST'])
def voteComment():
    supabase = connect_to_supabase()

    data = request.form

    UserId = data.get('userId')
    CommentId = data.get('commentId')
    up = data.get('up') == '1'
    redo = data.get('redo') == '1'
    
    try:
        if up:
            res = supabase.table('comments').select('up_votes').eq('id', CommentId).execute()
            current_up_votes = res.data[0]['up_votes']
            if redo:
                supabase.table('comments').update({'up_votes': current_up_votes - 1}).eq('id', CommentId).execute()
                supabase.table('commentVotes').delete().eq('user_id', UserId).eq('comment_id', CommentId).execute()
            else:
                supabase.table('comments').update({'up_votes': current_up_votes + 1}).eq('id', CommentId).execute()
                voteData = {'user_id': UserId, 'comment_id': CommentId, 'vote_type': True}
                supabase.table('commentVotes').insert(voteData).execute()
        else:
            res = supabase.table('comments').select('down_votes').eq('id', CommentId).execute()
            current_down_votes = res.data[0]['down_votes']
            if redo:
                supabase.table('comments').update({'down_votes': current_down_votes - 1}).eq('id', CommentId).execute()
                supabase.table('commentVotes').delete().eq('user_id', UserId).eq('comment_id', CommentId).execute()
            else:
                supabase.table('comments').update({'down_votes': current_down_votes + 1}).eq('id', CommentId).execute()
                voteData = {'user_id': UserId, 'comment_id': CommentId, 'vote_type': False}
                supabase.table('commentVotes').insert(voteData).execute()

        return jsonify({}), 200
    
    except Exception as ex:
        return jsonify({'message': 'voting failed', 'errors': [str(ex)]}), 400