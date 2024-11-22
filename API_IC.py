import streamlit as st
import requests
from supabase import create_client, Client

#Configuración de la conexión a Supabase
SUPABASE_URL = "https://pbsjxezvcmdlwusveukd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(SUPABASE_URL,SUPABASE_KEY)

#Consumir el API de tipo de cambio
def get_exchange_rate(base_currency="USD", target_currency="EUR"):
    url = f"https://api.exchangerate.host/latest?base={base_currency}&symbols={target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error":"No se puede conectar al API"}

#Guardar los datos en Supabase
def save_to_supabase(data):
    response = supabase.table("exchange_rates").insert(data).execute()
    return response