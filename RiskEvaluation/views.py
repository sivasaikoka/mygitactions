from django.shortcuts import render
# views.py
import pandas as pd
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient,Beneficiary, Prediction
from .serializers import PatientSerializer,BeneficiarySerializer, PredictionSerializer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import json
from django.shortcuts import render
import os 
from django.conf import settings
import datetime
# import matplotlib.pyplot as plt
# Create your views here.

def home(request):
    return render(request,'RiskEvaluation/index.html')
def RiskRecommand(request):
    return render(request,'RiskEvaluation/risk_recommand.html')
def BmiPrediction(request):
    return render(request,'RiskEvaluation/health_data.html')


data_path=os.path.join(settings.STATIC_ROOT,'data','patient_data.csv')

# Load and preprocess data
data = pd.read_csv(data_path)  # Update the path to the actual CSV file
columns_with_missing = data.columns[data.isnull().any()]

for col in columns_with_missing:
    if data[col].dtype == 'object':
        data[col] = data[col].fillna(data[col].mode().iloc[0])
    else:
        data[col] = data[col].fillna(data[col].mean())

data_encoded = pd.get_dummies(data, columns=["Gender", "Diabetes", "Energy Levels", "Sleep Issues",
                                             "Diet", "Physical Activity Level", "Smoking/Alcohol",
                                             "Mental Health", "Diagnosis Conditions", "Ayush Practices"])

X = data_encoded.drop(columns=["Patient ID", "Name", "Occupation", "Symptoms", "Family History",
                               "BP Value", "Risk Score", "Diet Recommendation", "Exercise Recommendation"])
y_risk = data_encoded["Risk Score"]
y_diet = data_encoded["Diet Recommendation"]
y_exercise = data_encoded["Exercise Recommendation"]

imputer_path=os.path.join(settings.STATIC_ROOT,'RiskEvaluation','imputer.pkl')
model_risk_path=os.path.join(settings.STATIC_ROOT,'RiskEvaluation','model_risk.pkl')
model_diet_path=os.path.join(settings.STATIC_ROOT,'RiskEvaluation','model_diet.pkl')
model_exercise_path=os.path.join(settings.STATIC_ROOT,'RiskEvaluation','model_exercise.pkl')

class PredictView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            
            Patient_instance = serializer.save()
            input_data = serializer.validated_data  # Use validated_data instead of data

            # Convert the input data into a DataFrame
            input_df = pd.DataFrame([input_data])

            # One-hot encode the input data
            input_encoded = pd.get_dummies(input_df, columns=["gender", "diabetes", "energy_levels",
                                                              "diet", "physical_activity_level", "smoking_alcohol",
                                                              "mental_health", "diagnosis_conditions", "ayush_practices"])
            
            input_encoded.rename(columns={
                'age': 'Age',
                'height': 'Height (cm)',
                'weight': 'Weight (kg)',
                'bmi': 'BMI',
                'gender_Female': 'Gender_Female',
                'gender_Male': 'Gender_Male',
                'gender_Other': 'Gender_Other',
                'diabetes_No': 'Diabetes_No',
                'diabetes_Yes': 'Diabetes_Yes',
                'energy_levels_Low': 'Energy Levels_Low',
                'energy_levels_High': 'Energy Levels_High',
                'energy_levels_Moderate': 'Energy Levels_Moderate',
                'energy_levels_Very High': 'Energy Levels_Very High',
                'energy_levels_Very Low': 'Energy Levels_Very Low',
                'sleep_issuessymptoms': 'Sleep Issues',
                'diet_Balanced': 'Diet_Balanced',
                'diet_High in Fat': 'Diet_High in Fat',
                'diet_High in Sugar': 'Diet_High in Sugar',
                'diet_Keto': 'Diet_Keto',
                'diet_Low in Protein': 'Diet_Low in Protein',
                'diet_Vegan': 'Diet_Vegan',
                'diet_Vegetarian': 'Diet_Vegetarian',
                'physical_activity_level_Low': 'Physical Activity Level_Low',
                'physical_activity_level_Moderate': 'Physical Activity Level_Moderate',
                'physical_activity_level_Sedentary': 'Physical Activity Level_Sedentary',
                'physical_activity_level_Active': 'Physical Activity Level_Active',
                'physical_activity_level_Very Active': 'Physical Activity Level_Very Active',
                'smoking_alcohol_Regular': 'Smoking/Alcohol_Regular',
                'mental_health_Excellent': 'Mental Health_Excellent',
                'mental_health_Good': 'Mental Health_Good',
                'mental_health_Fair': 'Mental Health_Fair',
                'mental_health_Poor': 'Mental Health_Poor',
                'diagnosis_conditions_Cancer (Stage 3)': 'Diagnosis Conditions_Cancer (Stage 3)',
                'ayush_practices_Siddha': 'Ayush Practices_Siddha'
            }, inplace=True)
            

            # Reindex to match training data columns and ensure data type consistency
            input_encoded = input_encoded.reindex(columns=X.columns, fill_value=0)

            # Handle boolean columns if any
            boolean_columns = input_encoded.select_dtypes(include=['bool']).columns
            input_encoded[boolean_columns] = input_encoded[boolean_columns].astype(int)

            # Ensure data type consistency
            input_encoded = input_encoded.astype(X.dtypes)


            # Load imputer
            imputer = joblib.load(imputer_path)

            # Impute missing values using the fitted imputer
            input_imputed = pd.DataFrame(imputer.transform(input_encoded), columns=input_encoded.columns)

            # Ensure that data types are preserved
            input_imputed = input_imputed.astype(X.dtypes)

            # Load models
            model_risk = joblib.load(model_risk_path)
            model_diet = joblib.load(model_diet_path)
            model_exercise = joblib.load(model_exercise_path)


            # Make predictions
            predicted_risk_score = model_risk.predict(input_imputed)[0]
            predicted_diet_recommendation = model_diet.predict(input_imputed)[0]
            predicted_exercise_recommendation = model_exercise.predict(input_imputed)[0]


            # Add predictions to response
            response_data = {
                **input_data,  # Include original input data in the response
                'predicted_risk_score': predicted_risk_score,
                'predicted_diet_recommendation': predicted_diet_recommendation,
                'predicted_exercise_recommendation': predicted_exercise_recommendation
            }

            # Debugging: Print response_data
            #print("Response data:")
            #print(response_data)

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Load the data (assuming 'data17.csv' exists in the current directory)
file_path = os.path.join(settings.STATIC_ROOT, 'data', 'risk_prediction.csv')
csv_data = pd.read_csv(file_path)
csv_data['capture_date'] = pd.to_datetime(csv_data['capture_date'], format='%d-%m-%Y %H:%M')
csv_data['year'] = csv_data['capture_date'].dt.year
csv_data['month'] = csv_data['capture_date'].dt.month
csv_data['height_m'] = csv_data['height'] / 100
csv_data['bmi'] = csv_data['weight'] / (csv_data['height_m'] ** 2)

