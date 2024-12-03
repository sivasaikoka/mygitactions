import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import os
from django.conf import settings

type_model_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'type_of_consultation_model1.h5')
med_model_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'prescribed_medications_model1.h5')
adv_model_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'advice_model1.h5')
type_label_encoder_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'type_of_consultation_label_encoder.pkl')
med_label_encoder_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'prescribed_medications_label_encoder.pkl')
adv_label_encoder_path = os.path.join(settings.STATIC_ROOT, 'bfi', 'advice_label_encoder.pkl')
token_label = os.path.join(settings.STATIC_ROOT, 'bfi', 'tokenizer.pkl')

type_model = load_model(type_model_path)
med_model = load_model(med_model_path)
adv_model = load_model(adv_model_path)

type_label_encoder = joblib.load(type_label_encoder_path)
med_label_encoder = joblib.load(med_label_encoder_path)
adv_label_encoder = joblib.load(adv_label_encoder_path)

def preprocess_input(input_data):
    tokenizer = joblib.load(token_label)
    max_seq_length = 100

    if input_data is None:
        return None

    X_input = []
    for col in ['vital_history', 'other_history', 'cc_brief_history', 'allergy', 'investigation', 'diagnosis']:
        if isinstance(col, str) and col in input_data:
            data = input_data[col]
        else:
            data = ''  # Or any appropriate default value

        if isinstance(data, str):
            # If data is a string, convert it to a dictionary with 'history' key
            data = {'history': data}

        if col == 'vital_history':
            vital_sequence = ' '.join([value for value in data.values() if value])
            X_input.append(pad_sequences(tokenizer.texts_to_sequences([vital_sequence]), maxlen=max_seq_length))
        else:
            X_input.append(pad_sequences(tokenizer.texts_to_sequences([data['history']]), maxlen=max_seq_length))

    X_input = np.concatenate(X_input, axis=1)
    return X_input

def make_predictions(input_data):
    X_input = preprocess_input(input_data)

    if X_input is None:
        return None, None, None

    type_prediction = type_model.predict(X_input)
    med_prediction = med_model.predict(X_input)
    adv_prediction = adv_model.predict(X_input)

    decoded_type_prediction = type_label_encoder.inverse_transform([np.argmax(type_prediction)])
    decoded_med_prediction = med_label_encoder.inverse_transform([np.argmax(med_prediction)])
    decoded_adv_prediction = adv_label_encoder.inverse_transform([np.argmax(adv_prediction)])

    return decoded_type_prediction[0], decoded_med_prediction[0], decoded_adv_prediction[0]
