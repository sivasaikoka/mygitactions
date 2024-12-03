
# urls.py
from django.urls import path
from .views import ConsultationCreateView, consultation_form,ConsultationPredictions
app_name='patient_risk'
urlpatterns = [
    path('consultations/', ConsultationCreateView.as_view(), name='consultation-create'),
    path('consultation-form/', consultation_form, name='consultation-form'),
    path('predictions/',ConsultationPredictions.as_view(),name='JsonPredictions')
]
