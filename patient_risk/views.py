from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Consultation
from .serializers import ConsultationSerializer
from .forms import ConsultationForm
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

class ConsultationCreateView(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        type_prediction, med_prediction, adv_prediction = make_predictions(serializer.data)
        instance.type_prediction = type_prediction
        instance.med_prediction = med_prediction
        instance.adv_prediction = adv_prediction
        instance.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        type_prediction, med_prediction, adv_prediction = make_predictions(serializer.data)

        if request.headers.get('accept') == 'json':
            return JsonResponse({
                'type_prediction': type_prediction,
                'med_prediction': med_prediction,
                'adv_prediction': adv_prediction
            })
        else:
            return render(request, 'patient_risk/predictions.html', {
                'type_prediction': type_prediction,
                'med_prediction': med_prediction,
                'adv_prediction': adv_prediction
            })


def consultation_form(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            type_prediction, med_prediction, adv_prediction = make_predictions(form.cleaned_data)
            consultation.type_prediction = type_prediction
            consultation.med_prediction = med_prediction
            consultation.adv_prediction = adv_prediction
            consultation.save()

            if request.headers.get('accept') == 'application/json':
                return JsonResponse({
                    'type_prediction': type_prediction,
                    'med_prediction': med_prediction,
                    'adv_prediction': adv_prediction
                })
            else:
                return render(request, 'patient_risk/predictions.html', {
                    'type_prediction': type_prediction,
                    'med_prediction': med_prediction,
                    'adv_prediction': adv_prediction
                })
    else:
        form = ConsultationForm()
    return render(request, 'patient_risk/consultation_form.html', {'form': form})




# class ConsultationPredictions(APIView):
#     queryset = Consultation.objects.all()
#     serializer_class = ConsultationSerializer

#     def perform_create(self, serializer):
#         instance = serializer.save()
#         type_prediction, med_prediction, adv_prediction = make_predictions(serializer.data)
#         instance.type_prediction = type_prediction
#         instance.med_prediction = med_prediction
#         instance.adv_prediction = adv_prediction
#         instance.save()

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # type_prediction, med_prediction, adv_prediction = make_predictions(serializer.data)

#         if serializer.is_valid():
#             consultation = serializer.save()

#             # Make predictions based on the serializer data
#             type_prediction, med_prediction, adv_prediction = make_predictions(serializer.data)

#             # Assign the predictions to the consultation instance
#             consultation.type_prediction = type_prediction
#             consultation.med_prediction = med_prediction
#             consultation.adv_prediction = adv_prediction

#             # Save the consultation instance with predictions
#             consultation.save()

#             # Return the predictions in the response
#             return Response({
#                 'type_prediction': type_prediction,
#                 'med_prediction': med_prediction,
#                 'adv_prediction': adv_prediction
#             }, status=status.HTTP_200_OK)
#         else:
#             # Return serializer errors if input data is invalid
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultationPredictions(APIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    def post(self, request):
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            consultation = serializer.save()

            # Make predictions based on the serializer data
            type_prediction, med_prediction, adv_prediction = make_predictions(serializer.validated_data)

            # Assign the predictions to the consultation instance
            consultation.type_prediction = type_prediction
            consultation.med_prediction = med_prediction
            consultation.adv_prediction = adv_prediction

            # Save the consultation instance with predictions
            consultation.save()

            # Return the predictions in the response
            return Response({
                'type_prediction': type_prediction,
                'med_prediction': med_prediction,
                'adv_prediction': adv_prediction
            }, status=status.HTTP_200_OK)
        else:
            # Return serializer errors if input data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)