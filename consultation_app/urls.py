from django.urls import path
from .views import PredictionView

app_name='consultation_app'

urlpatterns = [
    path('prediction/', PredictionView.as_view(), name='prediction'),
    # path('result/', PostPredictionView.as_view(), name='result'),
]
