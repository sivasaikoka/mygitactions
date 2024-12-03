# chat/urls.py
from django.urls import path
from .views import ChatBotView



app_name='ChatBot'
urlpatterns = [
    path('chat/', ChatBotView.as_view(), name='chatbot'),
    # path('api/suggest_doctors/', SuggestDoctorsView.as_view(), name='suggest_doctors'),
    # path('api/book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
]
