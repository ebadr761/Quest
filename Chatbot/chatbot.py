import pandas as pd
import streamlit as st
import os
import google.generativeai as genai # Using gemini
import plotly.express as px # for the chart (price vs range if the user wants to visualize the data)

# --- SETUP ---
GOOGLE_API_KEY = "AIzaSyCpJV2O1YgxH7mPQISRViRhAePHGRcisvI"  # Ebad Google API key
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

    if submitted: # Add new data to the DataFrame and save it (this happens only if the user manually adds a new entry)

        match_idx = data[data["Model"].str.lower() == model.strip().lower()].index #check if model already exists

        if not match_idx.empty:
            #update existing entry
            data.at[match_idx[0], "Brand"] = brand
            data.at[match_idx[0], "Range (km)"] = range_km
            data.at[match_idx[0], "Price (USD)"] = price
            st.info("✅ Existing entry updated!") # tells user that existing entry UPDATED

        else:
            new_row = pd.DataFrame([[brand, model, range_km, price]], columns=data.columns)
            data = pd.concat([data, new_row], ignore_index=True)
            save_excel(data)
            st.success("✅ Data added successfully!") # tells user that new entry ADDED

# --- CHAT INTERFACE ---
st.subheader("💬 Ask a Question About the Data")
user_query = st.text_input("Your question:")

show_chart = False

if user_query:
    #STEP 1: Check if the user wants to visualize the data <---- ADDITIONAL FEATURE ADDED
    chart_check_prompt = f"""
    The user asked: \"{user_query}\"

    Based on this, would it be helpful to show a chart comparing car price vs. range?
    Answer only with \"yes\" or \"no\".
    """
    try:
        chart_model = genai.GenerativeModel("models/gemini-1.5-flash")     #Letting gemini decide if chart is needed
        chart_response = chart_model.generate_content(chart_check_prompt)
        show_chart = chart_response.text.strip().lower().startswith("yes")
        if show_chart:
            st.markdown("📊 Showing chart as requested...")
    except:
        show_chart = False

        # STEP 2: Generate a response using Gemini AI (only happens if chart isn't shown)
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

# --- CONDITIONAL VISUALIZATION ---
if show_chart and not data.empty:
    fig = px.scatter(
        data,
        x="Range (km)",
        y="Price (USD)",
        text="Model",
        hover_data=["Brand", "Model", "Range (km)", "Price (USD)"],
        title="Electric Car Range vs Price",
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- DATA VIEW ---
with st.expander("📊 View Data"):
    st.dataframe(data)

# --- DELETE ENTRY UI ---
with st.expander("❌ Remove a Car by Model"):
    with st.form("delete_form"):
        delete_model = st.text_input("Enter the exact model name to delete")
        delete_submit = st.form_submit_button("Delete Entry")

    if delete_submit:
        match_idx = data[data["Model"].str.lower() == delete_model.strip().lower()].index
        if not match_idx.empty:
            data = data.drop(index=match_idx).reset_index(drop=True)
            save_excel(data)
            st.success(f"✅ Deleted '{delete_model}' from the dataset.")
        else:
            st.warning(f"⚠️ Model '{delete_model}' not found.")