# Handle missing values in CSV data
csv_data['bmi'] = csv_data['bmi'].fillna(csv_data['bmi'].mean())
csv_data['diabetic_value'] = csv_data['diabetic_value'].fillna(csv_data['diabetic_value'].mean())
csv_data['bp_value'] = csv_data['bp_value'].replace('/', np.nan)
csv_data['bp_value'] = csv_data['bp_value'].fillna(method='ffill')
csv_data[['systolic', 'diastolic']] = csv_data['bp_value'].str.split('/', expand=True).astype(float)
csv_data['pulse_rate'] = csv_data['pulse_rate'].fillna(csv_data['pulse_rate'].mean())
csv_data = csv_data.dropna(subset=['systolic', 'diabetic_value', 'bmi'])

# Fetch data from the database
def fetch_data_from_db():
    db_data = []
    beneficiaries = Beneficiary.objects.all()
    for beneficiary in beneficiaries:
        beneficiary_data = {
            'beneficiary_id': beneficiary.beneficiary_id,
            'capture_date': beneficiary.capture_date,
            'height': beneficiary.height,
            'weight': beneficiary.weight,
            'oxigen_count': beneficiary.oxygen_count,
            'temperature': beneficiary.temperature,
            'pulse_rate': beneficiary.pulse_rate,
            'diabetic_value': beneficiary.diabetic_value,
            'systolic': beneficiary.systolic,
            'diastolic': beneficiary.diastolic,
        }
        db_data.append(beneficiary_data)
    db_df = pd.DataFrame(db_data)
    if not db_df.empty:
        db_df['capture_date'] = pd.to_datetime(db_df['capture_date'])
        db_df['year'] = db_df['capture_date'].dt.year
        db_df['month'] = db_df['capture_date'].dt.month
        db_df['height_m'] = db_df['height'] / 100
        db_df['bmi'] = db_df['weight'] / (db_df['height_m'] ** 2)
    return db_df

# Combine CSV and database data
db_data = fetch_data_from_db()
# db_data=None
if not db_data.empty:
    combined_data = pd.concat([csv_data, db_data], ignore_index=True)
else:
    combined_data = csv_data
# combined_data = csv_data
# Define features and targets
features = ['height', 'weight', 'oxigen_count', 'temperature', 'pulse_rate', 'year', 'month', 'diabetic_value', 'systolic', 'diastolic']
target_bmi = 'bmi'
target_diabetic = 'diabetic_value'
target_systolic = 'systolic'
target_diastolic = 'diastolic'

