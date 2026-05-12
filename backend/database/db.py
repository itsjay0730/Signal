import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#save the signals
def save_signals(signals: list):
    response = supabase.table("signals").insert(signals).execute()
    return response

#save the internships
def save_internships(internships: list):
    response = supabase.table("internships").insert(internships).execute()
    return response
