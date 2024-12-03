# urls.py
from django.urls import path
from .views import QuestionInputView, ResultView,Homepage

from django.conf import settings
from django.conf.urls.static import static

app_name = 'Auto_Ques_and_Ans'

urlpatterns = [
    path('',Homepage.as_view(),name='homepage'),
    path('questions/', QuestionInputView.as_view(), name='generate_questions'),
    path('result/', ResultView.as_view(), name='result'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)