# Function to train models and make predictions
def train_and_predict_for_beneficiary(beneficiary_id, present_input):
    filtered_data = combined_data[combined_data['beneficiary_id'] == beneficiary_id]

    if filtered_data.shape[0] < 2:
        return {"error": f"Not enough data available for beneficiary_id: {beneficiary_id}"}

    X = filtered_data[features]
    y_bmi = filtered_data[target_bmi]
    y_diabetic = filtered_data[target_diabetic]
    y_systolic = filtered_data[target_systolic]
    y_diastolic = filtered_data[target_diastolic]

    X.fillna(X.mean(), inplace=True)
    
    if X.shape[0] < 2:
        return {"error": f"Not enough data after preprocessing for beneficiary_id: {beneficiary_id}"}

    X_train, X_test, y_bmi_train, y_bmi_test = train_test_split(X, y_bmi, test_size=0.2, random_state=42)
    X_train, X_test, y_diabetic_train, y_diabetic_test = train_test_split(X, y_diabetic, test_size=0.2, random_state=42)
    X_train, X_test, y_systolic_train, y_systolic_test = train_test_split(X, y_systolic, test_size=0.2, random_state=42)
    X_train, X_test, y_diastolic_train, y_diastolic_test = train_test_split(X, y_diastolic, test_size=0.2, random_state=42)

    if X_train.shape[0] < 2 or X_test.shape[0] < 1:
        return {"error": f"Not enough data after train-test split for beneficiary_id: {beneficiary_id}"}

    # Train models
    model_bmi = RandomForestRegressor(random_state=42)
    model_bmi.fit(X_train, y_bmi_train)

    model_diabetic = RandomForestRegressor(random_state=42)
    model_diabetic.fit(X_train, y_diabetic_train)

    model_systolic = RandomForestRegressor(random_state=42)
    model_systolic.fit(X_train, y_systolic_train)

    model_diastolic = RandomForestRegressor(random_state=42)
    model_diastolic.fit(X_train, y_diastolic_train)

    # Initialize prediction arrays
    future_bmi_pred = []
    future_diabetic_pred = []
    future_systolic_pred = []
    future_diastolic_pred = []

    # Predict future values
    last_date = datetime.datetime.now()
    future_dates = [last_date + datetime.timedelta(days=30 * i) for i in range(1, 7)]  # Predict next 6 months
    future_data = pd.DataFrame({'capture_date': future_dates})
    future_data['year'] = future_data['capture_date'].dt.year
    future_data['month'] = future_data['capture_date'].dt.month

    future_predictions = []
    future_X = pd.DataFrame(columns=features)  # Initialize an empty DataFrame with columns

    for i in range(6):
        if i == 0:
            future_input = pd.DataFrame([present_input])
        else:
            future_input = future_X.iloc[i - 1].copy()
            future_input['year'] = future_data.iloc[i]['year']
            future_input['month'] = future_data.iloc[i]['month']
            future_input['bmi'] = future_bmi_pred[i - 1]  # Use the previous month's BMI prediction
            future_input['diabetic_value'] = future_diabetic_pred[i - 1]  # Use the previous month's diabetic value prediction
            future_input['systolic'] = future_systolic_pred[i - 1]  # Use the previous month's systolic prediction
            future_input['diastolic'] = future_diastolic_pred[i - 1]  # Use the previous month's diastolic prediction
            future_input = pd.DataFrame([future_input])  # Ensure it's a DataFrame

        # Predict values for the current month
        bmi_pred = model_bmi.predict(future_input[features])
        diabetic_pred = model_diabetic.predict(future_input[features])
        systolic_pred = model_systolic.predict(future_input[features])
        diastolic_pred = model_diastolic.predict(future_input[features])

        # Append predictions to respective lists
        future_bmi_pred.append(bmi_pred[0])
        future_diabetic_pred.append(diabetic_pred[0])
        future_systolic_pred.append(systolic_pred[0])
        future_diastolic_pred.append(diastolic_pred[0])

        # Append the new row to future_X using pd.concat
        future_X = pd.concat([future_X, future_input], ignore_index=True)

        future_predictions.append({
            "month": i + 1,
            "predicted_bmi": bmi_pred[0],
            "predicted_diabetic_value": diabetic_pred[0],
            "predicted_systolic": systolic_pred[0],
            "predicted_diastolic": diastolic_pred[0],
        })

    return {"future_predictions": future_predictions}



@api_view(['POST'])
def predict_health_data(request):
    serializer = BeneficiarySerializer(data=request.data)
    if serializer.is_valid():
        beneficiary = serializer.save()
        present_input = {
            'height': beneficiary.height,
            'weight': beneficiary.weight,
            'oxigen_count': beneficiary.oxygen_count,
            'temperature': beneficiary.temperature,
            'pulse_rate': beneficiary.pulse_rate,
            'diabetic_value': beneficiary.diabetic_value,
            'systolic': beneficiary.systolic,
            'diastolic': beneficiary.diastolic,
            'year': datetime.datetime.now().year,
            'month': datetime.datetime.now().month,
        }
        result = train_and_predict_for_beneficiary(beneficiary.beneficiary_id, present_input)
        if 'error' in result:
            return Response(result, status=400)
        
        # Save predictions to the database
        for prediction in result['future_predictions']:
            Prediction.objects.create(
                beneficiary=beneficiary,
                prediction_date=datetime.datetime.now() + datetime.timedelta(days=30 * prediction['month']),
                predicted_bmi=prediction['predicted_bmi'],
                predicted_diabetic_value=prediction['predicted_diabetic_value'],
                predicted_systolic=prediction['predicted_systolic'],
                predicted_diastolic=prediction['predicted_diastolic']
            )

        return Response(result)
    return Response(serializer.errors, status=400)