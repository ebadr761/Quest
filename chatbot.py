import pandas as pd
import streamlit as st
import os
import google.generativeai as genai

# --- SETUP ---
GOOGLE_API_KEY = "AIzaSyCpJV2O1YgxH7mPQISRViRhAePHGRcisvI"  # Your Google API key
genai.configure(api_key=GOOGLE_API_KEY)

EXCEL_FILE = "electric_cars.xlsx"

# --- LOAD DATA ---
def load_excel():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["Brand", "Model", "Range (km)", "Price (USD)"])

def save_excel(df):
    df.to_excel(EXCEL_FILE, index=False)

# --- MAIN UI ---
st.title("🧠 Gemini Chatbot with Excel Data")

st.markdown("""
This chatbot can answer questions based on an Excel dataset (powered by Gemini AI).
You can also add new entries below, and the chatbot will use both old and new data.
""")

# Load current data
data = load_excel()

# --- DATA ENTRY ---
with st.expander("➕ Add New Data"):
    with st.form("new_data_form"):
        brand = st.text_input("Brand")
        model = st.text_input("Model")
        range_km = st.number_input("Range (km)", min_value=0)
        price = st.number_input("Price (USD)", min_value=0)
        submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = pd.DataFrame([[brand, model, range_km, price]], columns=data.columns)
        data = pd.concat([data, new_row], ignore_index=True)
        save_excel(data)
        st.success("✅ Data added successfully!")

# --- CHAT INTERFACE ---
st.subheader("💬 Ask a Question About the Data")
user_query = st.text_input("Your question:")

if user_query:
    prompt = f"""
You are a helpful assistant. Use the table of electric car data below to answer the user's question.

Data:
{data.to_string(index=False)}

User's question: {user_query}
Answer in a clear and friendly tone.
"""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        st.markdown(f"**Answer:** {response.text}")
    except Exception as e:
        st.error(f"Error generating response: {e}")

# --- DATA VIEW ---
with st.expander("📊 View Data"):
    st.dataframe(data)
