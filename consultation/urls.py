from django.urls import path
from .views import PredictionView
app_name='consultation'
urlpatterns = [
    path('predict/', PredictionView.as_view(), name='predict'),
]
