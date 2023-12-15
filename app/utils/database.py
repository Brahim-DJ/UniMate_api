from dotenv import load_dotenv
load_dotenv('../../')

import os
from supabase import create_client

# Function to establish Supabase connection
def connect_to_supabase():
    # Replace 'your_url' and 'your_key' with your actual Supabase URL and Key
    supabase_url = os.environ.get("supabase_url")
    supabase_key = os.environ.get("supabase_key")
    
    # Create a Supabase client
    supabase = create_client(supabase_url, supabase_key)

    return supabase
