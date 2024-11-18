import streamlit as st
import joblib

# Load your saved model
model = joblib.load('Malpred.joblib')

# Label mapping
label_mapping = {1: "Malaria", 0: "No Malaria"}

# Define the prediction function
def predict_malaria(input_data):
    prediction = model.predict([input_data])[0]  # Predict the class (0 or 1)
    return label_mapping[prediction]

# Streamlit App
st.title("Malaria Prediction App")
st.write("This app predicts the likelihood of malaria based on symptoms. Additionally, you can input vital signs for reference purposes.")

# Dropdowns for symptoms
st.subheader("Symptoms")
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

# Section for additional inputs (not part of the model)
st.subheader("Additional Medical Inputs")
bp = st.text_input("Blood Pressure (e.g., 120/80)", help="Enter the patient's blood pressure in the format Systolic/Diastolic.")
temperature = st.number_input("Temperature (in °C)", min_value=30.0, max_value=45.0, step=0.1, help="Enter the patient's temperature in degrees Celsius.")

# Prediction button
if st.button("Predict"):
    # Validate BP input
    try:
        systolic, diastolic = map(int, bp.split("/"))
    except ValueError:
        systolic = diastolic = None  # Set None if BP is invalid

    # Model prediction
    result = predict_malaria(input_data)
    
    # Display prediction
    st.success(f"The prediction result is: {result}")
    
    # Display additional medical information
    st.subheader("Additional Information:")
    if systolic and diastolic:
        st.write(f"Blood Pressure: {systolic}/{diastolic} mmHg")
    else:
        st.write("Blood Pressure: Invalid or not provided.")
    st.write(f"Temperature: {temperature:.1f}°C")
