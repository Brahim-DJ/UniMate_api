from flask import Blueprint, request, jsonify
import re
from app.utils.database import connect_to_supabase

post_bp = Blueprint('posts', __name__)

@post_bp.route('/add', methods=['POST'])
def addPost():
    supabase = connect_to_supabase()

    data = request.get_json
