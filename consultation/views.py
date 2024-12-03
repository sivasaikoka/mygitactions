from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputDataSerializer, OutputDataSerializer
from .prediction import make_predictions
from django.http import JsonResponse

import json

class PredictionView(APIView):
    def get(self, request, format=None):
        # Get initial data from input serializer
        initial_data = InputDataSerializer().data
        
        # Return the serialized initial data
        return Response(initial_data, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):
        input_serializer = InputDataSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        input_data = input_serializer.validated_data

        # Ensure input data is properly formatted
        if not isinstance(input_data, dict):
            return Response({"error": "Input data should be a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

        # Make predictions using your existing function
        type_prediction, med_prediction, adv_prediction = make_predictions(input_data)

        # Ensure predictions are not None
        if type_prediction is None or med_prediction is None or adv_prediction is None:
            return Response({"error": "Failed to make predictions."}, status=status.HTTP_400_BAD_REQUEST)

        # Decode the JSON strings if they are not already decoded
        if isinstance(med_prediction, str):
            med_prediction = json.loads(med_prediction)
        if isinstance(adv_prediction, str):
            adv_prediction = json.loads(adv_prediction)

        # Serialize the output data
        output_data = {
            'type_of_consultation_prediction': type_prediction,
            'prescribed_medications_prediction': med_prediction,
            'advice_prediction': adv_prediction
        }

        # Return the output data with a success status
        return Response(output_data, status=status.HTTP_200_OK)

        # print(output_serializer)
        # if output_serializer.is_valid():
        #     return Response(output_serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(output_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
