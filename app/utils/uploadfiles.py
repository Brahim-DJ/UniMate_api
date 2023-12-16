from app.utils.database import connect_to_supabase

supabase = connect_to_supabase()

def upload_avatar_to_supabase(file, user_id):
    file_bytes = file.read()

    # Extract filename and content type from the FileStorage object
    filename = file.filename
    content_type = file.content_type

    # Upload the temporary file to Supabase Storage
    # Example using supabase storage upload (replace with your own Supabase code)
    response = supabase.storage.from_("avatars").upload(
        file=file_bytes,
        path=f'avatars/{user_id}/{filename}',  # Adjust the path as needed
        file_options={"content-type": content_type}
    )

    return response