from flask import Blueprint, request, jsonify
from app.utils.database import connect_to_supabase

post_bp = Blueprint('posts', __name__)

@post_bp.route('/add', methods=['POST'])
def addPost():
    supabase = connect_to_supabase()

    data = request.form

    userId = data.get('userId')
    content = data.get('content')
    universityTag = data.get('universityTag')
    specialtyTag = data.get('specialtyTag')
    yearTag = data.get('yearTag')
    tags = data.get('tags')
    image = request.files.get('image')
    groupid=data.get('groupid')
    try:
        post_data = {'user_id': userId, 'content': content, 'university_tag': universityTag, 'specialty_tag': specialtyTag, "year_tag": yearTag, "tags": tags,
                     **({'group_id': groupid} if groupid is not None else {}),}
        res = supabase.table('posts').insert(post_data).execute()
        
        postId = res.data[0]['id']
        if image:
            supabase.storage.from_("posts").upload(
                file=image.read(),
                path=f'posts/{userId}/{postId}',  # Adjust the path as needed
                file_options={"content-type": image.mimetype}
            )
            url = supabase.storage.from_('posts').get_public_url(f'posts/{userId}/{postId}')
            ret = supabase.table('posts').update({'image_url': url}).eq('id', postId).execute()

        return jsonify({
                'message': 'post added successfully',
                
            }), 200
    
    except Exception as ex:
        return jsonify({'message': 'adding post failed', 'errors': [str(ex)]}), 400

@post_bp.route('/get', methods=['POST'])
def getPosts():
    supabase = connect_to_supabase()
    try:
        res = supabase.table('posts').select("*, users(*), postVotes(vote_type)").execute()

        return res.data
    except Exception as ex:
        return jsonify({'message': 'getting posts failed', 'errors': [str(ex)]}), 400   


@post_bp.route('/vote', methods=['POST'])
def votePost():
    supabase = connect_to_supabase()

    data = request.form

    UserId = data.get('userId')
    PostId = data.get('postId')
    up = data.get('up') == '1'
    redo = data.get('redo') == '1'
    
    try:
        if up:
            res = supabase.table('posts').select('up_votes').eq('id', PostId).execute()
            current_up_votes = res.data[0]['up_votes']
            if redo:
                supabase.table('posts').update({'up_votes': current_up_votes - 1}).eq('id', PostId).execute()
                supabase.table('postVotes').delete().eq('user_id', UserId).eq('post_id', PostId).execute()
            else:
                supabase.table('posts').update({'up_votes': current_up_votes + 1}).eq('id', PostId).execute()
                voteData = {'user_id': UserId, 'post_id': PostId, 'vote_type': True}
                supabase.table('postVotes').insert(voteData).execute()
        else:
            res = supabase.table('posts').select('down_votes').eq('id', PostId).execute()
            current_down_votes = res.data[0]['down_votes']
            if redo:
                supabase.table('posts').update({'down_votes': current_down_votes - 1}).eq('id', PostId).execute()
                supabase.table('postVotes').delete().eq('user_id', UserId).eq('post_id', PostId).execute()
            else:
                supabase.table('posts').update({'down_votes': current_down_votes + 1}).eq('id', PostId).execute()
                voteData = {'user_id': UserId, 'post_id': PostId, 'vote_type': False}
                supabase.table('postVotes').insert(voteData).execute()

        return jsonify({}), 200
    
    except Exception as ex:
        return jsonify({'message': 'voting failed', 'errors': [str(ex)]}), 400
    
@post_bp.route('/getVote', methods=['POST'])
def getVote():
    supabase = connect_to_supabase()

    data = request.form

    UserId = data.get('userId')
    PostId = data.get('postId')

    try:
        res = supabase.table('postVotes').select('vote_type').eq('user_id', UserId).eq('post_id', PostId).execute()

        if len(res.data) > 0:
            return res.data
        else: return jsonify({'message': 'noData'}), 200

    except Exception as ex:
        return jsonify({'message': 'getting vote failed', 'errors': [str(ex)]}), 400  
