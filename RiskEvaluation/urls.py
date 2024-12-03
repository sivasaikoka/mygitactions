from django.urls import path
from .views import home,PredictView,RiskRecommand,predict_health_data,BmiPrediction


app_name='RiskEvaluation'
urlpatterns = [
    path('',home,name='home'),
    path('RiskRecommand/',RiskRecommand,name='RiskRecommand'),
    path('RiskPrediction/',BmiPrediction,name='RiskPrediction'),
    path('prediction/', predict_health_data, name='predict_health_data'),
    path('predict/', PredictView.as_view(), name='predict'),
]
