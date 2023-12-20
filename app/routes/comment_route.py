from flask import Blueprint, request, jsonify
import re
from app.utils.database import connect_to_supabase

comment_bp = Blueprint('comment', __name__)
