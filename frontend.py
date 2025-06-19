import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Category Prediction")

st.markdown("Enter your details to predict the insurance premium category:")

#Input fields
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.7)
income = st.number_input("Annual Income in LPA($)", min_value=0.1, value=5.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City of Residence", value="Delhi")
occupation = st.selectbox('Occupation',['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'])

if st.button("Predict"):
    # Prepare the data for prediction
    data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income,  # Update the key to match the API schema
        "smoker": smoker,
        "city": city,  # Ensure this matches the expected field name
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"Predicted Insurance Premium Category: {prediction['predicted_category']}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Please ensure the backend is running on port 8000.")