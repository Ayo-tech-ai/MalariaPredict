import streamlit as st
import joblib
from fpdf import FPDF
import base64

# Load your saved model
model = joblib.load('Malpred.joblib')

# Label mapping
label_mapping = {1: "High Possibility of Malaria", 0: "Low Possibility of Malaria"}

# Define the prediction function
def predict_malaria(input_data):
    prediction = model.predict([input_data])[0]  # Predict the class (0 or 1)
    return label_mapping[prediction]

# Function to generate and save the PDF
def generate_pdf(result, symptoms, bp, temperature):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Medical Report", ln=True, align='C')
    pdf.ln(10)
    
    # Add prediction result
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Prediction Result:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Likelihood of Illness: {result}", ln=True)
    pdf.ln(10)
    
    # Add symptoms section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Symptoms:", ln=True)
    pdf.set_font("Arial", size=12)
    for symptom_name, presence in symptoms.items():
        pdf.cell(200, 10, txt=f"{symptom_name}: {presence}", ln=True)
    pdf.ln(10)
    
    # Add additional medical information
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Additional Medical Information:", ln=True)
    pdf.set_font("Arial", size=12)
    if bp:
        pdf.cell(200, 10, txt=f"Blood Pressure: {bp}", ln=True)
    else:
        pdf.cell(200, 10, txt="Blood Pressure: Invalid or not provided.", ln=True)
    pdf.cell(200, 10, txt=f"Temperature: {temperature:.1f}°C", ln=True)
    
    # Save PDF to a file
    pdf_file = "medical_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Streamlit App
st.markdown("""
    <style>
    body {
        background-image: url('https://github.com/Ayo-tech-ai/MalariaPredict/raw/main/background1.jpeg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .symptom-text, .additional-info-text, .title-text {
        color: blue;
        font-weight: bold;
    }
    .result-text {
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Main Page Heading
st.markdown("<h1 class='title-text'>AI-Doc Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='title-text'>This AI-powered web App predicts the likelihood of a Patient having malaria based on symptoms.</p>", unsafe_allow_html=True)

# Dropdowns for symptoms (Display in columns)
col1, col2 = st.columns(2)

with col1:
    symptoms = {
        "Fever": st.selectbox("<span class='symptom-text'>Fever</span>", options=["Yes", "No"], format_func=lambda x: x, key="Fever"),
        "Cold": st.selectbox("<span class='symptom-text'>Cold</span>", options=["Yes", "No"], format_func=lambda x: x, key="Cold"),
        "Rigor": st.selectbox("<span class='symptom-text'>Rigor</span>", options=["Yes", "No"], format_func=lambda x: x, key="Rigor"),
        "Fatigue": st.selectbox("<span class='symptom-text'>Fatigue</span>", options=["Yes", "No"], format_func=lambda x: x, key="Fatigue"),
    }

with col2:
    symptoms.update({
        "Headache": st.selectbox("<span class='symptom-text'>Headache</span>", options=["Yes", "No"], format_func=lambda x: x, key="Headache"),
        "Bitter Tongue": st.selectbox("<span class='symptom-text'>Bitter Tongue</span>", options=["Yes", "No"], format_func=lambda x: x, key="Bitter Tongue"),
        "Vomiting": st.selectbox("<span class='symptom-text'>Vomiting</span>", options=["Yes", "No"], format_func=lambda x: x, key="Vomiting"),
        "Diarrhea": st.selectbox("<span class='symptom-text'>Diarrhea</span>", options=["Yes", "No"], format_func=lambda x: x, key="Diarrhea"),
    })

# Map "Yes" and "No" to 1 and 0 for model input
input_data = [1 if value == "Yes" else 0 for value in symptoms.values()]

# Section for additional inputs (not part of the model)
st.subheader("Additional Medical Inputs")
bp = st.text_input("<span class='additional-info-text'>Blood Pressure (e.g., 120/80)</span>", help="Enter the patient's blood pressure in the format Systolic/Diastolic.")
temperature = st.number_input("<span class='additional-info-text'>Temperature (in °C)</span>", min_value=30.0, max_value=45.0, step=0.1, help="Enter the patient's temperature in degrees Celsius.")

# Prediction button
if st.button("Predict"):
    try:
        systolic, diastolic = map(int, bp.split("/"))
        bp_valid = f"{systolic}/{diastolic} mmHg"
    except ValueError:
        bp_valid = None  # Set None if BP is invalid

    result = predict_malaria(input_data)

    st.markdown(f"<p class='result-text'>The prediction result is: {result}</p>", unsafe_allow_html=True)
    st.markdown("<h3 class='additional-info-text'>Additional Information:</h3>", unsafe_allow_html=True)

    if bp_valid:
        st.markdown(f"<p class='symptom-text'>Blood Pressure: {bp_valid}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='symptom-text'>Blood Pressure: Invalid or not provided.</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='symptom-text'>Temperature: {temperature:.1f}°C</p>", unsafe_allow_html=True)
