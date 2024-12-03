# chat/bot_logic.py
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
import re
from .models import Doctor
from django.conf import settings

# Function to load intents and responses from JSON
def load_intents():
    intents_data = {
        'greeting': "Hello! How can I assist you today?",
        'find_doctor': "I can help you find a doctor. Please provide more details.",
        'book_appointment': "Let's schedule your appointment. When would you like to book?",
        'insurance_inquiry': "For insurance inquiries, please contact our insurance department.",
        'billing_inquiry': "For billing inquiries, please visit our billing department.",
        'test_results': "To access your test results, please consult your healthcare provider.",
        'prescription_refill': "To refill your prescription, please contact your pharmacy.",
        'hospital_information': "For information about our hospital, please visit our website.",
        'feedback': "We appreciate your feedback! Please share your thoughts with us.",
        'support': "For technical support, please contact our support team.",
        'symptom_analysis': "Let's analyze your symptoms. Please describe your symptoms.",
        'health_education': "Here are some resources for your health education.",
        'preventive_care': "To prevent health issues, consider these preventive care tips.",
        'faq_cancellation': "For information about cancellations, please review our cancellation policy.",
        'faq_forms': "To fill out forms before your appointment, visit our forms section."
    }
    
    intents = {}
    for intent, bot_response in intents_data.items():
        intents[intent] = bot_response
    
    return intents

# Train and save intent recognition model
def train_intent_recognition_model():
    # Download NLTK resources (if not already downloaded)
    nltk.download('punkt')
    nltk.download('stopwords')

    # Step 1: Load the CSV Data
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'ChatBot/Data/', 'data.csv'))

    # Step 2: Preprocess the Data
    def preprocess_text(text):
        # Lowercase
        text = text.lower()
        # Remove punctuation and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Tokenize
        tokens = nltk.word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        # Stemming (optional)
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
        # Join tokens back into text
        processed_text = ' '.join(stemmed_tokens)
        return processed_text

    # Assuming 'text' is the correct column name containing text data
    df['processed_text'] = df['query'].apply(preprocess_text)

    # Step 3: Split Data into Training and Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(df['processed_text'], df['intent'], test_size=0.2, random_state=42)

    # Step 4: Vectorize Text Data using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Step 5: Train a Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_vec, y_train)

    # Ensure the models directory exists
    model_dir = os.path.join(settings.BASE_DIR, 'ChatBot/models')
    os.makedirs(model_dir, exist_ok=True)

    # Save the model and vectorizer
    joblib.dump(rf_model, os.path.join(model_dir, 'intent_model.pkl'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.pkl'))

# Function to load trained intent recognition model
def load_intent_model():
    model_file = os.path.join(settings.BASE_DIR, 'ChatBot/models', 'intent_model.pkl')
    vectorizer_file = os.path.join(settings.BASE_DIR, 'ChatBot/models', 'vectorizer.pkl')
    model = joblib.load(model_file)
    vectorizer = joblib.load(vectorizer_file)
    return model, vectorizer

# Function to get bot response based on user input
def get_bot_response(user_input):
    model, vectorizer = load_intent_model()
    user_input_vec = vectorizer.transform([user_input])
    intent = model.predict(user_input_vec)[0]
    print(intent)
    
    intents = load_intents()

    if intent in intents:
        bot_response = intents[intent]
        # Optionally, you can customize responses based on intent specifics here
        if '[specialty]' in bot_response:
            bot_response = bot_response.replace('[specialty]', 'the relevant specialty')  # Example replacement
            # Implement further customizations as needed for other placeholders
        return bot_response
    else:
        return "I'm not sure how to help with that. Can you please rephrase?"
train_intent_recognition_model()