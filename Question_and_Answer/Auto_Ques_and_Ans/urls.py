# urls.py
from django.urls import path
from .views import QuestionInputView, ResultView

app_name = 'Auto_Ques_and_Ans'

urlpatterns = [
    path('', QuestionInputView.as_view(), name='generate_questions'),
    path('result/', ResultView.as_view(), name='result'),
]