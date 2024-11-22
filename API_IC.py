import streamlit as st
import yfinance as yf
from supabase import create_client, Client

# Configuración de la conexión a Supabase
SUPABASE_URL = "https://pbsjxezvcmdlwusveukd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Consumir el API de Yahoo Finance usando yfinance
def get_exchange_rate(base_currency="USD", target_currency="EUR"):
    pair = f"{base_currency}{target_currency}=X"
    ticker = yf.Ticker(pair)
    data = ticker.history(period="1d")
    if not data.empty:
        return {"rate": data["Close"][-1]}  # Toma el precio de cierre más reciente
    else:
        return {"error": "No se pudo obtener el tipo de cambio"}

# Guardar los datos en Supabase
def save_to_supabase(data):
    response = supabase.table("exchange_rates").insert(data).execute()
    return response

# Interfaz con Streamlit
st.title("Consulta y Registro de Tipo de Cambio")

# Selección de monedas
base_currency = st.selectbox("Moneda Base", ["USD", "EUR", "PEN"])
target_currency = st.selectbox("Moneda Objetivo", ["USD", "EUR", "PEN"])

# Consultar el tipo de cambio
if st.button("Consultar Tipo de Cambio"):
    exchange_rate_data = get_exchange_rate(base_currency, target_currency)
    if "error" in exchange_rate_data:
        st.error(exchange_rate_data["error"])
    else:
        rate = exchange_rate_data["rate"]
        st.success(f"1 {base_currency} = {rate} {target_currency}")
    
        # Espacio para anotar comentarios
        comment = st.text_area("Escribe un comentario sobre esta consulta:")

        if st.button("Guardar en Supabase"):
            data_to_save = {
                "base_currency": base_currency,
                "target_currency": target_currency,
                "exchange_rate": rate,
                "comment": comment,
            }
            response = save_to_supabase(data_to_save)
            if response.status_code == 201:
                st.success("Datos guardados exitosamente en Supabase.")
            else:
                st.error("Error al guardar los datos en Supabase.")
