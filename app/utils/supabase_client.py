from fastapi import UploadFile
from mimetypes import guess_type
from supabase import create_client

import os
import uuid

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL    = os.getenv("SUPABASE_URL")
SUPABASE_KEY    = os.getenv("SUPABASE_KEY")
BUCKET_NAME     = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase(file: UploadFile) -> str:
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    content_type = guess_type(file.filename)[0] or "application/octet-stream"

    file_bytes = file.file.read()
    
    supabase.storage.from_(BUCKET_NAME).upload(
        path = unique_filename,
        file = file_bytes,
        file_options={
            "content-type": content_type,
            "cache-control": "3600"
        }
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    return public_url