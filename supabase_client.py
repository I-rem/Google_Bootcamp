from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_case_result(data: dict):
    response = supabase.table("case_results").insert(data).execute()
    return response

def fetch_all_results():
    response = supabase.table("case_results").select("*").order("timestamp", desc=True).execute()
    return response.data
