import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, GlobalMaxPooling1D, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Load the dataset
df = pd.read_csv("data.csv")

# Drop unnecessary columns
columns_to_drop = ['modified_on', 'prakruti_constitution', 'general_assessment', 'roga_pariksha',
                   'vata_score', 'pita_score', 'kafa_score', 'nodal_officer_id', 'covid19_scanning',
                   'dependent_id', 'family_history', 'pharmacy_id', 'lab_id', 'lab_availed',
                   'pharmacy_availed', 'comments', 'phc_id', 'direct_auth_status']
df.drop(columns=columns_to_drop, inplace=True)

# Encode categorical variables
label_encoders = {}
for column in ['type_of_consultation', 'is_care_context_linked', 'prescribed_medications', 'advice']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Tokenize text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['vital_history'] + df['other_history'] + df['cc_brief_history'] +
                        df['allergy'] + df['investigation'] + df['diagnosis'])

# Save the tokenizer
with open('tokenizer.pkl', 'wb') as fp:
    joblib.dump(tokenizer, fp)

# Pad sequences
max_seq_length = 100  # Adjust as needed
X = [pad_sequences(tokenizer.texts_to_sequences(df[col]), maxlen=max_seq_length) for col in
     ['vital_history', 'other_history', 'cc_brief_history', 'allergy', 'investigation', 'diagnosis']]
X = np.concatenate(X, axis=1)

# Target variables
y_type_of_consultation = df['type_of_consultation'].values
y_prescribed_medications = df['prescribed_medications'].values
y_advice = df['advice'].values

# Split the data into training and testing sets
X_train, X_test, y_type_train, y_type_test, y_med_train, y_med_test, y_adv_train, y_adv_test = train_test_split(
    X, y_type_of_consultation, y_prescribed_medications, y_advice, test_size=0.2, random_state=42)

# Define LSTM model function with more layers
def build_lstm_model(input_shape, num_classes):
    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=100),
        LSTM(64, return_sequences=True),
        LSTM(32, return_sequences=True),  # Additional LSTM layer
        GlobalMaxPooling1D(),
        Dense(64, activation='relu'),
        Dropout(0.5),  # Add dropout layer to prevent overfitting
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

# Build and train LSTM models with more epochs
models = {}
for target, y_train, y_test in [('type_of_consultation', y_type_train, y_type_test),
                                ('prescribed_medications', y_med_train, y_med_test),
                                ('advice', y_adv_train, y_adv_test)]:
    # Ensure num_classes is max label value + 1
    num_classes = max(np.max(y_train), np.max(y_test)) + 1
    model = build_lstm_model(X_train.shape, num_classes)
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)  # Increased number of epochs
    models[target] = model
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f'{target.capitalize()} - Test Loss: {test_loss}, Test Accuracy: {test_accuracy}')

    # Save the label encoder
    with open(f'{target}_label_encoder.pkl', 'wb') as fp:
        joblib.dump(label_encoders[target], fp)

    # Save the model in .h5 format
    model.save(f'bfi/{target}_model1.h5')

