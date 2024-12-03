import json
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Load the pre-trained models and label encoders
type_model = load_model('bfi/type_of_consultation_model1.h5')
med_model = load_model('bfi/prescribed_medications_model1.h5')
adv_model = load_model('bfi/advice_model1.h5')

type_label_encoder = joblib.load('type_of_consultation_label_encoder.pkl')
med_label_encoder = joblib.load('prescribed_medications_label_encoder.pkl')
adv_label_encoder = joblib.load('advice_label_encoder.pkl')

# Function to preprocess input data
def preprocess_input(input_data):
    tokenizer = joblib.load('tokenizer.pkl')
    max_seq_length = 100

    X_input = []
    for col in ['vital_history', 'other_history', 'cc_brief_history', 'allergy', 'investigation', 'diagnosis']:
        if col == 'vital_history':
            # Handle empty strings in vital history
            vital_data = input_data[col]
            vital_sequence = ' '.join([value for value in vital_data.values() if value])  # Join non-empty values
            X_input.append(pad_sequences(tokenizer.texts_to_sequences([vital_sequence]), maxlen=max_seq_length))
        else:
            X_input.append(pad_sequences(tokenizer.texts_to_sequences([input_data[col]['history']]), maxlen=max_seq_length))
    
    X_input = np.concatenate(X_input, axis=1)
    return X_input

# Function to make predictions
def make_predictions(input_data):
    X_input = preprocess_input(input_data)

    type_prediction = type_model.predict(X_input)
    med_prediction = med_model.predict(X_input)
    adv_prediction = adv_model.predict(X_input)

    decoded_type_prediction = type_label_encoder.inverse_transform([np.argmax(type_prediction)])
    decoded_med_prediction = med_label_encoder.inverse_transform([np.argmax(med_prediction)])
    decoded_adv_prediction = adv_label_encoder.inverse_transform([np.argmax(adv_prediction)])

    return decoded_type_prediction[0], decoded_med_prediction[0], decoded_adv_prediction[0]

# Accept input from the user
input_data = {
    "vital_history": {
        "temperature": input("Enter temperature: "),
        "pulse": input("Enter pulse: "),
        "systolic": input("Enter systolic: "),
        "diastolic": input("Enter diastolic: "),
        "hemoglobin": input("Enter hemoglobin: "),
        "rbsk": input("Enter RBSK status: "),
        "oxigen_count": input("Enter oxygen count: "),
        "diabetic_value": input("Enter diabetic value: "),
        "height": input("Enter height: "),
        "weight": input("Enter weight: "),
        "history": ""  # Add empty string for 'history'
    },
    "other_history": {
        "history": input("Enter other history: ")
    },
    "cc_brief_history": {
        "chiefComplaints": [{"id": 74, "chief_complaint": "Cough", "is_active": True}],
        "otherComplaints": input("Enter other complaints: "),
        "othersifany": input("Enter any other details: "),
        "presentIllness": input("Enter present illness: "),
        "familyhistory": input("Enter family history: "),
        "history": ""  # Add empty string for 'history'
    },
    "allergy": {
        "allergies": input("Enter allergies: "),
        "history": ""  # Add empty string for 'history'
    },
    "investigation": {
        "master": [],
        "otherInvestigation": input("Enter other investigations: "),
        "history": ""  # Add empty string for 'history'
    },
    "diagnosis": {
        "provisionalDiagnosis": [],
        "othersifany": input("Enter any other diagnosis: "),
        "history": ""  # Add empty string for 'history'
    }
}

# Make predictions
type_prediction, med_prediction, adv_prediction = make_predictions(input_data)

# Print predictions
print("Type of Consultation Prediction:", type_prediction)
print("Prescribed Medications Prediction:", med_prediction)
print("Advice Prediction:", adv_prediction)
