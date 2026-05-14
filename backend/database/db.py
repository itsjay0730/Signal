import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#save the signals
def save_signals(signals: list):
    if not signals:
        print("No signals to save")
        return 
    
    response = supabase.table("signals").insert(signals).execute()
    return response

#save the internships
def save_internships(internships: list):
    if not internships:
        print("No internships to save")
        return
    
    response = supabase.table("internships").upsert(internships).execute()
    return response

#get all signals
def get_all_signals():
    response = supabase.table("signals").select("*").order("score", desc=True).execute()
    return response.data

#get all internships
def get_all_internships():
    response = supabase.table("internships").select("*").execute()
    return response.data