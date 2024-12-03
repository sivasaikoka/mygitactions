from rest_framework.views import APIView
from .serializers import InputDataSerializer, OutputDataSerializer
from rest_framework.response import Response
from django.shortcuts import render
from .forms import VitalHistoryForm, OtherHistoryForm, CCBriefHistoryForm, AllergyForm, InvestigationForm, DiagnosisForm
from .prediction import make_predictions
import ast,json

class PredictionView(APIView):
    def get(self, request, format=None):
        # Render the form template for user input
        vital_form = VitalHistoryForm()
        other_form = OtherHistoryForm()
        cc_brief_form = CCBriefHistoryForm()
        allergy_form = AllergyForm()
        investigation_form = InvestigationForm()
        diagnosis_form = DiagnosisForm()
        return render(request, 'consultation_app/prediction_form.html', {
            'vital_form': vital_form,
            'other_form': other_form,
            'cc_brief_form': cc_brief_form,
            'allergy_form': allergy_form,
            'investigation_form': investigation_form,
            'diagnosis_form': diagnosis_form
        })

    def post(self, request, format=None):
        # Check if request content type is JSON
        if request.content_type == 'application/json':
            # Process JSON input
            input_serializer = InputDataSerializer(data=request.data)
            if not input_serializer.is_valid():
                return Response(input_serializer.errors, status=400)

            input_data = input_serializer.validated_data

            # Make predictions using existing function
            type_prediction, med_prediction, adv_prediction = make_predictions(input_data)

            # Ensure predictions are not None
            if None in [type_prediction, med_prediction, adv_prediction]:
                return Response({"error": "Failed to make predictions."}, status=400)
            
            med_prediction=med_prediction.replace('true', 'True').replace('false', 'False')
            # print(med_prediction,type(med_prediction))
            med_prediction_list=ast.literal_eval(med_prediction)
            # adv_prediction=adv_prediction.replace('true', 'True').replace('false', 'False')
            adv_prediction_list=json.loads(adv_prediction)

            # Serialize the output data
            output_data = {
                'type_of_consultation_prediction': type_prediction,
                'prescribed_medications_prediction': med_prediction_list,
                'advice_prediction': adv_prediction_list
            }


            # Return JSON response for API requests
            output_serializer = OutputDataSerializer(output_data)
            return Response(output_data)

        else:
            # Process form input and render prediction results
            return self.render_prediction_results(request)

    def render_prediction_results(self, request):
        # Handle form submission
        vital_form = VitalHistoryForm(request.POST)
        other_form = OtherHistoryForm(request.POST)
        cc_brief_form = CCBriefHistoryForm(request.POST)
        allergy_form = AllergyForm(request.POST)
        investigation_form = InvestigationForm(request.POST)
        diagnosis_form = DiagnosisForm(request.POST)

        # Check if all forms are valid
        if not all([vital_form.is_valid(), other_form.is_valid(), cc_brief_form.is_valid(),
                    allergy_form.is_valid(), investigation_form.is_valid(), diagnosis_form.is_valid()]):
            # Handle form errors
            return render(request, 'consultation_app/prediction_form.html', {
                'vital_form': vital_form,
                'other_form': other_form,
                'cc_brief_form': cc_brief_form,
                'allergy_form': allergy_form,
                'investigation_form': investigation_form,
                'diagnosis_form': diagnosis_form
            })

        # Convert form data to dictionary for input
        input_data = {
            'vital_history': vital_form.cleaned_data,
            'other_history': other_form.cleaned_data,
            'cc_brief_history': cc_brief_form.cleaned_data,
            'allergy': allergy_form.cleaned_data,
            'investigation': investigation_form.cleaned_data,
            'diagnosis': diagnosis_form.cleaned_data
        }

        # Make predictions using existing function
        type_prediction, med_prediction, adv_prediction = make_predictions(input_data)
        med_prediction=med_prediction.replace('true', 'True').replace('false', 'False')
            # print(med_prediction,type(med_prediction))
        med_prediction_list=ast.literal_eval(med_prediction)
        adv_prediction_list=json.loads(adv_prediction)

        # Ensure predictions are not None
        if None in [type_prediction, med_prediction, adv_prediction]:
            error_message = "Failed to make predictions."
            return render(request, 'consultation_app/prediction_form.html', {'error': error_message})
        
        # Add predictions to context
        context = {
            'vital_form': vital_form,
            'other_form': other_form,
            'cc_brief_form': cc_brief_form,
            'allergy_form': allergy_form,
            'investigation_form': investigation_form,
            'diagnosis_form': diagnosis_form,
            'output_data': {
                'type_of_consultation_prediction': type_prediction,
                'prescribed_medications_prediction': med_prediction_list,
                'advice_prediction': adv_prediction_list
            }
        }

        # Render output template with predictions
        return render(request, 'consultation_app/prediction_form.html', context)