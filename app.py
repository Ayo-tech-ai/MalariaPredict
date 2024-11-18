import streamlit as st
import joblib

# Load your saved model
model = joblib.load('Malpred.joblib')

# Label mapping
label_mapping = {1: "high Possibility of Malaria", 0: "Very low Possiblity of Malaria"}

# Define the prediction function
def predict_malaria(input_data):
    prediction = model.predict([input_data])[0]  # Predict the class (0 or 1)
    return label_mapping[prediction]

# Streamlit App
st.title("Malaria Prediction App")
st.write("This app predicts the likelihood of malaria based on symptoms. Please select 'Yes' or 'No' for each symptom below:")

# Dropdowns for input features
fever = st.selectbox("Fever", options=["Yes", "No"])
cold = st.selectbox("Cold", options=["Yes", "No"])
rigor = st.selectbox("Rigor", options=["Yes", "No"])
fatigue = st.selectbox("Fatigue", options=["Yes", "No"])
headache = st.selectbox("Headache", options=["Yes", "No"])
bitter_tongue = st.selectbox("Bitter Tongue", options=["Yes", "No"])
vomiting = st.selectbox("Vomiting", options=["Yes", "No"])
diarrhea = st.selectbox("Diarrhea", options=["Yes", "No"])

# Map "Yes" and "No" to 1 and 0
input_data = [
    1 if fever == "Yes" else 0,
    1 if cold == "Yes" else 0,
    1 if rigor == "Yes" else 0,
    1 if fatigue == "Yes" else 0,
    1 if headache == "Yes" else 0,
    1 if bitter_tongue == "Yes" else 0,
    1 if vomiting == "Yes" else 0,
    1 if diarrhea == "Yes" else 0,
]

# Prediction button
if st.button("Predict"):
    result = predict_malaria(input_data)
    st.success(f"The result is: {result}")
