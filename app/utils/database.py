from dotenv import load_dotenv
load_dotenv('../../')

import os
from supabase import create_client

# Function to establish Supabase connection
def connect_to_supabase():
    # Replace 'your_url' and 'your_key' with your actual Supabase URL and Key
    supabase_url = "https://rhfvjesulpmswnuzmrmz.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoZnZqZXN1bHBtc3dudXptcm16Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0NjE3MDUsImV4cCI6MjAxODAzNzcwNX0.-a8soZeh3szf07ZvwRCHcDZ0yXGwCNZH8QwHIIML6E4"
    
    # Create a Supabase client
    supabase = create_client(supabase_url, supabase_key)

    return supabase
